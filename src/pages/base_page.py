"""
BasePage: Abstract base class for all page objects.
Provides safe Selenium wrappers with robust error handling and logging.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.exceptions import ElementNotFoundError
import logging

class BasePage:
    def __init__(self, driver, timeout=10):
        """
        :param driver: Selenium WebDriver instance
        :param timeout: Default timeout for element waits
        """
        self.driver = driver
        self.timeout = timeout

    def find_element(self, locator):
        """
        Safely find an element with error handling.
        :param locator: Tuple (By.<method>, locator_string)
        :return: WebElement
        :raises: ElementNotFoundError
        """
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            logging.error(f"Element not found: {locator} - {str(e)}")
            raise ElementNotFoundError(f"Element not found: {locator}")

    def click_element(self, locator):
        """
        Safely click an element.
        :param locator: Tuple (By.<method>, locator_string)
        """
        try:
            element = self.find_element(locator)
            element.click()
        except Exception as e:
            logging.error(f"Failed to click element: {locator} - {str(e)}")
            raise ElementNotFoundError(f"Failed to click element: {locator}")

    def enter_text(self, locator, text):
        """
        Safely enter text into an input field.
        :param locator: Tuple (By.<method>, locator_string)
        :param text: Text to enter
        """
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            logging.error(f"Failed to enter text: {locator} - {str(e)}")
            raise ElementNotFoundError(f"Failed to enter text: {locator}")