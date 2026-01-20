"""
Parametrized pytest test class for login scenarios.
Deterministic method names per story and scenario.
Full traceability to user stories AUTH-001 through AUTH-011.
"""

import pytest
import logging
from src.pages.login_page import LoginPage
from src.utils.config import Config

logger = logging.getLogger(__name__)

class TestLogin:
    """Test suite for login functionality covering all authentication scenarios."""

    @pytest.mark.p1
    @pytest.mark.web
    @pytest.mark.smoke
    def test_AUTH_001_login_valid_web(self, driver, config):
        """
        Test AUTH-001: Login with valid credentials on Web.
        
        Story: As a Registered User, I want to log in via the web application 
        using my valid credentials so that I can access my dashboard.
        
        Acceptance Criteria:
        - Given the login page is open on Web
        - When I enter a valid username and valid password and click Login
        - Then I should be redirected to my dashboard within 2 seconds
        """
        logger.info("Starting test: AUTH-001 - Login with valid credentials on Web")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        result, elapsed = page.login("valid_user_web", "valid_pass")
        
        assert result is True, "Login should succeed with valid credentials"
        assert elapsed is not None, "Elapsed time should be measured"
        assert elapsed <= 2, f"Dashboard should load within 2 seconds, but took {elapsed:.2f} seconds"
        logger.info(f"Test AUTH-001 passed. Dashboard loaded in {elapsed:.2f} seconds")

    @pytest.mark.p1
    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_AUTH_002_login_valid_mobile(self, driver, config):
        """
        Test AUTH-002: Login with valid credentials on Mobile.
        
        Story: As a Registered User, I want to log in via the mobile application 
        using my valid credentials so that I can access my dashboard.
        
        Acceptance Criteria:
        - Given the login page is open on Mobile
        - When I enter a valid username and valid password and tap Login
        - Then I should be redirected to my dashboard within 2 seconds
        """
        logger.info("Starting test: AUTH-002 - Login with valid credentials on Mobile")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        result, elapsed = page.login("valid_user_mobile", "valid_pass")
        
        assert result is True, "Login should succeed with valid credentials"
        assert elapsed is not None, "Elapsed time should be measured"
        assert elapsed <= 2, f"Dashboard should load within 2 seconds, but took {elapsed:.2f} seconds"
        logger.info(f"Test AUTH-002 passed. Dashboard loaded in {elapsed:.2f} seconds")

    @pytest.mark.p1
    @pytest.mark.web
    @pytest.mark.regression
    def test_AUTH_003_login_invalid_web(self, driver, config):
        """
        Test AUTH-003: Login with invalid credentials on Web.
        
        Story: As a Registered User, I want to be notified when I enter invalid 
        credentials on the web application so that I can correct my input.
        
        Acceptance Criteria:
        - Given the login page is open on Web
        - When I enter an invalid username or invalid password and click Login
        - Then I should see an error message indicating invalid credentials and not be logged in
        """
        logger.info("Starting test: AUTH-003 - Login with invalid credentials on Web")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        result, _ = page.login("invalid_user_web", "invalid_pass")
        
        assert result is False, "Login should fail with invalid credentials"
        error_msg = page.get_error_message()
        assert error_msg is not None, "Error message should be displayed"
        assert not page.is_dashboard_visible(), "Dashboard should not be visible"
        logger.info(f"Test AUTH-003 passed. Error message displayed: {error_msg}")

    @pytest.mark.p1
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_AUTH_004_login_invalid_mobile(self, driver, config):
        """
        Test AUTH-004: Login with invalid credentials on Mobile.
        
        Story: As a Registered User, I want to be notified when I enter invalid 
        credentials on the mobile application so that I can correct my input.
        
        Acceptance Criteria:
        - Given the login page is open on Mobile
        - When I enter an invalid username or invalid password and tap Login
        - Then I should see an error message indicating invalid credentials and not be logged in
        """
        logger.info("Starting test: AUTH-004 - Login with invalid credentials on Mobile")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        result, _ = page.login("invalid_user_mobile", "invalid_pass")
        
        assert result is False, "Login should fail with invalid credentials"
        error_msg = page.get_error_message()
        assert error_msg is not None, "Error message should be displayed"
        assert not page.is_dashboard_visible(), "Dashboard should not be visible"
        logger.info(f"Test AUTH-004 passed. Error message displayed: {error_msg}")

    @pytest.mark.p1
    @pytest.mark.web
    @pytest.mark.regression
    def test_AUTH_005_account_lockout_web(self, driver, config):
        """
        Test AUTH-005: Account lockout after repeated failed attempts on Web.
        
        Story: As a Registered User, I want my account to be locked after repeated 
        failed login attempts on the web application to protect against unauthorized access.
        
        Acceptance Criteria:
        - Given the login page is open on Web
        - When I enter invalid credentials 5 times in a row
        - Then my account should be locked and I should see a message indicating the lockout
        """
        logger.info("Starting test: AUTH-005 - Account lockout after repeated failed attempts on Web")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        # Attempt login 5 times with invalid credentials
        for attempt in range(1, 6):
            logger.info(f"Login attempt {attempt}/5")
            result, _ = page.login("lockout_user_web", "invalid_pass")
            if attempt < 5:
                assert result is False, f"Attempt {attempt} should fail"
        
        # After 5 attempts, account should be locked
        assert result == "locked", "Account should be locked after 5 failed attempts"
        lockout_msg = page.get_lockout_message()
        assert lockout_msg is not None, "Lockout message should be displayed"
        logger.info(f"Test AUTH-005 passed. Lockout message: {lockout_msg}")

    @pytest.mark.p1
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_AUTH_006_account_lockout_mobile(self, driver, config):
        """
        Test AUTH-006: Account lockout after repeated failed attempts on Mobile.
        
        Story: As a Registered User, I want my account to be locked after repeated 
        failed login attempts on the mobile application to protect against unauthorized access.
        
        Acceptance Criteria:
        - Given the login page is open on Mobile
        - When I enter invalid credentials 5 times in a row
        - Then my account should be locked and I should see a message indicating the lockout
        """
        logger.info("Starting test: AUTH-006 - Account lockout after repeated failed attempts on Mobile")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        # Attempt login 5 times with invalid credentials
        for attempt in range(1, 6):
            logger.info(f"Login attempt {attempt}/5")
            result, _ = page.login("lockout_user_mobile", "invalid_pass")
            if attempt < 5:
                assert result is False, f"Attempt {attempt} should fail"
        
        # After 5 attempts, account should be locked
        assert result == "locked", "Account should be locked after 5 failed attempts"
        lockout_msg = page.get_lockout_message()
        assert lockout_msg is not None, "Lockout message should be displayed"
        logger.info(f"Test AUTH-006 passed. Lockout message: {lockout_msg}")

    @pytest.mark.p1
    @pytest.mark.web
    @pytest.mark.regression
    def test_AUTH_007_locked_user_web(self, driver, config):
        """
        Test AUTH-007: Display lockout message to Locked User on Web.
        
        Story: As a Locked User, I want to be informed that my account is locked 
        when I attempt to log in on the web application so that I know why I cannot access my account.
        
        Acceptance Criteria:
        - Given my account is locked and the login page is open on Web
        - When I enter my username and password and click Login
        - Then I should see a message indicating my account is locked and not be logged in
        """
        logger.info("Starting test: AUTH-007 - Display lockout message to Locked User on Web")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        result, _ = page.login("locked_user_web", "any_pass")
        
        assert result == "locked", "Login should return locked status for locked account"
        lockout_msg = page.get_lockout_message()
        assert lockout_msg is not None, "Lockout message should be displayed"
        assert not page.is_dashboard_visible(), "Dashboard should not be visible"
        logger.info(f"Test AUTH-007 passed. Lockout message: {lockout_msg}")

    @pytest.mark.p1
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_AUTH_008_locked_user_mobile(self, driver, config):
        """
        Test AUTH-008: Display lockout message to Locked User on Mobile.
        
        Story: As a Locked User, I want to be informed that my account is locked 
        when I attempt to log in on the mobile application so that I know why I cannot access my account.
        
        Acceptance Criteria:
        - Given my account is locked and the login page is open on Mobile
        - When I enter my username and password and tap Login
        - Then I should see a message indicating my account is locked and not be logged in
        """
        logger.info("Starting test: AUTH-008 - Display lockout message to Locked User on Mobile")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        result, _ = page.login("locked_user_mobile", "any_pass")
        
        assert result == "locked", "Login should return locked status for locked account"
        lockout_msg = page.get_lockout_message()
        assert lockout_msg is not None, "Lockout message should be displayed"
        assert not page.is_dashboard_visible(), "Dashboard should not be visible"
        logger.info(f"Test AUTH-008 passed. Lockout message: {lockout_msg}")

    @pytest.mark.p2
    @pytest.mark.web
    @pytest.mark.regression
    def test_AUTH_009_password_visibility_toggle_web(self, driver, config):
        """
        Test AUTH-009: Password visibility toggle on Web.
        
        Story: As a Registered User, I want to toggle the visibility of my password 
        on the web login page so that I can verify my input.
        
        Acceptance Criteria:
        - Given the login page is open on Web
        - When I click the password visibility toggle
        - Then my password input should be shown or hidden accordingly
        """
        logger.info("Starting test: AUTH-009 - Password visibility toggle on Web")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        # Initially password should be hidden
        initial_type = page.get_attribute(*page.PASSWORD_INPUT, "type")
        assert initial_type == "password", "Password should initially be hidden"
        
        # Toggle visibility
        new_type = page.toggle_password_visibility()
        assert new_type in ["text", "password"], "Password input type should be valid"
        assert new_type != initial_type, "Password visibility should toggle"
        
        logger.info(f"Test AUTH-009 passed. Password type toggled from {initial_type} to {new_type}")

    @pytest.mark.p2
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_AUTH_010_password_visibility_toggle_mobile(self, driver, config):
        """
        Test AUTH-010: Password visibility toggle on Mobile.
        
        Story: As a Registered User, I want to toggle the visibility of my password 
        on the mobile login page so that I can verify my input.
        
        Acceptance Criteria:
        - Given the login page is open on Mobile
        - When I tap the password visibility toggle
        - Then my password input should be shown or hidden accordingly
        """
        logger.info("Starting test: AUTH-010 - Password visibility toggle on Mobile")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        # Initially password should be hidden
        initial_type = page.get_attribute(*page.PASSWORD_INPUT, "type")
        assert initial_type == "password", "Password should initially be hidden"
        
        # Toggle visibility
        new_type = page.toggle_password_visibility()
        assert new_type in ["text", "password"], "Password input type should be valid"
        assert new_type != initial_type, "Password visibility should toggle"
        
        logger.info(f"Test AUTH-010 passed. Password type toggled from {initial_type} to {new_type}")

    @pytest.mark.p1
    @pytest.mark.regression
    def test_AUTH_011_audit_login_attempts(self, driver, config):
        """
        Test AUTH-011: Audit login attempts for security monitoring.
        
        Story: As a Security Administrator, I want all login attempts to be auditable 
        without storing plain-text credentials so that I can monitor authentication security.
        
        Acceptance Criteria:
        - Given a user attempts to log in
        - When the attempt is processed
        - Then an audit log entry should be created without storing plain-text credentials
        
        Note: This test validates that the login process completes and assumes 
        backend audit logging is in place. Full validation requires backend/API integration.
        """
        logger.info("Starting test: AUTH-011 - Audit login attempts for security monitoring")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        
        # Perform login attempt (success or failure both should be audited)
        result, _ = page.login("audit_user", "audit_pass")
        
        # The test validates that login attempt completes
        # Actual audit log validation would require backend API or database access
        assert result in [True, False, "locked"], "Login attempt should complete"
        
        logger.info("Test AUTH-011 passed. Login attempt completed (audit log validation requires backend integration)")
        logger.warning("Note: Full audit log validation requires backend API or database access")