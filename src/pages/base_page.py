"""
BasePage: Abstract base class for all page objects.
Provides safe Selenium wrappers and robust error handling.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    StaleElementReferenceException
)
from src.utils.exceptions import ElementNotFoundError
import logging
import time

class BasePage:
    """
    Base page object class providing common Selenium operations.
    All page objects should inherit from this class.
    """

    def __init__(self, driver):
        """
        Initialize with Selenium WebDriver.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator, timeout=10):
        """
        Safely find an element with explicit wait.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement if found
            
        Raises:
            ElementNotFoundError: If element is not found within timeout
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except NoSuchElementException as e:
            logging.error(f"Element not found: {locator}")
            raise ElementNotFoundError(f"Element not found: {locator}") from e
        except TimeoutException as e:
            logging.error(f"Timeout finding element: {locator}")
            raise ElementNotFoundError(f"Timeout finding element: {locator}") from e
        except WebDriverException as e:
            logging.error(f"WebDriver error: {str(e)}")
            raise

    def find_elements(self, locator, timeout=10):
        """
        Safely find multiple elements with explicit wait.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
            
        Returns:
            List of WebElements
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except (NoSuchElementException, TimeoutException) as e:
            logging.warning(f"Elements not found: {locator}")
            return []

    def click(self, locator, timeout=10):
        """
        Safely click an element with retry logic.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
        """
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                wait = WebDriverWait(self.driver, timeout)
                element = wait.until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if attempt == max_attempts - 1:
                    logging.error(f"Failed to click element after {max_attempts} attempts: {locator}")
                    raise
                time.sleep(0.5)
            except Exception as e:
                logging.error(f"Failed to click element: {locator}")
                raise

    def enter_text(self, locator, text, timeout=10):
        """
        Safely enter text into an input field.
        
        Args:
            locator: Tuple of (By, value)
            text: Text to enter
            timeout: Maximum wait time in seconds
        """
        try:
            element = self.find_element(locator, timeout)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            logging.error(f"Failed to enter text in element: {locator}")
            raise

    def get_text(self, locator, timeout=10):
        """
        Get text from an element.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
            
        Returns:
            Text content of the element
        """
        try:
            element = self.find_element(locator, timeout)
            return element.text
        except Exception as e:
            logging.error(f"Failed to get text from element: {locator}")
            raise

    def is_visible(self, locator, timeout=10):
        """
        Check if element is visible.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
            
        Returns:
            True if visible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def is_present(self, locator, timeout=10):
        """
        Check if element is present in DOM.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
            
        Returns:
            True if present, False otherwise
        """
        try:
            self.find_element(locator, timeout)
            return True
        except ElementNotFoundError:
            return False

    def wait_for_element_to_disappear(self, locator, timeout=10):
        """
        Wait for an element to disappear from the page.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            logging.warning(f"Element did not disappear: {locator}")

    def get_attribute(self, locator, attribute, timeout=10):
        """
        Get attribute value from an element.
        
        Args:
            locator: Tuple of (By, value)
            attribute: Attribute name
            timeout: Maximum wait time in seconds
            
        Returns:
            Attribute value
        """
        try:
            element = self.find_element(locator, timeout)
            return element.get_attribute(attribute)
        except Exception as e:
            logging.error(f"Failed to get attribute {attribute} from element: {locator}")
            raise

    def scroll_to_element(self, locator, timeout=10):
        """
        Scroll to an element.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum wait time in seconds
        """
        try:
            element = self.find_element(locator, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Allow time for scroll animation
        except Exception as e:
            logging.error(f"Failed to scroll to element: {locator}")
            raise

    def take_screenshot(self, filename):
        """
        Take a screenshot and save to file.
        
        Args:
            filename: Path to save screenshot
        """
        try:
            self.driver.save_screenshot(filename)
            logging.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logging.error(f"Failed to take screenshot: {str(e)}")

    def get_current_url(self):
        """
        Get current page URL.
        
        Returns:
            Current URL as string
        """
        return self.driver.current_url

    def get_page_title(self):
        """
        Get current page title.
        
        Returns:
            Page title as string
        """
        return self.driver.title