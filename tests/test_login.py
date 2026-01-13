"""
Login test suite.
Comprehensive test cases for authentication functionality across Web and Mobile.
Covers positive, negative, security, and accessibility scenarios.
"""

import pytest
import logging
from src.pages.login_page import LoginPage
from src.utils.config import Config
from src.utils.exceptions import LoginFailedError

class TestLogin:
    """
    Test class for login functionality.
    Implements all authentication test scenarios with proper traceability.
    """

    @pytest.mark.positive
    @pytest.mark.p1
    @pytest.mark.parametrize("username,password,env", [
        ("valid_user", "valid_pass", "Web"),
    ])
    def test_AUTH_001_valid_login_web(self, driver, username, password, env):
        """
        Test Case: AUTH-001 - Login with valid credentials on Web
        
        Scenario: As a Registered User, I want to log in via the Web environment
        using valid credentials so that I can access my dashboard.
        
        Steps:
        1. Open login page on Web
        2. Enter valid username
        3. Enter valid password
        4. Click Login button
        
        Expected Result:
        - User is redirected to dashboard within 2 seconds
        """
        logging.info(f"Starting test: AUTH-001 - Valid login on {env}")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        result = page.login(username, password, expect_success=True, timeout=2)
        
        assert result is True, "Login should succeed with valid credentials"
        assert page.is_dashboard_visible(), "Dashboard should be visible after successful login"
        
        logging.info("Test AUTH-001 passed successfully")

    @pytest.mark.positive
    @pytest.mark.p1
    @pytest.mark.parametrize("username,password,env", [
        ("valid_user", "valid_pass", "Mobile"),
    ])
    def test_AUTH_002_valid_login_mobile(self, driver, username, password, env):
        """
        Test Case: AUTH-002 - Login with valid credentials on Mobile
        
        Scenario: As a Registered User, I want to log in via the Mobile environment
        using valid credentials so that I can access my dashboard.
        
        Steps:
        1. Open login page on Mobile
        2. Enter valid username
        3. Enter valid password
        4. Tap Login button
        
        Expected Result:
        - User is redirected to dashboard within 2 seconds
        """
        logging.info(f"Starting test: AUTH-002 - Valid login on {env}")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        result = page.login(username, password, expect_success=True, timeout=2)
        
        assert result is True, "Login should succeed with valid credentials"
        assert page.is_dashboard_visible(), "Dashboard should be visible after successful login"
        
        logging.info("Test AUTH-002 passed successfully")

    @pytest.mark.negative
    @pytest.mark.p1
    @pytest.mark.parametrize("username,password,env", [
        ("invalid_user", "invalid_pass", "Web"),
    ])
    def test_AUTH_003_invalid_login_web(self, driver, username, password, env):
        """
        Test Case: AUTH-003 - Login with invalid credentials on Web
        
        Scenario: As a Registered User, I want to be notified when I enter
        invalid credentials on the Web environment so that I can correct my input.
        
        Steps:
        1. Open login page on Web
        2. Enter invalid username or password
        3. Click Login button
        
        Expected Result:
        - Error message is displayed indicating invalid credentials
        - User is not logged in
        """
        logging.info(f"Starting test: AUTH-003 - Invalid login on {env}")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        with pytest.raises(LoginFailedError):
            page.login(username, password, expect_success=False, timeout=2)
        
        assert page.is_error_message_visible(), "Error message should be visible"
        error_msg = page.get_error_message()
        assert "invalid" in error_msg.lower() or "incorrect" in error_msg.lower(), \
            "Error message should indicate invalid credentials"
        
        logging.info("Test AUTH-003 passed successfully")

    @pytest.mark.negative
    @pytest.mark.p1
    @pytest.mark.parametrize("username,password,env", [
        ("invalid_user", "invalid_pass", "Mobile"),
    ])
    def test_AUTH_004_invalid_login_mobile(self, driver, username, password, env):
        """
        Test Case: AUTH-004 - Login with invalid credentials on Mobile
        
        Scenario: As a Registered User, I want to be notified when I enter
        invalid credentials on the Mobile environment so that I can correct my input.
        
        Steps:
        1. Open login page on Mobile
        2. Enter invalid username or password
        3. Tap Login button
        
        Expected Result:
        - Error message is displayed indicating invalid credentials
        - User is not logged in
        """
        logging.info(f"Starting test: AUTH-004 - Invalid login on {env}")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        with pytest.raises(LoginFailedError):
            page.login(username, password, expect_success=False, timeout=2)
        
        assert page.is_error_message_visible(), "Error message should be visible"
        error_msg = page.get_error_message()
        assert "invalid" in error_msg.lower() or "incorrect" in error_msg.lower(), \
            "Error message should indicate invalid credentials"
        
        logging.info("Test AUTH-004 passed successfully")

    @pytest.mark.negative
    @pytest.mark.p1
    def test_AUTH_005_account_lockout_web(self, driver):
        """
        Test Case: AUTH-005 - Account lockout after repeated failed attempts on Web
        
        Scenario: As a Registered User, I want my account to be locked after
        repeated failed login attempts on the Web environment to protect
        against unauthorized access.
        
        Steps:
        1. Open login page on Web
        2. Enter invalid credentials 5 times in a row
        
        Expected Result:
        - Account is locked after 5 failed attempts
        - Lockout message is displayed
        """
        logging.info("Starting test: AUTH-005 - Account lockout on Web")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        # Attempt 5 failed logins
        page.attempt_multiple_failed_logins("lockout_user", "invalid_pass", attempts=5)
        
        # Verify lockout message
        assert page.is_lockout_message_visible(), "Lockout message should be visible"
        lockout_msg = page.get_lockout_message()
        assert "locked" in lockout_msg.lower() or "blocked" in lockout_msg.lower(), \
            "Lockout message should indicate account is locked"
        
        logging.info("Test AUTH-005 passed successfully")

    @pytest.mark.negative
    @pytest.mark.p1
    def test_AUTH_006_account_lockout_mobile(self, driver):
        """
        Test Case: AUTH-006 - Account lockout after repeated failed attempts on Mobile
        
        Scenario: As a Registered User, I want my account to be locked after
        repeated failed login attempts on the Mobile environment to protect
        against unauthorized access.
        
        Steps:
        1. Open login page on Mobile
        2. Enter invalid credentials 5 times in a row
        
        Expected Result:
        - Account is locked after 5 failed attempts
        - Lockout message is displayed
        """
        logging.info("Starting test: AUTH-006 - Account lockout on Mobile")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        # Attempt 5 failed logins
        page.attempt_multiple_failed_logins("lockout_user_mobile", "invalid_pass", attempts=5)
        
        # Verify lockout message
        assert page.is_lockout_message_visible(), "Lockout message should be visible"
        lockout_msg = page.get_lockout_message()
        assert "locked" in lockout_msg.lower() or "blocked" in lockout_msg.lower(), \
            "Lockout message should indicate account is locked"
        
        logging.info("Test AUTH-006 passed successfully")

    @pytest.mark.negative
    @pytest.mark.p1
    def test_AUTH_007_locked_user_web(self, driver):
        """
        Test Case: AUTH-007 - Display lockout message to Locked User on Web
        
        Scenario: As a Locked User, I want to be informed that my account is
        locked when I attempt to log in on the Web environment so that I know
        why I cannot access my account.
        
        Steps:
        1. Open login page on Web (account already locked)
        2. Enter username and password
        3. Click Login button
        
        Expected Result:
        - Lockout message is displayed
        - User is not logged in
        """
        logging.info("Starting test: AUTH-007 - Locked user on Web")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        # Attempt login with locked account
        with pytest.raises(LoginFailedError):
            page.login("locked_user", "valid_pass", expect_success=False, timeout=2)
        
        # Verify lockout message
        assert page.is_lockout_message_visible(), "Lockout message should be visible"
        lockout_msg = page.get_lockout_message()
        assert "locked" in lockout_msg.lower() or "blocked" in lockout_msg.lower(), \
            "Lockout message should indicate account is locked"
        
        logging.info("Test AUTH-007 passed successfully")

    @pytest.mark.negative
    @pytest.mark.p1
    def test_AUTH_008_locked_user_mobile(self, driver):
        """
        Test Case: AUTH-008 - Display lockout message to Locked User on Mobile
        
        Scenario: As a Locked User, I want to be informed that my account is
        locked when I attempt to log in on the Mobile environment so that I know
        why I cannot access my account.
        
        Steps:
        1. Open login page on Mobile (account already locked)
        2. Enter username and password
        3. Tap Login button
        
        Expected Result:
        - Lockout message is displayed
        - User is not logged in
        """
        logging.info("Starting test: AUTH-008 - Locked user on Mobile")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        # Attempt login with locked account
        with pytest.raises(LoginFailedError):
            page.login("locked_user_mobile", "valid_pass", expect_success=False, timeout=2)
        
        # Verify lockout message
        assert page.is_lockout_message_visible(), "Lockout message should be visible"
        lockout_msg = page.get_lockout_message()
        assert "locked" in lockout_msg.lower() or "blocked" in lockout_msg.lower(), \
            "Lockout message should indicate account is locked"
        
        logging.info("Test AUTH-008 passed successfully")

    @pytest.mark.positive
    @pytest.mark.p2
    def test_AUTH_009_password_visibility_toggle_web(self, driver):
        """
        Test Case: AUTH-009 - Password visibility toggle on Web
        
        Scenario: As a Registered User, I want to toggle password visibility
        on the Web login page so that I can verify my password entry.
        
        Steps:
        1. Open login page on Web
        2. Click password visibility toggle
        3. Verify password is shown
        4. Click toggle again
        5. Verify password is hidden
        
        Expected Result:
        - Password visibility toggles correctly
        """
        logging.info("Starting test: AUTH-009 - Password visibility toggle on Web")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        # Enter password
        page.enter_password("test_password")
        
        # Initially password should be hidden
        assert page.is_password_visible() is False, "Password should be hidden initially"
        
        # Toggle to show password
        page.toggle_password_visibility()
        assert page.is_password_visible() is True, "Password should be visible after toggle"
        
        # Toggle to hide password
        page.toggle_password_visibility()
        assert page.is_password_visible() is False, "Password should be hidden after second toggle"
        
        logging.info("Test AUTH-009 passed successfully")

    @pytest.mark.positive
    @pytest.mark.p2
    def test_AUTH_010_password_visibility_toggle_mobile(self, driver):
        """
        Test Case: AUTH-010 - Password visibility toggle on Mobile
        
        Scenario: As a Registered User, I want to toggle password visibility
        on the Mobile login page so that I can verify my password entry.
        
        Steps:
        1. Open login page on Mobile
        2. Tap password visibility toggle
        3. Verify password is shown
        4. Tap toggle again
        5. Verify password is hidden
        
        Expected Result:
        - Password visibility toggles correctly
        """
        logging.info("Starting test: AUTH-010 - Password visibility toggle on Mobile")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        # Enter password
        page.enter_password("test_password")
        
        # Initially password should be hidden
        assert page.is_password_visible() is False, "Password should be hidden initially"
        
        # Toggle to show password
        page.toggle_password_visibility()
        assert page.is_password_visible() is True, "Password should be visible after toggle"
        
        # Toggle to hide password
        page.toggle_password_visibility()
        assert page.is_password_visible() is False, "Password should be hidden after second toggle"
        
        logging.info("Test AUTH-010 passed successfully")

    @pytest.mark.p1
    def test_AUTH_011_audit_login_attempts(self, driver):
        """
        Test Case: AUTH-011 - Audit login attempts for compliance
        
        Scenario: As a Security Administrator, I want all login attempts to be
        auditable without storing plain-text credentials so that I can monitor
        authentication security and ensure compliance.
        
        Note: This test verifies UI behavior only. Backend audit logging
        should be verified through API or database tests.
        
        Steps:
        1. Attempt login
        2. Verify UI does not expose credentials
        
        Expected Result:
        - Login attempt is processed
        - No credentials are visible in UI
        """
        logging.info("Starting test: AUTH-011 - Audit login attempts")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        # Attempt login
        page.enter_username("audit_user")
        page.enter_password("audit_pass")
        page.click_login_button()
        
        # Verify password field is masked
        assert page.is_password_visible() is False, "Password should remain masked"
        
        logging.info("Test AUTH-011 passed successfully (UI verification only)")

    @pytest.mark.p2
    def test_AUTH_012_monitor_account_lockout_events(self, driver):
        """
        Test Case: AUTH-012 - Monitor account lockout events
        
        Scenario: As a Security Administrator, I want to monitor account lockout
        events so that I can detect potential security threats.
        
        Note: This test verifies UI behavior only. Backend audit logging
        should be verified through API or database tests.
        
        Steps:
        1. Trigger account lockout
        2. Verify lockout message is displayed
        
        Expected Result:
        - Lockout event is visible in UI
        """
        logging.info("Starting test: AUTH-012 - Monitor account lockout events")
        
        page = LoginPage(driver)
        page.open(Config.BASE_URL)
        
        # Trigger lockout
        page.attempt_multiple_failed_logins("monitor_user", "invalid_pass", attempts=5)
        
        # Verify lockout is visible
        assert page.is_lockout_message_visible(), "Lockout event should be visible in UI"
        
        logging.info("Test AUTH-012 passed successfully (UI verification only)")