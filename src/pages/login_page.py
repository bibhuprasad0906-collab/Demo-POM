"""
LoginPage: Page object for login functionality.
Implements robust error handling and exposes login operations.
"""

from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.utils.exceptions import LoginFailedError, ElementNotFoundError

class LoginPage(BasePage):
    # Locators (update as per actual application)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    DASHBOARD_INDICATOR = (By.ID, "dashboard")
    LOCKOUT_MESSAGE = (By.ID, "lockoutMsg")
    PASSWORD_TOGGLE = (By.ID, "passwordToggle")

    def login(self, username, password):
        """
        Attempt login with provided credentials.
        Raises LoginFailedError if login fails.
        """
        try:
            self.enter_text(self.USERNAME_INPUT, username)
            self.enter_text(self.PASSWORD_INPUT, password)
            self.click_element(self.LOGIN_BUTTON)
        except ElementNotFoundError as e:
            raise LoginFailedError(f"Login failed: {str(e)}")

    def is_dashboard_displayed(self):
        """
        Check if dashboard is displayed after login.
        """
        return self.is_element_visible(self.DASHBOARD_INDICATOR)

    def get_error_message(self):
        """
        Retrieve error message after failed login.
        """
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_element_text(self.ERROR_MESSAGE)
        return None

    def get_lockout_message(self):
        """
        Retrieve lockout message after account is locked.
        """
        if self.is_element_visible(self.LOCKOUT_MESSAGE):
            return self.get_element_text(self.LOCKOUT_MESSAGE)
        return None

    def toggle_password_visibility(self):
        """
        Toggle password visibility.
        """
        self.click_element(self.PASSWORD_TOGGLE)

    def is_password_visible(self):
        """
        Check if password input is visible (type='text').
        """
        try:
            element = self.find_element(self.PASSWORD_INPUT)
            return element.get_attribute("type") == "text"
        except Exception:
            return False