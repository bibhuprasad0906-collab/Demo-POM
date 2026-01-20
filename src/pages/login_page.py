"""
LoginPage: Page object for login functionality.
Implements robust error handling and POM best practices.
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
    LOCKOUT_MESSAGE = (By.ID, "lockoutMsg")
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
        Perform login action.
        Returns True if dashboard is visible within 2 seconds, else raises LoginFailedError.
        """
        try:
            self.enter_text(*self.USERNAME_INPUT, username)
            self.enter_text(*self.PASSWORD_INPUT, password)
            self.click_element(*self.LOGIN_BUTTON)
            start_time = time.time()
            if self.is_element_visible(*self.DASHBOARD_INDICATOR):
                elapsed = time.time() - start_time
                if elapsed > 2:
                    logging.warning(f"Dashboard loaded in {elapsed:.2f}s, exceeds 2s SLA.")
                return True
            elif self.is_element_visible(*self.ERROR_MESSAGE):
                raise LoginFailedError("Invalid credentials.")
            elif self.is_element_visible(*self.LOCKOUT_MESSAGE):
                raise LoginFailedError("Account locked.")
            else:
                raise LoginFailedError("Unknown login failure.")
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            raise LoginFailedError(str(e))

    def get_error_message(self):
        """
        Get error message text.
        """
        try:
            elem = self.find_element(*self.ERROR_MESSAGE)
            return elem.text
        except Exception as e:
            logging.error(f"Error message not found: {str(e)}")
            return ""

    def get_lockout_message(self):
        """
        Get lockout message text.
        """
        try:
            elem = self.find_element(*self.LOCKOUT_MESSAGE)
            return elem.text
        except Exception as e:
            logging.error(f"Lockout message not found: {str(e)}")
            return ""

    def toggle_password_visibility(self):
        """
        Toggle password visibility.
        Returns True if toggled successfully.
        """
        try:
            self.click_element(*self.PASSWORD_TOGGLE)
            # Check input type changed (implementation depends on app)
            elem = self.find_element(*self.PASSWORD_INPUT)
            input_type = elem.get_attribute("type")
            return input_type in ["text", "password"]
        except Exception as e:
            logging.error(f"Failed to toggle password visibility: {str(e)}")
            return False