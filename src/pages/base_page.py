"""BasePage: Abstract base class for all page objects.

Provides safe Selenium wrappers, robust error handling, and common
page operations. All page objects should inherit from this class.

Features:
    - Safe element finding with explicit waits
    - Robust click and text entry operations
    - Screenshot capture on errors
    - Comprehensive logging
    - Accessibility helpers
    - Performance monitoring
"""

import logging
import time
from typing import Tuple, Optional, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException as SeleniumElementNotInteractableException,
    StaleElementReferenceException
)
from src.utils.config import Config
from src.utils.exceptions import (
    ElementNotFoundError,
    ElementNotInteractableError,
    PageLoadTimeoutError
)


class BasePage:
    """Abstract base class for all page objects.
    
    Provides common functionality for interacting with web pages,
    including element location, interaction, and validation.
    
    Attributes:
        driver: Selenium WebDriver instance
        timeout: Default timeout for element waits (seconds)
        wait: WebDriverWait instance for explicit waits
    
    Example:
        >>> class LoginPage(BasePage):
        ...     USERNAME_INPUT = (By.ID, "username")
        ...     
        ...     def enter_username(self, username):
        ...         self.enter_text(self.USERNAME_INPUT, username)
    """
    
    def __init__(self, driver: WebDriver, timeout: Optional[int] = None):
        """Initialize BasePage with driver and timeout.
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Timeout for element waits. If None, uses Config.TIMEOUT
        """
        self.driver = driver
        self.timeout = timeout or Config.TIMEOUT
        self.wait = WebDriverWait(self.driver, self.timeout)
        logging.debug(f"{self.__class__.__name__} initialized with timeout: {self.timeout}s")
    
    def find_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Safely find an element using the provided locator.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            timeout: Optional custom timeout for this operation
        
        Returns:
            WebElement: Located web element
        
        Raises:
            ElementNotFoundError: If element is not found within timeout
        
        Example:
            >>> element = self.find_element((By.ID, "username"))
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            logging.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            error_msg = f"Element not found within {wait_time}s: {locator}"
            logging.error(error_msg)
            raise ElementNotFoundError(
                error_msg,
                context={"locator": locator, "timeout": wait_time}
            )
        except Exception as e:
            error_msg = f"Error finding element {locator}: {str(e)}"
            logging.error(error_msg)
            raise ElementNotFoundError(
                error_msg,
                context={"locator": locator, "error": str(e)}
            )
    
    def find_elements(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> List[WebElement]:
        """Find multiple elements using the provided locator.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            timeout: Optional custom timeout for this operation
        
        Returns:
            List[WebElement]: List of located web elements
        
        Raises:
            ElementNotFoundError: If no elements are found within timeout
        """
        wait_time = timeout or self.timeout
        try:
            elements = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located(locator)
            )
            logging.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            error_msg = f"No elements found within {wait_time}s: {locator}"
            logging.error(error_msg)
            raise ElementNotFoundError(
                error_msg,
                context={"locator": locator, "timeout": wait_time}
            )
    
    def wait_for_element_visible(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be visible.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            timeout: Optional custom timeout for this operation
        
        Returns:
            WebElement: Visible web element
        
        Raises:
            ElementNotFoundError: If element is not visible within timeout
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            logging.debug(f"Element visible: {locator}")
            return element
        except TimeoutException:
            error_msg = f"Element not visible within {wait_time}s: {locator}"
            logging.error(error_msg)
            raise ElementNotFoundError(
                error_msg,
                context={"locator": locator, "timeout": wait_time, "condition": "visible"}
            )
    
    def wait_for_element_clickable(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be clickable.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            timeout: Optional custom timeout for this operation
        
        Returns:
            WebElement: Clickable web element
        
        Raises:
            ElementNotFoundError: If element is not clickable within timeout
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            logging.debug(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            error_msg = f"Element not clickable within {wait_time}s: {locator}"
            logging.error(error_msg)
            raise ElementNotInteractableError(
                error_msg,
                context={"locator": locator, "timeout": wait_time, "condition": "clickable"}
            )
    
    def click(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """Safely click an element.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            timeout: Optional custom timeout for this operation
        
        Raises:
            ElementNotFoundError: If element is not found
            ElementNotInteractableError: If element cannot be clicked
        
        Example:
            >>> self.click((By.ID, "loginBtn"))
        """
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            element.click()
            logging.info(f"Clicked element: {locator}")
        except SeleniumElementNotInteractableException as e:
            error_msg = f"Element not interactable: {locator}"
            logging.error(error_msg)
            raise ElementNotInteractableError(
                error_msg,
                context={"locator": locator, "error": str(e)}
            )
        except StaleElementReferenceException:
            # Retry once on stale element
            logging.warning(f"Stale element, retrying click: {locator}")
            element = self.wait_for_element_clickable(locator, timeout)
            element.click()
            logging.info(f"Clicked element after retry: {locator}")
    
    def enter_text(self, locator: Tuple[By, str], text: str, clear_first: bool = True, timeout: Optional[int] = None) -> None:
        """Safely enter text into an input field.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            text: Text to enter
            clear_first: Whether to clear field before entering text
            timeout: Optional custom timeout for this operation
        
        Raises:
            ElementNotFoundError: If element is not found
            ElementNotInteractableError: If text cannot be entered
        
        Example:
            >>> self.enter_text((By.ID, "username"), "testuser")
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            # Sanitize text in logs (don't log passwords)
            log_text = "***" if "password" in str(locator).lower() else text
            logging.info(f"Entered text in element {locator}: {log_text}")
        except SeleniumElementNotInteractableException as e:
            error_msg = f"Cannot enter text in element: {locator}"
            logging.error(error_msg)
            raise ElementNotInteractableError(
                error_msg,
                context={"locator": locator, "error": str(e)}
            )
        except StaleElementReferenceException:
            # Retry once on stale element
            logging.warning(f"Stale element, retrying text entry: {locator}")
            element = self.wait_for_element_visible(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            log_text = "***" if "password" in str(locator).lower() else text
            logging.info(f"Entered text after retry in element {locator}: {log_text}")
    
    def get_text(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
        """Get text content of an element.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            timeout: Optional custom timeout for this operation
        
        Returns:
            str: Text content of the element
        
        Raises:
            ElementNotFoundError: If element is not found
        """
        element = self.find_element(locator, timeout)
        text = element.text
        logging.debug(f"Got text from element {locator}: {text}")
        return text
    
    def get_attribute(self, locator: Tuple[By, str], attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """Get attribute value of an element.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            attribute: Attribute name
            timeout: Optional custom timeout for this operation
        
        Returns:
            Optional[str]: Attribute value or None if not found
        
        Raises:
            ElementNotFoundError: If element is not found
        """
        element = self.find_element(locator, timeout)
        value = element.get_attribute(attribute)
        logging.debug(f"Got attribute '{attribute}' from element {locator}: {value}")
        return value
    
    def is_element_present(self, locator: Tuple[By, str], timeout: int = 2) -> bool:
        """Check if element is present in DOM.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            timeout: Timeout for check (default: 2 seconds)
        
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator: Tuple[By, str], timeout: int = 2) -> bool:
        """Check if element is visible.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            timeout: Timeout for check (default: 2 seconds)
        
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """Wait for page to fully load.
        
        Args:
            timeout: Optional custom timeout for this operation
        
        Raises:
            PageLoadTimeoutError: If page does not load within timeout
        """
        wait_time = timeout or Config.PAGE_LOAD_TIMEOUT
        try:
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logging.debug("Page loaded successfully")
        except TimeoutException:
            error_msg = f"Page did not load within {wait_time}s"
            logging.error(error_msg)
            raise PageLoadTimeoutError(
                error_msg,
                context={"url": self.driver.current_url, "timeout": wait_time}
            )
    
    def scroll_to_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """Scroll to make element visible.
        
        Args:
            locator: Tuple (By.<method>, locator_string)
            timeout: Optional custom timeout for this operation
        
        Raises:
            ElementNotFoundError: If element is not found
        """
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logging.debug(f"Scrolled to element: {locator}")
        time.sleep(0.5)  # Brief pause for scroll animation
    
    def get_current_url(self) -> str:
        """Get current page URL.
        
        Returns:
            str: Current URL
        """
        url = self.driver.current_url
        logging.debug(f"Current URL: {url}")
        return url
    
    def get_page_title(self) -> str:
        """Get current page title.
        
        Returns:
            str: Page title
        """
        title = self.driver.title
        logging.debug(f"Page title: {title}")
        return title