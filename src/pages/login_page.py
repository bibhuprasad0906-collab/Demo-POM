"""
LoginPage: Page object for login functionality.
Implements login, error handling, password toggle, and accessibility checks.
"""

from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.utils.exceptions import LoginFailedError, ElementNotFoundError

class LoginPage(BasePage):
    # Locators (adjust as per actual app)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    DASHBOARD = (By.ID, "dashboard")
    LOCKED_MESSAGE = (By.ID, "lockedMsg")
    PASSWORD_TOGGLE = (By.ID, "togglePassword")

    def login(self, username, password):
        """
        Attempt login with given credentials.
        Raises LoginFailedError if login fails.
        """
        try:
            self.send_keys(self.USERNAME_INPUT, username)
            self.send_keys(self.PASSWORD_INPUT, password)
            self.click(self.LOGIN_BUTTON)
            # Wait for dashboard or error
            if self.is_visible(self.DASHBOARD):
                return True
            elif self.is_visible(self.ERROR_MESSAGE):
                raise LoginFailedError(self.get_text(self.ERROR_MESSAGE))
            elif self.is_visible(self.LOCKED_MESSAGE):
                raise LoginFailedError(self.get_text(self.LOCKED_MESSAGE))
            else:
                raise LoginFailedError("Unknown login failure")
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            raise

    def get_error_message(self):
        """
        Get error message after failed login.
        """
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except ElementNotFoundError:
            return None

    def get_locked_message(self):
        """
        Get locked account message.
        """
        try:
            return self.get_text(self.LOCKED_MESSAGE)
        except ElementNotFoundError:
            return None

    def toggle_password_visibility(self):
        """
        Toggle password visibility.
        """
        try:
            self.click(self.PASSWORD_TOGGLE)
        except Exception as e:
            self.logger.error(f"Password toggle failed: {str(e)}")
            raise

    def is_password_visible(self):
        """
        Check if password input is visible (type='text').
        """
        try:
            element = self.find_element(self.PASSWORD_INPUT)
            return element.get_attribute("type") == "text"
        except Exception as e:
            self.logger.error(f"Check password visibility failed: {str(e)}")
            raise

    def check_accessibility(self):
        """
        Placeholder for accessibility checks (e.g., ARIA attributes).
        """
        try:
            username = self.find_element(self.USERNAME_INPUT)
            password = self.find_element(self.PASSWORD_INPUT)
            login_btn = self.find_element(self.LOGIN_BUTTON)
            # Example: check for aria-label
            assert username.get_attribute("aria-label") is not None
            assert password.get_attribute("aria-label") is not None
            assert login_btn.get_attribute("aria-label") is not None
            return True
        except Exception as e:
            self.logger.error(f"Accessibility check failed: {str(e)}")
            return False