"""LoginPage: Page Object for login functionality.
Implements robust error handling for login, password toggle, and error messages."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.base_page import BasePage
from src.utils.exceptions import LoginFailedError, ElementNotFoundError
import time
import logging


class LoginPage(BasePage):
    """Page object for login page with comprehensive error handling."""

    # Locators - Update these based on actual application UI
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    LOCKOUT_MESSAGE = (By.ID, "lockoutMsg")
    DASHBOARD = (By.ID, "dashboard")
    PASSWORD_TOGGLE = (By.ID, "passwordToggle")

    def __init__(self, driver):
        """Initialize LoginPage with WebDriver.
        
        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.logger = logging.getLogger(self.__class__.__name__)

    def open(self, base_url):
        """Open login page.
        
        Args:
            base_url: Base URL of the application
        """
        try:
            self.driver.get(base_url)
            self.logger.info(f"Opened login page: {base_url}")
        except Exception as e:
            self.logger.error(f"Failed to open login page: {base_url}")
            raise

    def login(self, username, password):
        """Perform login with comprehensive error handling.
        
        Args:
            username: Username for login
            password: Password for login
            
        Returns:
            bool: True if login successful and dashboard visible
            
        Raises:
            LoginFailedError: If login fails due to invalid credentials or account lockout
        """
        try:
            self.logger.info(f"Attempting login for user: {username}")
            
            # Enter credentials
            self.enter_text(self.USERNAME_INPUT, username)
            self.enter_text(self.PASSWORD_INPUT, password)
            
            # Click login button
            self.click_element(self.LOGIN_BUTTON)
            
            # Wait for response (dashboard, error, or lockout)
            start_time = time.time()
            timeout = 5  # 5 seconds timeout for login response
            
            while time.time() - start_time < timeout:
                # Check for successful login (dashboard visible)
                if self.is_element_visible(self.DASHBOARD, timeout=1):
                    self.logger.info(f"Login successful for user: {username}")
                    return True
                
                # Check for error message
                if self.is_element_visible(self.ERROR_MESSAGE, timeout=1):
                    error_msg = self.get_element_text(self.ERROR_MESSAGE)
                    self.logger.error(f"Login failed: {error_msg}")
                    raise LoginFailedError(f"Invalid credentials: {error_msg}")
                
                # Check for lockout message
                if self.is_element_visible(self.LOCKOUT_MESSAGE, timeout=1):
                    lockout_msg = self.get_element_text(self.LOCKOUT_MESSAGE)
                    self.logger.error(f"Account locked: {lockout_msg}")
                    raise LoginFailedError(f"Account locked: {lockout_msg}")
                
                time.sleep(0.2)
            
            # Timeout - no response received
            self.logger.error("Login response timeout")
            raise LoginFailedError("Login response timeout - no dashboard, error, or lockout message")
            
        except LoginFailedError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during login: {str(e)}")
            raise LoginFailedError(f"Login failed with unexpected error: {str(e)}") from e

    def get_error_message(self):
        """Return error message text if visible.
        
        Returns:
            str: Error message text, or None if not visible
        """
        try:
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=2):
                return self.get_element_text(self.ERROR_MESSAGE)
            return None
        except ElementNotFoundError:
            return None

    def get_lockout_message(self):
        """Return lockout message text if visible.
        
        Returns:
            str: Lockout message text, or None if not visible
        """
        try:
            if self.is_element_visible(self.LOCKOUT_MESSAGE, timeout=2):
                return self.get_element_text(self.LOCKOUT_MESSAGE)
            return None
        except ElementNotFoundError:
            return None

    def toggle_password_visibility(self):
        """Toggle password visibility and return input type.
        
        Returns:
            str: Password input type after toggle ('text' or 'password')
            
        Raises:
            ElementNotFoundError: If toggle button or password input not found
        """
        try:
            self.logger.info("Toggling password visibility")
            self.click_element(self.PASSWORD_TOGGLE)
            input_type = self.get_element_attribute(self.PASSWORD_INPUT, "type")
            self.logger.info(f"Password input type after toggle: {input_type}")
            return input_type
        except Exception as e:
            self.logger.error("Failed to toggle password visibility")
            raise ElementNotFoundError("Failed to toggle password visibility") from e

    def is_dashboard_visible(self):
        """Check if dashboard is visible after login.
        
        Returns:
            bool: True if dashboard visible, False otherwise
        """
        return self.is_element_visible(self.DASHBOARD, timeout=2)

    def is_error_displayed(self):
        """Check if error message is displayed.
        
        Returns:
            bool: True if error message visible, False otherwise
        """
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=2)

    def is_lockout_displayed(self):
        """Check if lockout message is displayed.
        
        Returns:
            bool: True if lockout message visible, False otherwise
        """
        return self.is_element_visible(self.LOCKOUT_MESSAGE, timeout=2)