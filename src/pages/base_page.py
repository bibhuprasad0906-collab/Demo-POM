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
        Initialize with Selenium WebDriver and default timeout.
        """
        self.driver = driver
        self.timeout = timeout

    def find_element(self, by, value):
        """
        Safely find a single element.
        Raises ElementNotFoundError if not found.
        """
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception as e:
            logging.error(f"Element not found: {by}={value} | {str(e)}")
            raise ElementNotFoundError(f"Element not found: {by}={value}")

    def click_element(self, by, value):
        """
        Safely click an element.
        """
        try:
            elem = self.find_element(by, value)
            elem.click()
        except Exception as e:
            logging.error(f"Failed to click element: {by}={value} | {str(e)}")
            raise ElementNotFoundError(f"Failed to click element: {by}={value}")

    def enter_text(self, by, value, text):
        """
        Safely enter text into an input field.
        """
        try:
            elem = self.find_element(by, value)
            elem.clear()
            elem.send_keys(text)
        except Exception as e:
            logging.error(f"Failed to enter text: {by}={value} | {str(e)}")
            raise ElementNotFoundError(f"Failed to enter text: {by}={value}")

    def is_element_visible(self, by, value):
        """
        Check if element is visible.
        """
        try:
            elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except Exception:
            return False