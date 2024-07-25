from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class EnvironmentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    chrome_profile: str = Field(..., env="CHROME_PROFILE")
    headless: bool = Field(env="HEADLESS", default=True)
    api_key: str = Field(..., env="API_KEY")


env_settings = EnvironmentSettings()
