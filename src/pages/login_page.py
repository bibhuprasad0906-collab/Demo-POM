"""
LoginPage: Page object for login functionality.
Implements robust error handling and all login-related UI operations.
"""

from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.utils.exceptions import LoginFailedError, ElementNotFoundError
import logging
import time

class LoginPage(BasePage):
    # Locators (update as per actual UI)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    DASHBOARD = (By.ID, "dashboard")
    LOCKED_MESSAGE = (By.ID, "lockedMsg")
    PASSWORD_TOGGLE = (By.ID, "passwordToggle")

    def open(self, base_url):
        """
        Open login page.
        """
        try:
            self.driver.get(base_url)
        except Exception as e:
            logging.error(f"Failed to open login page: {str(e)}")
            raise

    def login(self, username, password):
        """
        Perform login action.
        Returns True if dashboard is visible, False otherwise.
        """
        try:
            self.send_keys(*self.USERNAME_INPUT, username)
            self.send_keys(*self.PASSWORD_INPUT, password)
            start_time = time.time()
            self.click(*self.LOGIN_BUTTON)
            # Wait for dashboard or error
            if self.is_visible(*self.DASHBOARD):
                elapsed = time.time() - start_time
                if elapsed > 2:
                    logging.warning(f"Dashboard loaded in {elapsed:.2f}s, exceeds 2s SLA")
                return True
            elif self.is_visible(*self.ERROR_MESSAGE):
                return False
            elif self.is_visible(*self.LOCKED_MESSAGE):
                raise LoginFailedError("Account is locked")
            else:
                raise LoginFailedError("Unknown login failure")
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            raise LoginFailedError(str(e))

    def get_error_message(self):
        """
        Get error message text.
        """
        try:
            return self.get_text(*self.ERROR_MESSAGE)
        except ElementNotFoundError:
            return ""

    def get_locked_message(self):
        """
        Get locked message text.
        """
        try:
            return self.get_text(*self.LOCKED_MESSAGE)
        except ElementNotFoundError:
            return ""

    def toggle_password_visibility(self):
        """
        Toggle password visibility.
        Returns True if password is shown, False if masked.
        """
        try:
            self.click(*self.PASSWORD_TOGGLE)
            # Check input type
            elem = self.find_element(*self.PASSWORD_INPUT)
            input_type = elem.get_attribute("type")
            return input_type == "text"
        except Exception as e:
            logging.error(f"Password toggle failed: {str(e)}")
            raise ElementNotFoundError("Password toggle failed")

    def is_password_masked(self):
        """
        Check if password is masked.
        """
        try:
            elem = self.find_element(*self.PASSWORD_INPUT)
            return elem.get_attribute("type") == "password"
        except Exception as e:
            logging.error(f"Check password mask failed: {str(e)}")
            raise ElementNotFoundError("Check password mask failed")