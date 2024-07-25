import base64
import re
from typing import List
import uuid
import os
import time
import sys
import getpass as gt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from browser_gpt_api.utils import find_locator
from browser_gpt_api.settings import EnvironmentSettings


def get_chrome_profile_path() -> str:
    if sys.platform == "win32":
        return f"C:/Users/{gt.getuser()}/Appdata/Local/Google/Chrome/User Data"
    elif sys.platform == "darwin":
        return "~/Library/Application Support/Google/Chrome"
    elif sys.platform.startswith("linux"):
        return f"/home/{gt.getuser()}/.config/google-chrome"
    else:
        raise Exception("Unidentified OS Platform")


def setup_chrome_driver(config: EnvironmentSettings):
    """
    self_method to setup the chrome-driver profile path and given url.
    """

    profile_path = get_chrome_profile_path()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(f"--user-data-dir={profile_path}")
    chrome_options.add_argument(f"--profile-directory={config.chrome_profile}")
    if sys.platform.startswith("linux"):
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    if config.headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def base64_to_image(base64_string: str, output_file_path: str) -> None:
    image_data = base64.b64decode(base64_string)
    with open(output_file_path, "wb") as output_file:
        output_file.write(image_data)


class GPTAutomator:
    config: EnvironmentSettings

    def __init__(self, config: EnvironmentSettings, headless: bool = False):
        self.config = config.model_copy()
        self.config.headless = headless
        self._initialize()

    def _initialize(self):
        self.profile = self.config.chrome_profile
        self.driver = setup_chrome_driver(self.config)
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.short_wait = WebDriverWait(self.driver, timeout=5)
        self.chats = []

    def reset(self, headless: bool = None):
        self.driver.quit()
        if headless is not None:
            self.config.headless = headless
        self._initialize()

    def __check_historytab(self):
        """
        self_method to check whether the history-sidebar is open or not
        and opens it if its not.
        """
        history_sidebar_text = self.driver.find_element(
            By.CSS_SELECTOR, "span[data-state='closed'] span"
        ).text
        if history_sidebar_text == "Open sidebar":
            main_tab = self.driver.find_element(By.CSS_SELECTOR, "main")
            history_button = main_tab.find_element(By.CSS_SELECTOR, "button")
            history_button.click()

    def is_user_logged_in(self):
        self.driver.get("https://chatgpt.com")
        locators = [
            "button[data-testid='fruit-juice-profile']",
            "button[data-testid='profile-button']",
        ]

        for locator in locators:
            try:
                self.short_wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, locator))
                )
                self.driver.find_element(By.CSS_SELECTOR, locator)
                return True
            except Exception:
                continue

        return False

    def send_prompt_stream(self, prompt: str):
        """
        Sends a prompt string to the ChatGPT webpage and streams the responses in chunks
        """
        input_form = self.driver.find_element(By.CSS_SELECTOR, "form[class='w-full']")
        inputarea = input_form.find_element(By.ID, "prompt-textarea")
        inputarea.send_keys(prompt)
        send_button = input_form.find_elements(By.CSS_SELECTOR, "button")
        send_button[len(send_button) - 1].click()
        time.sleep(2)
        generate_button_locators = [
            {
                "By": By.CSS_SELECTOR,
                "value": "button[data-testid='fruitjuice-stop-button']",
            },
            {"By": By.CSS_SELECTOR, "value": "button[aria-label='Stop generating']"},
            {"By": By.CSS_SELECTOR, "value": "button[data-testid='stop-button']"},
        ]
        generate_button = find_locator(self.driver, generate_button_locators)
        init_txt = ""
        start_time = time.time()
        while True:
            try:
                if (
                    not generate_button.find_element(
                        By.CSS_SELECTOR, "rect"
                    ).is_displayed()
                    or (time.time() - start_time) > 30
                ):
                    break
                time.sleep(0.1)
                new_txt = self.driver.find_elements(
                    By.CSS_SELECTOR, "div[data-message-author-role='assistant']"
                )[-1].text
                added_txt = new_txt[len(init_txt) :]
                if added_txt != "":
                    yield added_txt
                init_txt = new_txt
            except Exception:
                break

    def send_prompt(self, prompt: str, stream: bool = False) -> str:
        """
        Sends a prompt string to the ChatGPT webpage and returns the response via string.
        """
        input_form = self.driver.find_element(By.CSS_SELECTOR, "form[class='w-full']")
        inputarea = input_form.find_element(By.ID, "prompt-textarea")
        inputarea.send_keys(prompt)
        send_button = input_form.find_elements(By.CSS_SELECTOR, "button")
        send_button[len(send_button) - 1].click()
        time.sleep(2)
        generate_button_locators = [
            {
                "By": By.CSS_SELECTOR,
                "value": "button[data-testid='fruitjuice-stop-button']",
            },
            {"By": By.CSS_SELECTOR, "value": "button[aria-label='Stop generating']"},
            {"By": By.CSS_SELECTOR, "value": "button[data-testid='stop-button']"},
        ]
        generate_button = find_locator(self.driver, generate_button_locators)
        start_time = time.time()
        while True:
            try:
                if (
                    not generate_button.find_element(
                        By.CSS_SELECTOR, "rect"
                    ).is_displayed()
                    or (time.time() - start_time) > 45
                ):
                    break
            except Exception:
                break

        response_box = self.driver.find_elements(
            By.CSS_SELECTOR, "div[data-message-author-role='assistant']"
        )[-1]
        return response_box.text

    def image_upload(self, image_urls: List[str]) -> None:
        """
        Downloads the image (both base64 && url) and uploads them to the ChatGPT prompt-box.
        """
        original_window = self.driver.current_window_handle
        existing_windows = set(self.driver.window_handles)
        base64_pattern = r"^data:image/(png|jpeg|gif);base64,(.*)$"
        image_paths = []

        for i, url in enumerate(image_urls):
            image_path = f"images/image-{i}-{uuid.uuid4()}.png"
            if re.match(base64_pattern, url):
                image_base64_string = url.split(",")[1]
                base64_to_image(image_base64_string, output_file_path=image_path)
                image_paths.append(image_path)
            else:
                try:
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.get(url)
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "img"))
                    )
                    img_element = self.driver.find_element(By.TAG_NAME, "img")
                    img_element.screenshot(image_path)
                    image_paths.append(image_path)
                except Exception as e:
                    print(f"Error processing URL {url}: {str(e)}")
                finally:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

        new_windows = set(self.driver.window_handles) - existing_windows
        if new_windows:
            temp_window = new_windows.pop()
            self.driver.switch_to.window(temp_window)
            self.driver.close()
        self.driver.switch_to.window(original_window)
        input_form = self.driver.find_element(By.CSS_SELECTOR, "form[class='w-full']")

        for image in image_paths:
            input_form.find_element(By.CSS_SELECTOR, "input").send_keys(
                f"{os.path.abspath(str(image))}"
            )
            button = input_form.find_element(
                By.CSS_SELECTOR, "button[data-testid='send-button']"
            )
            start_time = time.time()
            while button.get_attribute("disabled") is not None:
                if time.time() - start_time > 5:
                    break
                button = input_form.find_element(
                    By.CSS_SELECTOR, "button[data-testid='send-button']"
                )

    def get_previous_chats(self, link=False) -> list:
        """
        Get a list of all previous chats from the sidebar.
        If link is True, returns a list of name & chat-link
        else returns a list of chat-name only.
        """
        self.__check_historytab()
        chats = []
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "nav[aria-label='Chat history'] ol")
            )
        )
        previousChats = self.driver.find_element(
            By.CSS_SELECTOR, "nav[aria-label='Chat history'] ol"
        )
        for chat in previousChats.find_elements(By.CSS_SELECTOR, "li"):
            chat_name = chat.find_element(By.CSS_SELECTOR, "div a div[dir='auto']").text
            chat_link = (chat.find_element(By.CSS_SELECTOR, "a")).get_attribute("href")
            chats.append([chat_name, chat_link])
        self.chats = chats
        if not link:
            return "\n".join(chatname[0] for chatname in chats)
        else:
            return chats

    def find_chat(self, name: str):
        """
        Finds the given chatname from the list of chatnames.
        If chat is found, opens it in a new tab and driver focus is
        shifted to that tab.
        """
        chat_received = False
        if self.chats == []:
            self.get_previouschats(link=True)
        for chat in self.chats:
            if chat[0] == name:
                print(f'chat "{name}" found!')
                chat_link = chat[1]
                print(f"chat link - {chat_link}")
                self.driver.switch_to.new_window("tab")
                self.driver.get(url=chat_link)
                time.sleep(5)
                chat_received = True
                break
        if not chat_received:
            raise Exception(f"Chat '{name}' not found in history")

    def delete_latest_chat(self):
        ActionChains(self.driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys(
            Keys.BACK_SPACE
        ).perform()
        time.sleep(2)
        dialog_box = self.driver.find_element(By.CSS_SELECTOR, "div[role='dialog']")
        dialog_box.find_element(By.CSS_SELECTOR, "button").click()

    def close_current_tab(self):
        """
        Close the tab in-focus and shift to previous tab.
        """

        if len(self.driver.window_handles) == 1:
            raise Exception("Only one Tab open, instead use close_currentWindow()")
        print(f"Closing  {self.driver.title} Tab")
        self.driver.close()

    def close_current_window(self):
        """
        Close the entire driver window.
        """

        self.driver.quit()
