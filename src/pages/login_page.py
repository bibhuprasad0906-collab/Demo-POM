"""
LoginPage: Page object for login functionality.
Implements robust error handling and exposes login operations.
"""

from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.utils.exceptions import LoginFailedError, ElementNotFoundError
import logging
import time

class LoginPage(BasePage):
    # Locators (update as per actual application)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    DASHBOARD_INDICATOR = (By.ID, "dashboard")
    LOCKED_MESSAGE = (By.ID, "lockedMsg")
    PASSWORD_TOGGLE = (By.ID, "togglePassword")

    def open(self, base_url):
        """
        Open the login page.
        """
        try:
            self.driver.get(base_url + "/login")
        except Exception as e:
            logging.error(f"Failed to open login page: {str(e)}")
            raise

    def login(self, username, password):
        """
        Perform login with given credentials.
        Returns True if dashboard is reached, False otherwise.
        Raises LoginFailedError on error.
        """
        try:
            self.send_keys(self.USERNAME_INPUT, username)
            self.send_keys(self.PASSWORD_INPUT, password)
            self.click(self.LOGIN_BUTTON)
            start_time = time.time()
            # Wait for dashboard or error
            if self.is_visible(self.DASHBOARD_INDICATOR):
                elapsed = time.time() - start_time
                if elapsed > 2:
                    logging.warning(f"Dashboard loaded in {elapsed:.2f}s, exceeds 2s requirement.")
                return True
            elif self.is_visible(self.ERROR_MESSAGE):
                return False
            elif self.is_visible(self.LOCKED_MESSAGE):
                raise LoginFailedError("Account is locked.")
            else:
                raise LoginFailedError("Unknown login failure.")
        except ElementNotFoundError as e:
            logging.error(f"Login failed: {str(e)}")
            raise LoginFailedError(str(e))
        except Exception as e:
            logging.error(f"Unexpected error during login: {str(e)}")
            raise LoginFailedError(str(e))

    def get_error_message(self):
        """
        Return error message text if present.
        """
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except ElementNotFoundError:
            return ""

    def get_locked_message(self):
        """
        Return locked account message text if present.
        """
        try:
            return self.get_text(self.LOCKED_MESSAGE)
        except ElementNotFoundError:
            return ""

    def toggle_password_visibility(self):
        """
        Toggle password visibility.
        Returns True if toggled successfully.
        """
        try:
            self.click(self.PASSWORD_TOGGLE)
            # Check if password input type changed
            element = self.find_element(self.PASSWORD_INPUT)
            input_type = element.get_attribute("type")
            return input_type in ["text", "password"]
        except Exception as e:
            logging.error(f"Failed to toggle password visibility: {str(e)}")
            return False
