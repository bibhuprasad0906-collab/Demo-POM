"""LoginPage: Page object for login functionality.

Implements robust error handling, performance monitoring, and exposes
all login operations including valid/invalid login, account lockout,
and password visibility toggle.

Features:
    - Valid and invalid credential handling
    - Account lockout detection
    - Password visibility toggle
    - Response time monitoring
    - Comprehensive error handling
    - Security-compliant logging (no credential exposure)
"""

import logging
import time
from typing import Optional, Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from src.pages.base_page import BasePage
from src.utils.config import Config
from src.utils.exceptions import (
    LoginFailedError,
    AccountLockedError,
    ElementNotFoundError,
    PerformanceThresholdExceededError
)


class LoginPage(BasePage):
    """Page object for login functionality.
    
    Provides methods for all login-related operations including
    successful login, failed login, account lockout, and password
    visibility toggle.
    
    Locators:
        Update these locators to match your application's actual DOM structure.
    
    Example:
        >>> login_page = LoginPage(driver)
        >>> result = login_page.login("testuser", "password123")
        >>> assert result["success"] is True
    """
    
    # Locators - Update these according to your application's DOM
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    DASHBOARD_INDICATOR = (By.ID, "dashboard")
    PASSWORD_TOGGLE = (By.ID, "passwordToggle")
    ACCOUNT_LOCKED_MESSAGE = (By.ID, "lockedMsg")
    LOADING_INDICATOR = (By.CLASS_NAME, "loading")
    
    def __init__(self, driver: WebDriver, timeout: Optional[int] = None):
        """Initialize LoginPage.
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Optional custom timeout
        """
        super().__init__(driver, timeout)
        logging.info("LoginPage initialized")
    
    def navigate_to_login(self, url: Optional[str] = None) -> None:
        """Navigate to login page.
        
        Args:
            url: Optional custom URL. If None, uses Config.BASE_URL
        """
        login_url = url or Config.BASE_URL
        self.driver.get(login_url)
        self.wait_for_page_load()
        logging.info(f"Navigated to login page: {login_url}")
    
    def enter_username(self, username: str) -> None:
        """Enter username in the username field.
        
        Args:
            username: Username to enter
        
        Raises:
            ElementNotFoundError: If username field is not found
        """
        self.enter_text(self.USERNAME_INPUT, username)
        logging.info(f"Entered username: {username[:3]}***")  # Partial sanitization
    
    def enter_password(self, password: str) -> None:
        """Enter password in the password field.
        
        Args:
            password: Password to enter
        
        Raises:
            ElementNotFoundError: If password field is not found
        
        Security Note:
            Password is never logged in plain text.
        """
        self.enter_text(self.PASSWORD_INPUT, password)
        logging.info("Entered password: ***")  # Never log actual password
    
    def click_login_button(self) -> None:
        """Click the login button.
        
        Raises:
            ElementNotFoundError: If login button is not found
            ElementNotInteractableError: If login button is not clickable
        """
        self.click(self.LOGIN_BUTTON)
        logging.info("Clicked login button")
    
    def wait_for_loading_complete(self, timeout: int = 5) -> None:
        """Wait for loading indicator to disappear.
        
        Args:
            timeout: Maximum time to wait for loading to complete
        """
        try:
            if self.is_element_present(self.LOADING_INDICATOR, timeout=1):
                # Wait for loading indicator to disappear
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.support.ui import WebDriverWait
                WebDriverWait(self.driver, timeout).until(
                    EC.invisibility_of_element_located(self.LOADING_INDICATOR)
                )
                logging.debug("Loading complete")
        except Exception as e:
            logging.debug(f"No loading indicator or already complete: {str(e)}")
    
    def is_dashboard_displayed(self, timeout: int = 5) -> bool:
        """Check if dashboard is displayed after login.
        
        Args:
            timeout: Maximum time to wait for dashboard
        
        Returns:
            bool: True if dashboard is displayed, False otherwise
        """
        try:
            return self.is_element_visible(self.DASHBOARD_INDICATOR, timeout=timeout)
        except Exception:
            return False
    
    def is_error_displayed(self, timeout: int = 3) -> bool:
        """Check if error message is displayed.
        
        Args:
            timeout: Maximum time to wait for error message
        
        Returns:
            bool: True if error message is present and visible
        """
        try:
            return self.is_element_visible(self.ERROR_MESSAGE, timeout=timeout)
        except Exception:
            return False
    
    def get_error_message(self) -> Optional[str]:
        """Get the error message text.
        
        Returns:
            Optional[str]: Error message text or None if not found
        """
        try:
            return self.get_text(self.ERROR_MESSAGE, timeout=2)
        except ElementNotFoundError:
            return None
    
    def is_account_locked(self, timeout: int = 3) -> bool:
        """Check if account locked message is displayed.
        
        Args:
            timeout: Maximum time to wait for locked message
        
        Returns:
            bool: True if locked message is present and visible
        """
        try:
            return self.is_element_visible(self.ACCOUNT_LOCKED_MESSAGE, timeout=timeout)
        except Exception:
            return False
    
    def get_account_locked_message(self) -> Optional[str]:
        """Get the account locked message text.
        
        Returns:
            Optional[str]: Locked message text or None if not found
        """
        try:
            return self.get_text(self.ACCOUNT_LOCKED_MESSAGE, timeout=2)
        except ElementNotFoundError:
            return None
    
    def login(self, username: str, password: str, expected_success: bool = True) -> Dict[str, Any]:
        """Attempt to log in with provided credentials.
        
        Args:
            username: Username for login
            password: Password for login
            expected_success: Whether login is expected to succeed
        
        Returns:
            Dict containing:
                - success: bool - Whether login succeeded
                - response_time: float - Time taken for login operation
                - message: str - Success or error message
                - locked: bool - Whether account is locked
        
        Raises:
            LoginFailedError: If login fails and expected_success is True
            AccountLockedError: If account is locked
        
        Example:
            >>> result = login_page.login("testuser", "password123")
            >>> assert result["success"] is True
            >>> assert result["response_time"] < 2.0
        """
        start_time = time.time()
        
        try:
            # Enter credentials
            self.enter_username(username)
            self.enter_password(password)
            
            # Click login
            self.click_login_button()
            
            # Wait for loading to complete
            self.wait_for_loading_complete()
            
            # Check for account lockout first
            if self.is_account_locked(timeout=2):
                elapsed = time.time() - start_time
                locked_msg = self.get_account_locked_message() or "Account is locked"
                logging.warning(f"Account locked: {username[:3]}***")
                
                if expected_success:
                    raise AccountLockedError(
                        locked_msg,
                        context={
                            "username": f"{username[:3]}***",
                            "response_time": elapsed
                        }
                    )
                
                return {
                    "success": False,
                    "response_time": elapsed,
                    "message": locked_msg,
                    "locked": True
                }
            
            # Check for dashboard (successful login)
            if self.is_dashboard_displayed(timeout=Config.LOGIN_RESPONSE_TIME_THRESHOLD):
                elapsed = time.time() - start_time
                logging.info(f"Login successful for user: {username[:3]}*** (Response time: {elapsed:.2f}s)")
                
                # Check performance threshold
                if elapsed > Config.LOGIN_RESPONSE_TIME_THRESHOLD:
                    logging.warning(
                        f"Login response time exceeded threshold: {elapsed:.2f}s > {Config.LOGIN_RESPONSE_TIME_THRESHOLD}s"
                    )
                    if expected_success:
                        raise PerformanceThresholdExceededError(
                            f"Login response time exceeded: {elapsed:.2f}s",
                            context={
                                "actual": elapsed,
                                "threshold": Config.LOGIN_RESPONSE_TIME_THRESHOLD,
                                "unit": "seconds"
                            }
                        )
                
                return {
                    "success": True,
                    "response_time": elapsed,
                    "message": "Login successful",
                    "locked": False
                }
            
            # Check for error message (failed login)
            if self.is_error_displayed(timeout=2):
                elapsed = time.time() - start_time
                error_msg = self.get_error_message() or "Invalid credentials"
                logging.warning(f"Login failed for user: {username[:3]}*** - {error_msg}")
                
                if expected_success:
                    raise LoginFailedError(
                        error_msg,
                        context={
                            "username": f"{username[:3]}***",
                            "response_time": elapsed
                        }
                    )
                
                return {
                    "success": False,
                    "response_time": elapsed,
                    "message": error_msg,
                    "locked": False
                }
            
            # Unknown state - neither dashboard nor error
            elapsed = time.time() - start_time
            error_msg = "Login outcome unclear - neither dashboard nor error displayed"
            logging.error(error_msg)
            
            if expected_success:
                raise LoginFailedError(
                    error_msg,
                    context={
                        "username": f"{username[:3]}***",
                        "response_time": elapsed,
                        "current_url": self.get_current_url()
                    }
                )
            
            return {
                "success": False,
                "response_time": elapsed,
                "message": error_msg,
                "locked": False
            }
        
        except (LoginFailedError, AccountLockedError, PerformanceThresholdExceededError):
            # Re-raise expected exceptions
            raise
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = f"Unexpected error during login: {str(e)}"
            logging.error(error_msg)
            
            if expected_success:
                raise LoginFailedError(
                    error_msg,
                    context={
                        "username": f"{username[:3]}***",
                        "response_time": elapsed,
                        "error": str(e)
                    }
                )
            
            return {
                "success": False,
                "response_time": elapsed,
                "message": error_msg,
                "locked": False
            }
    
    def toggle_password_visibility(self) -> bool:
        """Toggle password visibility.
        
        Returns:
            bool: True if toggle succeeded and input type changed
        
        Raises:
            ElementNotFoundError: If password toggle is not found
        
        Example:
            >>> login_page.enter_password("secret")
            >>> assert login_page.toggle_password_visibility() is True
        """
        try:
            # Get initial password field type
            initial_type = self.get_attribute(self.PASSWORD_INPUT, "type")
            logging.debug(f"Initial password field type: {initial_type}")
            
            # Click toggle
            self.click(self.PASSWORD_TOGGLE)
            time.sleep(0.3)  # Brief pause for toggle animation
            
            # Get new password field type
            new_type = self.get_attribute(self.PASSWORD_INPUT, "type")
            logging.debug(f"New password field type: {new_type}")
            
            # Verify type changed
            if initial_type != new_type and new_type in ["text", "password"]:
                logging.info(f"Password visibility toggled: {initial_type} -> {new_type}")
                return True
            else:
                logging.warning(f"Password visibility toggle may have failed: {initial_type} -> {new_type}")
                return False
        
        except Exception as e:
            logging.error(f"Password visibility toggle failed: {str(e)}")
            raise ElementNotFoundError(
                f"Failed to toggle password visibility: {str(e)}",
                context={"error": str(e)}
            )
    
    def attempt_multiple_failed_logins(self, username: str, password: str, attempts: int) -> Dict[str, Any]:
        """Attempt multiple failed logins to trigger account lockout.
        
        Args:
            username: Username for login attempts
            password: Incorrect password
            attempts: Number of failed attempts to make
        
        Returns:
            Dict containing:
                - locked: bool - Whether account was locked
                - attempts_made: int - Number of attempts made before lockout
                - final_message: str - Final error or lockout message
        
        Example:
            >>> result = login_page.attempt_multiple_failed_logins("testuser", "wrong", 5)
            >>> assert result["locked"] is True
        """
        logging.info(f"Attempting {attempts} failed logins for user: {username[:3]}***")
        
        for attempt in range(1, attempts + 1):
            logging.debug(f"Failed login attempt {attempt}/{attempts}")
            
            try:
                result = self.login(username, password, expected_success=False)
                
                if result["locked"]:
                    logging.info(f"Account locked after {attempt} attempts")
                    return {
                        "locked": True,
                        "attempts_made": attempt,
                        "final_message": result["message"]
                    }
            
            except AccountLockedError as e:
                logging.info(f"Account locked after {attempt} attempts")
                return {
                    "locked": True,
                    "attempts_made": attempt,
                    "final_message": str(e)
                }
            
            # Brief pause between attempts
            if attempt < attempts:
                time.sleep(0.5)
        
        # All attempts completed without lockout
        logging.warning(f"Account not locked after {attempts} failed attempts")
        return {
            "locked": False,
            "attempts_made": attempts,
            "final_message": "Account not locked after maximum attempts"
        }