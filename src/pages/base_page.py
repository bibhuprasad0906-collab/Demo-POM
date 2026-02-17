"""BasePage: Abstract base class for all page objects.
Provides safe Selenium wrappers with robust error handling and logging."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from src.utils.exceptions import ElementNotFoundError
import logging


class BasePage:
    """Base page object providing safe Selenium operations."""

    def __init__(self, driver):
        """Initialize with Selenium WebDriver.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator, timeout=10):
        """Safely find element by locator tuple (By, value).
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement if found
            
        Raises:
            ElementNotFoundError: If element not found within timeout
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Element not found: {locator}")
            raise ElementNotFoundError(f"Element not found: {locator}") from e

    def click_element(self, locator, timeout=10):
        """Safely click element.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
            
        Raises:
            ElementNotFoundError: If element not found or not clickable
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicked element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click element: {locator}")
            raise ElementNotFoundError(f"Failed to click element: {locator}") from e

    def enter_text(self, locator, text, timeout=10):
        """Safely enter text into element.
        
        Args:
            locator: Tuple of (By, value)
            text: Text to enter
            timeout: Maximum wait time in seconds
            
        Raises:
            ElementNotFoundError: If element not found
        """
        try:
            element = self.find_element(locator, timeout)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Entered text in element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to enter text in element: {locator}")
            raise ElementNotFoundError(f"Failed to enter text in element: {locator}") from e

    def is_element_visible(self, locator, timeout=10):
        """Check if element is visible.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
            
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def get_element_text(self, locator, timeout=10):
        """Get text from element.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
            
        Returns:
            str: Element text
            
        Raises:
            ElementNotFoundError: If element not found
        """
        try:
            element = self.find_element(locator, timeout)
            return element.text
        except Exception as e:
            self.logger.error(f"Failed to get text from element: {locator}")
            raise ElementNotFoundError(f"Failed to get text from element: {locator}") from e

    def get_element_attribute(self, locator, attribute, timeout=10):
        """Get attribute value from element.
        
        Args:
            locator: Tuple of (By, value)
            attribute: Attribute name
            timeout: Maximum wait time in seconds
            
        Returns:
            str: Attribute value
            
        Raises:
            ElementNotFoundError: If element not found
        """
        try:
            element = self.find_element(locator, timeout)
            return element.get_attribute(attribute)
        except Exception as e:
            self.logger.error(f"Failed to get attribute '{attribute}' from element: {locator}")
            raise ElementNotFoundError(f"Failed to get attribute from element: {locator}") from e