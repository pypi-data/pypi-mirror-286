from fastapi import FastAPI, HTTPException, Request, Security, status
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, Field, computed_field
import time
import tiktoken
import uvicorn
import uuid
from typing import List, Optional, Generator, Union
from browser_gpt_api.gpt_automator import GPTAutomator
from browser_gpt_api.settings import env_settings
from contextlib import asynccontextmanager

from browser_gpt_api.utils import ask_yes_no


class VisionTextContent(BaseModel):
    type: str = "text"
    text: str


class VisionImageContent(BaseModel):
    type: str = "image_url"
    image_url: dict


class ChatMessage(BaseModel):
    content: Union[str, List[VisionImageContent | VisionTextContent]]
    role: str = "assistant"
    function_call: None = None
    tool_calls: None = None


class ChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str
    messages: List[ChatMessage]
    stream: Optional[bool] = False
    stream_options: Optional[dict[str, bool]] = None


class TokenUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int

    @computed_field
    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


class MessageContent(BaseModel):
    finish_reason: str | None = None
    index: int = 0
    logprobs: None = None
    message: ChatMessage


class DeltaContent(BaseModel):
    content: None | str = None
    function_call: None = None
    role: None = None
    tool_calls: None = None


class ChunksContent(BaseModel):
    delta: DeltaContent
    finish_reason: None | str = None
    index: int = 0
    logprobs: None = None


class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: "chatcmpl-" + str(uuid.uuid4()))
    choices: list[ChunksContent | MessageContent]
    created: int = Field(default_factory=lambda: int(round(time.time(), 0)))
    model: str
    object: str
    service_tier: None = None
    system_fingerprint: str = Field(default_factory=lambda: str(uuid.uuid4()))
    usage: TokenUsage | None = None


def get_token_count(text: str) -> int:
    encodings = tiktoken.get_encoding("cl100k_base")
    return len(encodings.encode(text))


def combine_messages(messages: List[ChatMessage]) -> str:
    final_prompt = ""
    for i in range(len(messages)):
        prompt = messages[i].content
        role = messages[i].role
        final_prompt += role + ": " + prompt + ","

    return final_prompt


def split_images_prompts(
    messages: List[VisionImageContent | VisionTextContent],
) -> tuple[str, List[str]]:
    final_prompt = ""
    image_urls = []
    for i in range(len(messages)):
        for data in messages[i].content:
            if data.type == "text":
                final_prompt += data.text
            else:
                image_url = data.image_url["url"]
                image_urls.append(image_url)

    return final_prompt, image_urls


def stream_chat_completion_response(
    gpt_automator: GPTAutomator,
    model: str,
    messages: List[ChatMessage],
    token_usage_flag: bool = False,
) -> Generator[str, None, None]:
    final_prompt = combine_messages(messages)
    prompt_token = get_token_count(final_prompt)
    completion_tokens = 0
    req_id = "chatcmpl-" + str(uuid.uuid4())
    system_fingerprint = str(uuid.uuid4())

    for chunk in gpt_automator.send_prompt_stream(final_prompt):
        response_body = ChatCompletionResponse(
            id=req_id,
            system_fingerprint=system_fingerprint,
            model=model,
            choices=[ChunksContent(delta=DeltaContent(content=chunk))],
            usage=None,
            object="chat.completion.chunk",
        )
        yield response_body.model_dump_json()
        completion_tokens += get_token_count(chunk)
    gpt_automator.delete_latest_chat()
    yield ChatCompletionResponse(
        id=req_id,
        system_fingerprint=system_fingerprint,
        model=model,
        choices=[ChunksContent(delta=DeltaContent(), finish_reason="stop")],
        usage=(
            TokenUsage(prompt_tokens=prompt_token, completion_tokens=completion_tokens)
            if token_usage_flag
            else None
        ),
        object="chat.completion.chunk",
    ).model_dump_json()


def get_chat_completion_response(
    gpt_automator: GPTAutomator, model: str, message_list: List[ChatMessage]
) -> ChatCompletionResponse:
    if any((isinstance(message.content, list)) for message in message_list):
        final_prompt, image_urls = split_images_prompts(message_list)
        gpt_automator.image_upload(image_urls)
    else:
        final_prompt = combine_messages(message_list)
    response = gpt_automator.send_prompt(final_prompt)
    gpt_automator.delete_latest_chat()

    prompt_token = get_token_count(final_prompt)
    completion_tokens = get_token_count(response)
    response_msg = ChatMessage(content=response)
    response_body = ChatCompletionResponse(
        model=model,
        choices=[MessageContent(message=response_msg, finish_reason="stop")],
        usage=TokenUsage(
            prompt_tokens=prompt_token,
            completion_tokens=completion_tokens,
        ),
        object="chat.completion",
    )
    return response_body


security = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> bool:
    if credentials.credentials == env_settings.api_key:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_gpt_automator(request: Request):
    return request.app.state.gpt_automator


@asynccontextmanager
async def lifespan(app: FastAPI):
    gpt_automator = GPTAutomator(env_settings, headless=False)

    while True:
        if not gpt_automator.is_user_logged_in():
            answer = ask_yes_no(
                "Please login to your OpenAI account in the browser and press 'y' to continue or n to exit"
            )
            if not answer:
                raise Exception(
                    "Please login to your OpenAI account in the browser and restart the server"
                )
        else:
            break

    if env_settings.headless:
        gpt_automator.reset(env_settings.headless)

    app.state.gpt_automator = gpt_automator
    yield
    print("Exiting Server")


app = FastAPI(title="Browser_gpt_API", lifespan=lifespan)


@app.post("/chat/completions")
async def chat_completion(
    request: ChatCompletionRequest,
    _: bool = Depends(verify_token),
    gpt_automator: GPTAutomator = Depends(get_gpt_automator),
) -> ChatCompletionResponse:
    message = request.messages
    stream = request.stream
    model = request.model
    if stream is True:
        if request.stream_options is not None:
            return StreamingResponse(
                stream_chat_completion_response(
                    gpt_automator,
                    model,
                    message,
                    token_usage_flag=request.stream_options["include_usage"],
                )
            )
        return StreamingResponse(
            stream_chat_completion_response(gpt_automator, model, message)
        )
    else:
        return get_chat_completion_response(gpt_automator, model, message)


@app.get("/")
def home():
    return {"Hello!"}


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        reload=True,
    )
