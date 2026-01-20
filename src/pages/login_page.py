"""
LoginPage: Page object for login functionality.
Implements login, error handling, password visibility toggle, and lockout checks.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.base_page import BasePage
from src.utils.exceptions import LoginFailedError, ElementNotFoundError
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
        Open the login page.
        """
        try:
            self.driver.get(base_url + "/login")
        except Exception as e:
            self.logger.error(f"Failed to open login page: {str(e)}")
            raise

    def login(self, username, password):
        """
        Perform login and return outcome.
        Raises LoginFailedError if login fails.
        """
        try:
            self.enter_text(*self.USERNAME_INPUT, username)
            self.enter_text(*self.PASSWORD_INPUT, password)
            self.click_element(*self.LOGIN_BUTTON)
            start = time.time()
            try:
                dashboard = WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located(self.DASHBOARD)
                )
                elapsed = time.time() - start
                if elapsed > 2:
                    self.logger.warning(f"Login response time exceeded: {elapsed:.2f}s")
                return "success"
            except Exception:
                # Check for error or lockout
                if self.is_element_present(*self.LOCKOUT_MESSAGE):
                    return "locked"
                elif self.is_element_present(*self.ERROR_MESSAGE):
                    return "fail"
                else:
                    raise LoginFailedError("Unknown login failure")
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            raise LoginFailedError(str(e))

    def is_element_present(self, by, value):
        """
        Check if element is present.
        """
        try:
            self.driver.find_element(by, value)
            return True
        except:
            return False

    def get_error_message(self):
        """
        Get error message text.
        """
        try:
            return self.find_element(*self.ERROR_MESSAGE).text
        except ElementNotFoundError:
            return ""

    def get_lockout_message(self):
        """
        Get lockout message text.
        """
        try:
            return self.find_element(*self.LOCKOUT_MESSAGE).text
        except ElementNotFoundError:
            return ""

    def toggle_password_visibility(self):
        """
        Toggle password visibility.
        """
        try:
            self.click_element(*self.PASSWORD_TOGGLE)
            # Return current type attribute
            password_field = self.find_element(*self.PASSWORD_INPUT)
            return password_field.get_attribute("type")
        except Exception as e:
            self.logger.error(f"Failed to toggle password visibility: {str(e)}")
            raise
