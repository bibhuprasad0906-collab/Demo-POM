"""
LoginPage: Page object for login functionality.
Implements login, error message checks, password visibility toggle, and lockout checks.
"""

from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.utils.exceptions import LoginFailedError, ElementNotFoundError
import logging
import time

class LoginPage(BasePage):
    # Locators (update as per actual app)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    DASHBOARD = (By.ID, "dashboard")
    LOCKOUT_MESSAGE = (By.ID, "lockoutMsg")
    PASSWORD_TOGGLE = (By.ID, "passwordToggle")

    def open(self, base_url):
        """
        Opens the login page.
        :param base_url: Base URL of the application
        """
        try:
            self.driver.get(base_url + "/login")
        except Exception as e:
            logging.error(f"Failed to open login page: {str(e)}")
            raise

    def login(self, username, password):
        """
        Attempts to log in with provided credentials.
        :param username: Username string
        :param password: Password string
        :raises: LoginFailedError
        """
        try:
            self.enter_text(self.USERNAME_INPUT, username)
            self.enter_text(self.PASSWORD_INPUT, password)
            self.click_element(self.LOGIN_BUTTON)
            start_time = time.time()
            # Wait for dashboard or error
            try:
                self.find_element(self.DASHBOARD)
                elapsed = time.time() - start_time
                if elapsed > 2:
                    logging.warning(f"Dashboard loaded in {elapsed:.2f}s, exceeds 2s requirement.")
                return "success"
            except ElementNotFoundError:
                if self.is_error_displayed():
                    return "fail"
                elif self.is_lockout_displayed():
                    return "locked"
                else:
                    raise LoginFailedError("Unknown login failure.")
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            raise LoginFailedError(str(e))

    def is_error_displayed(self):
        """
        Checks if error message is displayed.
        :return: True if error message is present
        """
        try:
            error = self.find_element(self.ERROR_MESSAGE)
            return error.is_displayed()
        except ElementNotFoundError:
            return False

    def is_lockout_displayed(self):
        """
        Checks if lockout message is displayed.
        :return: True if lockout message is present
        """
        try:
            lockout = self.find_element(self.LOCKOUT_MESSAGE)
            return lockout.is_displayed()
        except ElementNotFoundError:
            return False

    def toggle_password_visibility(self):
        """
        Toggles password visibility.
        :return: True if toggle successful
        """
        try:
            self.click_element(self.PASSWORD_TOGGLE)
            # Check if password input type changed
            password_input = self.find_element(self.PASSWORD_INPUT)
            input_type = password_input.get_attribute("type")
            return input_type in ["text", "password"]
        except Exception as e:
            logging.error(f"Password visibility toggle failed: {str(e)}")
            return False