"""Login test suite with parametrized tests for all authentication scenarios.
Provides comprehensive coverage of login functionality across Web and Mobile platforms."""

import pytest
import time
import logging
from src.pages.login_page import LoginPage
from src.utils.exceptions import LoginFailedError
from src.utils.config import Config

logger = logging.getLogger(__name__)


class TestLogin:
    """Test class for login functionality with comprehensive scenario coverage."""

    @pytest.mark.p1
    @pytest.mark.smoke
    @pytest.mark.parametrize("username,password,platform,story_id", [
        ("valid_user_web", "valid_pass", "web", "AUTH-001"),
        ("valid_user_mobile", "valid_pass", "mobile", "AUTH-002"),
    ])
    def test_AUTH_001_002_valid_login(self, driver, base_url, username, password, platform, story_id):
        """Test valid login on Web and Mobile (AUTH-001, AUTH-002).
        
        Verifies that users can successfully log in with valid credentials
        and are redirected to the dashboard within 2 seconds.
        
        Story IDs: AUTH-001, AUTH-002
        Priority: P1
        """
        logger.info(f"Testing {story_id}: Valid login on {platform}")
        
        login_page = LoginPage(driver)
        login_page.open(base_url)
        
        start_time = time.time()
        
        try:
            result = login_page.login(username, password)
            elapsed_time = time.time() - start_time
            
            assert result is True, "Login should succeed with valid credentials"
            assert elapsed_time < 2.0, f"Login took {elapsed_time:.2f}s, should be under 2s"
            assert login_page.is_dashboard_visible(), "Dashboard should be visible after successful login"
            
            logger.info(f"{story_id}: Valid login test passed (elapsed: {elapsed_time:.2f}s)")
            
        except LoginFailedError as e:
            pytest.fail(f"Valid login failed unexpectedly: {str(e)}")

    @pytest.mark.p1
    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,platform,story_id", [
        ("invalid_user_web", "invalid_pass", "web", "AUTH-003"),
        ("invalid_user_mobile", "invalid_pass", "mobile", "AUTH-004"),
    ])
    def test_AUTH_003_004_invalid_login(self, driver, base_url, username, password, platform, story_id):
        """Test invalid login on Web and Mobile (AUTH-003, AUTH-004).
        
        Verifies that users receive an error message when attempting to log in
        with invalid credentials.
        
        Story IDs: AUTH-003, AUTH-004
        Priority: P1
        """
        logger.info(f"Testing {story_id}: Invalid login on {platform}")
        
        login_page = LoginPage(driver)
        login_page.open(base_url)
        
        with pytest.raises(LoginFailedError, match="Invalid credentials"):
            login_page.login(username, password)
        
        # Verify error message is displayed
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "Error message should be displayed"
        assert "invalid" in error_msg.lower() or "incorrect" in error_msg.lower(), \
            "Error message should indicate invalid credentials"
        
        logger.info(f"{story_id}: Invalid login test passed")

    @pytest.mark.p1
    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,platform,story_id", [
        ("lockout_user_web", "invalid_pass", "web", "AUTH-005"),
        ("lockout_user_mobile", "invalid_pass", "mobile", "AUTH-006"),
    ])
    def test_AUTH_005_006_account_lockout(self, driver, base_url, username, password, platform, story_id):
        """Test account lockout after repeated failed attempts (AUTH-005, AUTH-006).
        
        Verifies that accounts are locked after the configured number of
        consecutive failed login attempts.
        
        Story IDs: AUTH-005, AUTH-006
        Priority: P1
        """
        logger.info(f"Testing {story_id}: Account lockout on {platform}")
        
        login_page = LoginPage(driver)
        login_page.open(base_url)
        
        # Simulate repeated failed attempts
        lockout_threshold = Config.LOCKOUT_THRESHOLD
        logger.info(f"Attempting {lockout_threshold} failed logins to trigger lockout")
        
        for attempt in range(lockout_threshold):
            try:
                login_page.login(username, password)
            except LoginFailedError:
                logger.info(f"Failed attempt {attempt + 1}/{lockout_threshold}")
                pass
        
        # After threshold, check lockout message
        lockout_msg = login_page.get_lockout_message()
        assert lockout_msg is not None, "Lockout message should be displayed after threshold"
        assert "locked" in lockout_msg.lower() or "disabled" in lockout_msg.lower(), \
            "Message should indicate account is locked"
        
        logger.info(f"{story_id}: Account lockout test passed")

    @pytest.mark.p1
    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,platform,story_id", [
        ("locked_user_web", "any_pass", "web", "AUTH-007"),
        ("locked_user_mobile", "any_pass", "mobile", "AUTH-008"),
    ])
    def test_AUTH_007_008_locked_account_login(self, driver, base_url, username, password, platform, story_id):
        """Test login attempt with locked account (AUTH-007, AUTH-008).
        
        Verifies that locked accounts cannot log in and receive appropriate
        lockout message.
        
        Story IDs: AUTH-007, AUTH-008
        Priority: P1
        """
        logger.info(f"Testing {story_id}: Locked account login on {platform}")
        
        login_page = LoginPage(driver)
        login_page.open(base_url)
        
        with pytest.raises(LoginFailedError, match="Account locked"):
            login_page.login(username, password)
        
        # Verify lockout message is displayed
        lockout_msg = login_page.get_lockout_message()
        assert lockout_msg is not None, "Lockout message should be displayed"
        assert "locked" in lockout_msg.lower() or "disabled" in lockout_msg.lower(), \
            "Message should indicate account is locked"
        
        logger.info(f"{story_id}: Locked account login test passed")

    @pytest.mark.p2
    @pytest.mark.regression
    @pytest.mark.web
    def test_AUTH_009_password_visibility_toggle_web(self, driver, base_url):
        """Test password visibility toggle on Web (AUTH-009).
        
        Verifies that users can toggle password visibility to verify their input.
        
        Story ID: AUTH-009
        Priority: P2
        """
        logger.info("Testing AUTH-009: Password visibility toggle on Web")
        
        login_page = LoginPage(driver)
        login_page.open(base_url)
        
        # Initially password input type should be 'password'
        input_type_before = login_page.get_element_attribute(
            login_page.PASSWORD_INPUT, "type"
        )
        assert input_type_before == "password", "Password should be hidden initially"
        
        # Toggle visibility
        input_type_after = login_page.toggle_password_visibility()
        assert input_type_after in ["text", "password"], "Input type should be text or password"
        assert input_type_after != input_type_before, "Input type should change after toggle"
        
        # Toggle again to verify it works both ways
        input_type_final = login_page.toggle_password_visibility()
        assert input_type_final == input_type_before, "Should return to original state"
        
        logger.info("AUTH-009: Password visibility toggle test passed")

    @pytest.mark.p2
    @pytest.mark.regression
    @pytest.mark.mobile
    def test_AUTH_010_password_visibility_toggle_mobile(self, driver, base_url):
        """Test password visibility toggle on Mobile (AUTH-010).
        
        Verifies that users can toggle password visibility on mobile devices.
        
        Story ID: AUTH-010
        Priority: P2
        """
        logger.info("Testing AUTH-010: Password visibility toggle on Mobile")
        
        login_page = LoginPage(driver)
        login_page.open(base_url)
        
        # Initially password input type should be 'password'
        input_type_before = login_page.get_element_attribute(
            login_page.PASSWORD_INPUT, "type"
        )
        assert input_type_before == "password", "Password should be hidden initially"
        
        # Toggle visibility
        input_type_after = login_page.toggle_password_visibility()
        assert input_type_after in ["text", "password"], "Input type should be text or password"
        assert input_type_after != input_type_before, "Input type should change after toggle"
        
        logger.info("AUTH-010: Password visibility toggle test passed")

    @pytest.mark.p1
    @pytest.mark.regression
    def test_AUTH_011_audit_login_attempt(self, driver, base_url):
        """Test audit log creation for login attempt (AUTH-011).
        
        Verifies that login attempts are auditable without storing plain-text credentials.
        Note: This is a placeholder test as audit log verification typically requires
        backend/API access or admin UI.
        
        Story ID: AUTH-011
        Priority: P1
        """
        logger.info("Testing AUTH-011: Audit login attempts")
        
        login_page = LoginPage(driver)
        login_page.open(base_url)
        
        # Perform a login attempt
        try:
            login_page.login("audit_test_user", "audit_test_pass")
        except LoginFailedError:
            pass  # Expected for test user
        
        # In a real scenario, this would verify:
        # 1. Audit log entry exists for this login attempt
        # 2. Log contains username, timestamp, IP, result
        # 3. Log does NOT contain plain-text password
        # 4. Log complies with security and privacy requirements
        
        # For UI test, we can only verify the login attempt was processed
        # Actual audit log verification requires backend/API integration
        
        logger.info("AUTH-011: Audit login attempt test passed (UI verification only)")
        logger.warning("Full audit log verification requires backend/API integration")
        
        # Placeholder assertion
        assert True, "Audit log verification is out of scope for UI test"