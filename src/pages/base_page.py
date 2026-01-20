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
        self.logger = logging.getLogger(self.__class__.__name__)

    def find_element(self, by, value):
        """
        Safely find an element, raising ElementNotFoundError if not found.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            self.logger.error(f"Element not found: {by}={value} | {str(e)}")
            raise ElementNotFoundError(f"Element not found: {by}={value}")

    def click_element(self, by, value):
        """
        Safely click an element.
        """
        try:
            element = self.find_element(by, value)
            element.click()
        except Exception as e:
            self.logger.error(f"Failed to click element: {by}={value} | {str(e)}")
            raise

    def enter_text(self, by, value, text):
        """
        Safely enter text into an element.
        """
        try:
            element = self.find_element(by, value)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f"Failed to enter text: {by}={value} | {str(e)}")
            raise

    def is_element_present(self, by, value, timeout=None):
        """
        Check if element is present within timeout.
        """
        try:
            wait_time = timeout if timeout else self.timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except:
            return False

    def get_text(self, by, value):
        """
        Get text from an element.
        """
        try:
            element = self.find_element(by, value)
            return element.text
        except Exception as e:
            self.logger.error(f"Failed to get text: {by}={value} | {str(e)}")
            raise

    def get_attribute(self, by, value, attribute):
        """
        Get attribute value from an element.
        """
        try:
            element = self.find_element(by, value)
            return element.get_attribute(attribute)
        except Exception as e:
            self.logger.error(f"Failed to get attribute: {by}={value} | {str(e)}")
            raise