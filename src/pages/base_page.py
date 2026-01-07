"""
BasePage: Abstract base class for all page objects.
Provides safe Selenium wrappers and robust error handling.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.exceptions import ElementNotFoundError
import logging

class BasePage:
    def __init__(self, driver, timeout=10):
        """
        Initialize BasePage with driver and default timeout.
        """
        self.driver = driver
        self.timeout = timeout

    def find_element(self, locator):
        """
        Safely find a single element.
        Raises ElementNotFoundError if not found.
        """
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            logging.error(f"Element not found: {locator} - {str(e)}")
            raise ElementNotFoundError(f"Element not found: {locator}")

    def click(self, locator):
        """
        Safely click an element.
        """
        try:
            element = self.find_element(locator)
            element.click()
        except Exception as e:
            logging.error(f"Failed to click element: {locator} - {str(e)}")
            raise ElementNotFoundError(f"Failed to click element: {locator}")

    def send_keys(self, locator, value):
        """
        Safely send keys to an element.
        """
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(value)
        except Exception as e:
            logging.error(f"Failed to send keys to element: {locator} - {str(e)}")
            raise ElementNotFoundError(f"Failed to send keys to element: {locator}")

    def is_visible(self, locator):
        """
        Check if element is visible.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except Exception as e:
            logging.error(f"Element not visible: {locator} - {str(e)}")
            return False

    def get_text(self, locator):
        """
        Get text from an element.
        """
        try:
            element = self.find_element(locator)
            return element.text
        except Exception as e:
            logging.error(f"Failed to get text from element: {locator} - {str(e)}")
            raise ElementNotFoundError(f"Failed to get text from element: {locator}")
