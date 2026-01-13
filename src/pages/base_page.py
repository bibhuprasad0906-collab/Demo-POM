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
        Initialize with WebDriver and default timeout.
        """
        self.driver = driver
        self.timeout = timeout

    def find_element(self, by, value):
        """
        Safely find element with error handling.
        """
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception as e:
            logging.error(f"Element not found: {by}={value} - {str(e)}")
            raise ElementNotFoundError(f"Element not found: {by}={value}")

    def click(self, by, value):
        """
        Safely click element.
        """
        try:
            elem = self.find_element(by, value)
            elem.click()
        except Exception as e:
            logging.error(f"Click failed: {by}={value} - {str(e)}")
            raise ElementNotFoundError(f"Click failed: {by}={value}")

    def send_keys(self, by, value, keys):
        """
        Safely send keys to element.
        """
        try:
            elem = self.find_element(by, value)
            elem.clear()
            elem.send_keys(keys)
        except Exception as e:
            logging.error(f"Send keys failed: {by}={value} - {str(e)}")
            raise ElementNotFoundError(f"Send keys failed: {by}={value}")

    def is_visible(self, by, value):
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

    def get_text(self, by, value):
        """
        Get text from element.
        """
        try:
            elem = self.find_element(by, value)
            return elem.text
        except Exception as e:
            logging.error(f"Get text failed: {by}={value} - {str(e)}")
            raise ElementNotFoundError(f"Get text failed: {by}={value}")