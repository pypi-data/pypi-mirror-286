from selenium.common.exceptions import NoSuchElementException


def find_locator(driver, locators, wait=False):
    for locator in locators:
        try:
            element = driver.find_element(locator["By"], locator["value"])
            return element
        except NoSuchElementException:
            pass


def ask_yes_no(question: str):
    answer = input(f"{question} (y/n): ").strip().lower()
    while True:
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            answer = input("Invalid input. Please enter 'y' or 'n'.")
