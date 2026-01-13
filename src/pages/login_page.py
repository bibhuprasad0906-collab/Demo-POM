"""
LoginPage: Page object for login functionality.
Handles login, error messages, password visibility toggle, and lockout checks.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.base_page import BasePage
from src.utils.exceptions import LoginFailedError, ElementNotFoundError
import logging
import time

class LoginPage(BasePage):
    """
    Page object for login page interactions.
    Implements all login-related operations with robust error handling.
    """
    
    # Locators - Update these based on actual application UI
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    DASHBOARD = (By.ID, "dashboard")
    LOCKOUT_MESSAGE = (By.ID, "lockoutMsg")
    PASSWORD_TOGGLE = (By.ID, "passwordToggle")
    
    # Alternative locators (fallback if IDs change)
    USERNAME_INPUT_ALT = (By.NAME, "username")
    PASSWORD_INPUT_ALT = (By.NAME, "password")
    LOGIN_BUTTON_ALT = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE_ALT = (By.CLASS_NAME, "error-message")
    DASHBOARD_ALT = (By.CLASS_NAME, "dashboard")
    LOCKOUT_MESSAGE_ALT = (By.CLASS_NAME, "lockout-message")

    def __init__(self, driver):
        """
        Initialize LoginPage with WebDriver.
        
        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)

    def open(self, base_url):
        """
        Navigate to the login page.
        
        Args:
            base_url: Base URL of the application
        """
        try:
            login_url = f"{base_url}/login" if not base_url.endswith('/') else f"{base_url}login"
            self.driver.get(login_url)
            logging.info(f"Opened login page: {login_url}")
            # Wait for page to load
            self.wait_for_page_load()
        except Exception as e:
            logging.error(f"Failed to open login page: {str(e)}")
            raise

    def wait_for_page_load(self, timeout=10):
        """
        Wait for login page to fully load.
        
        Args:
            timeout: Maximum wait time in seconds
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
            wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
            wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
            logging.info("Login page loaded successfully")
        except Exception as e:
            logging.error(f"Login page did not load properly: {str(e)}")
            raise

    def enter_username(self, username):
        """
        Enter username in the username field.
        
        Args:
            username: Username to enter
        """
        try:
            self.enter_text(self.USERNAME_INPUT, username)
            logging.info("Username entered successfully")
        except ElementNotFoundError:
            # Try alternative locator
            self.enter_text(self.USERNAME_INPUT_ALT, username)
            logging.info("Username entered using alternative locator")

    def enter_password(self, password):
        """
        Enter password in the password field.
        
        Args:
            password: Password to enter (not logged for security)
        """
        try:
            self.enter_text(self.PASSWORD_INPUT, password)
            logging.info("Password entered successfully")
        except ElementNotFoundError:
            # Try alternative locator
            self.enter_text(self.PASSWORD_INPUT_ALT, password)
            logging.info("Password entered using alternative locator")

    def click_login_button(self):
        """
        Click the login button.
        """
        try:
            self.click(self.LOGIN_BUTTON)
            logging.info("Login button clicked")
        except ElementNotFoundError:
            # Try alternative locator
            self.click(self.LOGIN_BUTTON_ALT)
            logging.info("Login button clicked using alternative locator")

    def login(self, username, password, expect_success=True, timeout=2):
        """
        Perform complete login operation and verify outcome.
        
        Args:
            username: Username to login with
            password: Password to login with
            expect_success: Whether login is expected to succeed
            timeout: Maximum wait time for outcome verification
            
        Returns:
            True if login succeeded as expected, False otherwise
            
        Raises:
            LoginFailedError: If login outcome doesn't match expectation
        """
        try:
            # Enter credentials
            self.enter_username(username)
            self.enter_password(password)
            
            # Click login
            self.click_login_button()
            
            # Wait for outcome
            start_time = time.time()
            
            if expect_success:
                # Wait for dashboard to appear
                while time.time() - start_time < timeout:
                    if self.is_dashboard_visible():
                        logging.info("Login successful - dashboard visible")
                        return True
                    time.sleep(0.2)
                
                # Dashboard not visible within timeout
                logging.error("Dashboard not visible after login")
                self.take_screenshot("screenshots/login_failed.png")
                raise LoginFailedError("Dashboard not visible after login")
            else:
                # Wait for error message to appear
                while time.time() - start_time < timeout:
                    if self.is_error_message_visible() or self.is_lockout_message_visible():
                        logging.info("Login failed as expected - error/lockout message visible")
                        return False
                    time.sleep(0.2)
                
                # No error message visible
                logging.error("Error message not visible after failed login")
                self.take_screenshot("screenshots/error_not_shown.png")
                raise LoginFailedError("Error message not visible after failed login")
                
        except LoginFailedError:
            raise
        except Exception as e:
            logging.error(f"Login operation failed: {str(e)}")
            self.take_screenshot("screenshots/login_exception.png")
            raise LoginFailedError(f"Login operation failed: {str(e)}") from e

    def is_dashboard_visible(self):
        """
        Check if dashboard is visible after login.
        
        Returns:
            True if dashboard is visible, False otherwise
        """
        try:
            return self.is_visible(self.DASHBOARD, timeout=1)
        except:
            try:
                return self.is_visible(self.DASHBOARD_ALT, timeout=1)
            except:
                return False

    def is_error_message_visible(self):
        """
        Check if error message is visible.
        
        Returns:
            True if error message is visible, False otherwise
        """
        try:
            return self.is_visible(self.ERROR_MESSAGE, timeout=1)
        except:
            try:
                return self.is_visible(self.ERROR_MESSAGE_ALT, timeout=1)
            except:
                return False

    def is_lockout_message_visible(self):
        """
        Check if lockout message is visible.
        
        Returns:
            True if lockout message is visible, False otherwise
        """
        try:
            return self.is_visible(self.LOCKOUT_MESSAGE, timeout=1)
        except:
            try:
                return self.is_visible(self.LOCKOUT_MESSAGE_ALT, timeout=1)
            except:
                return False

    def get_error_message(self):
        """
        Get the text of the error message.
        
        Returns:
            Error message text, or empty string if not found
        """
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except:
            try:
                return self.get_text(self.ERROR_MESSAGE_ALT)
            except:
                logging.warning("Error message element not found")
                return ""

    def get_lockout_message(self):
        """
        Get the text of the lockout message.
        
        Returns:
            Lockout message text, or empty string if not found
        """
        try:
            return self.get_text(self.LOCKOUT_MESSAGE)
        except:
            try:
                return self.get_text(self.LOCKOUT_MESSAGE_ALT)
            except:
                logging.warning("Lockout message element not found")
                return ""

    def toggle_password_visibility(self):
        """
        Toggle password visibility (show/hide password).
        """
        try:
            self.click(self.PASSWORD_TOGGLE)
            logging.info("Password visibility toggled")
        except Exception as e:
            logging.error(f"Failed to toggle password visibility: {str(e)}")
            raise

    def is_password_visible(self):
        """
        Check if password is currently visible (type='text').
        
        Returns:
            True if password is visible (type='text'), False if hidden (type='password')
        """
        try:
            password_type = self.get_attribute(self.PASSWORD_INPUT, "type")
            return password_type == "text"
        except:
            try:
                password_type = self.get_attribute(self.PASSWORD_INPUT_ALT, "type")
                return password_type == "text"
            except Exception as e:
                logging.error(f"Failed to check password visibility: {str(e)}")
                raise

    def attempt_multiple_failed_logins(self, username, password, attempts=5):
        """
        Attempt multiple failed logins to trigger account lockout.
        
        Args:
            username: Username to use
            password: Invalid password to use
            attempts: Number of failed attempts
        """
        logging.info(f"Attempting {attempts} failed logins for user: {username}")
        for i in range(attempts):
            try:
                self.enter_username(username)
                self.enter_password(password)
                self.click_login_button()
                time.sleep(0.5)  # Brief pause between attempts
                logging.info(f"Failed login attempt {i+1}/{attempts}")
            except Exception as e:
                logging.error(f"Error during failed login attempt {i+1}: {str(e)}")
                
        # Wait for lockout message
        time.sleep(1)