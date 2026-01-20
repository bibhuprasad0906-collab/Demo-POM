"""
LoginPage: Page object for login functionality.
Implements robust error handling and UI operations for login scenarios.
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
    LOGIN_BUTTON = (By.ID, "login-btn")
    ERROR_MESSAGE = (By.ID, "error-msg")
    DASHBOARD = (By.ID, "dashboard")
    LOCKOUT_MESSAGE = (By.ID, "lockout-msg")
    PASSWORD_TOGGLE = (By.ID, "password-toggle")

    def open(self, base_url):
        """
        Open the login page.
        """
        try:
            self.driver.get(base_url + "/login")
            self.logger.info(f"Opened login page: {base_url}/login")
        except Exception as e:
            self.logger.error(f"Failed to open login page: {str(e)}")
            raise

    def login(self, username, password):
        """
        Perform login action.
        Returns tuple: (result, elapsed_time)
        - result: True (success), False (invalid credentials), "locked" (account locked)
        - elapsed_time: Time taken to reach dashboard (only for success)
        """
        try:
            self.logger.info(f"Attempting login with username: {username}")
            self.enter_text(*self.USERNAME_INPUT, username)
            self.enter_text(*self.PASSWORD_INPUT, password)
            self.click_element(*self.LOGIN_BUTTON)
            
            start_time = time.time()
            
            # Wait for one of the possible outcomes
            try:
                # Check for successful login (dashboard appears)
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located(self.DASHBOARD)
                )
                elapsed = time.time() - start_time
                self.logger.info(f"Login successful. Dashboard loaded in {elapsed:.2f} seconds")
                return True, elapsed
            except:
                # Check for error message
                if self.is_element_present(*self.ERROR_MESSAGE, timeout=2):
                    error_msg = self.get_text(*self.ERROR_MESSAGE)
                    self.logger.warning(f"Login failed with error: {error_msg}")
                    return False, None
                # Check for lockout message
                elif self.is_element_present(*self.LOCKOUT_MESSAGE, timeout=2):
                    lockout_msg = self.get_text(*self.LOCKOUT_MESSAGE)
                    self.logger.warning(f"Account locked: {lockout_msg}")
                    return "locked", None
                else:
                    self.logger.error("Login failed for unknown reason")
                    raise LoginFailedError("Login failed for unknown reason.")
        except Exception as e:
            self.logger.error(f"Login operation failed: {str(e)}")
            raise LoginFailedError(str(e))

    def get_error_message(self):
        """
        Get error message text.
        """
        try:
            if self.is_element_present(*self.ERROR_MESSAGE, timeout=2):
                return self.get_text(*self.ERROR_MESSAGE)
            return None
        except ElementNotFoundError:
            return None

    def get_lockout_message(self):
        """
        Get lockout message text.
        """
        try:
            if self.is_element_present(*self.LOCKOUT_MESSAGE, timeout=2):
                return self.get_text(*self.LOCKOUT_MESSAGE)
            return None
        except ElementNotFoundError:
            return None

    def toggle_password_visibility(self):
        """
        Toggle password visibility.
        Returns the new input type ("text" or "password").
        """
        try:
            self.logger.info("Toggling password visibility")
            self.click_element(*self.PASSWORD_TOGGLE)
            # Get the new input type
            input_type = self.get_attribute(*self.PASSWORD_INPUT, "type")
            self.logger.info(f"Password input type changed to: {input_type}")
            return input_type
        except Exception as e:
            self.logger.error(f"Failed to toggle password visibility: {str(e)}")
            raise

    def is_dashboard_visible(self):
        """
        Check if dashboard is visible.
        """
        return self.is_element_present(*self.DASHBOARD, timeout=2)

    def is_error_displayed(self):
        """
        Check if error message is displayed.
        """
        return self.is_element_present(*self.ERROR_MESSAGE, timeout=2)

    def is_lockout_displayed(self):
        """
        Check if lockout message is displayed.
        """
        return self.is_element_present(*self.LOCKOUT_MESSAGE, timeout=2)