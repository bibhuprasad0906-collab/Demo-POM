"""
LoginPage: Page object for login functionality.
Implements robust error handling and exposes login operations.
"""

from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.utils.exceptions import LoginFailedError, ElementNotFoundError
import time

class LoginPage(BasePage):
    # Locators (update as per actual application)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    LOCKED_MESSAGE = (By.ID, "lockedMsg")
    DASHBOARD_INDICATOR = (By.ID, "dashboard")
    PASSWORD_TOGGLE = (By.ID, "togglePassword")

    def login(self, username, password):
        """
        Attempt to log in with provided credentials.
        Returns True if dashboard is reached, False if error message appears.
        Raises LoginFailedError if login fails unexpectedly.
        """
        try:
            self.enter_text(*self.USERNAME_INPUT, username)
            self.enter_text(*self.PASSWORD_INPUT, password)
            self.click_element(*self.LOGIN_BUTTON)
            start_time = time.time()
            # Wait for dashboard or error
            if self.is_element_visible(*self.DASHBOARD_INDICATOR):
                elapsed = time.time() - start_time
                return {"result": "success", "elapsed": elapsed}
            elif self.is_element_visible(*self.ERROR_MESSAGE):
                return {"result": "error", "message": self.find_element(*self.ERROR_MESSAGE).text}
            elif self.is_element_visible(*self.LOCKED_MESSAGE):
                return {"result": "locked", "message": self.find_element(*self.LOCKED_MESSAGE).text}
            else:
                raise LoginFailedError("Login result undetermined")
        except ElementNotFoundError as e:
            raise LoginFailedError(f"Login failed: {str(e)}")
        except Exception as e:
            raise LoginFailedError(f"Unexpected error during login: {str(e)}")

    def toggle_password_visibility(self):
        """
        Toggle password visibility and return current state.
        """
        try:
            self.click_element(*self.PASSWORD_TOGGLE)
            password_field = self.find_element(*self.PASSWORD_INPUT)
            field_type = password_field.get_attribute("type")
            return field_type  # 'text' or 'password'
        except Exception as e:
            self.logger.error(f"Failed to toggle password visibility: {str(e)}")
            raise

    def is_accessible(self):
        """
        Check accessibility attributes for login controls.
        Returns True if all required attributes are present.
        """
        try:
            username = self.find_element(*self.USERNAME_INPUT)
            password = self.find_element(*self.PASSWORD_INPUT)
            login_btn = self.find_element(*self.LOGIN_BUTTON)
            # Example accessibility checks
            return all([
                username.get_attribute("aria-label") is not None,
                password.get_attribute("aria-label") is not None,
                login_btn.get_attribute("aria-label") is not None
            ])
        except Exception as e:
            self.logger.error(f"Accessibility check failed: {str(e)}")
            return False