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

    def find_element(self, locator):
        """
        Safely find element by locator.
        Raises ElementNotFoundError if not found.
        """
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            self.logger.error(f"Element not found: {locator} - {str(e)}")
            raise ElementNotFoundError(f"Element not found: {locator}")

    def click_element(self, locator):
        """
        Safely click element.
        """
        try:
            element = self.find_element(locator)
            element.click()
        except Exception as e:
            self.logger.error(f"Click failed for {locator}: {str(e)}")
            raise

    def enter_text(self, locator, text):
        """
        Safely enter text into element.
        """
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f"Text entry failed for {locator}: {str(e)}")
            raise

    def is_element_visible(self, locator):
        """
        Check if element is visible.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def get_element_text(self, locator):
        """
        Get text from element.
        """
        try:
            element = self.find_element(locator)
            return element.text
        except Exception as e:
            self.logger.error(f"Get text failed for {locator}: {str(e)}")
            raise