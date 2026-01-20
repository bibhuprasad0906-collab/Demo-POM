"""
Parametrized pytest test class for login scenarios.
Deterministic method names per story and scenario.
"""

import pytest
from src.pages.login_page import LoginPage
from src.utils.exceptions import LoginFailedError

class TestLogin:

    @pytest.mark.parametrize("login_data", [
        {"username": "validUser", "password": "validPass", "expected": "success", "story": "AUTH-001"},
    ])
    def test_AUTH_001_login_valid_web(self, driver, login_data):
        """
        Test AUTH-001: Login with valid credentials on Web.
        """
        page = LoginPage(driver)
        try:
            result = page.login(login_data["username"], login_data["password"])
            assert result is True
        except LoginFailedError:
            pytest.fail("Login failed with valid credentials.")

    @pytest.mark.parametrize("login_data", [
        {"username": "validUserMobile", "password": "validPassMobile", "expected": "success", "story": "AUTH-002"},
    ])
    def test_AUTH_002_login_valid_mobile(self, driver, login_data):
        """
        Test AUTH-002: Login with valid credentials on Mobile.
        """
        page = LoginPage(driver)
        try:
            result = page.login(login_data["username"], login_data["password"])
            assert result is True
        except LoginFailedError:
            pytest.fail("Login failed with valid credentials (Mobile).")

    @pytest.mark.parametrize("login_data", [
        {"username": "invalidUser", "password": "invalidPass", "expected": "fail", "story": "AUTH-003"},
    ])
    def test_AUTH_003_login_invalid_web(self, driver, login_data):
        """
        Test AUTH-003: Login with invalid credentials on Web.
        """
        page = LoginPage(driver)
        with pytest.raises(LoginFailedError):
            page.login(login_data["username"], login_data["password"])
        assert page.get_error_message() is not None

    @pytest.mark.parametrize("login_data", [
        {"username": "invalidUserMobile", "password": "invalidPassMobile", "expected": "fail", "story": "AUTH-004"},
    ])
    def test_AUTH_004_login_invalid_mobile(self, driver, login_data):
        """
        Test AUTH-004: Login with invalid credentials on Mobile.
        """
        page = LoginPage(driver)
        with pytest.raises(LoginFailedError):
            page.login(login_data["username"], login_data["password"])
        assert page.get_error_message() is not None

    def test_AUTH_005_account_lockout_web(self, driver):
        """
        Test AUTH-005: Account lockout after 5 failed attempts on Web.
        """
        page = LoginPage(driver)
        for _ in range(5):
            with pytest.raises(LoginFailedError):
                page.login("invalidUser", "invalidPass")
        assert page.get_locked_message() is not None

    def test_AUTH_006_account_lockout_mobile(self, driver):
        """
        Test AUTH-006: Account lockout after 5 failed attempts on Mobile.
        """
        page = LoginPage(driver)
        for _ in range(5):
            with pytest.raises(LoginFailedError):
                page.login("invalidUserMobile", "invalidPassMobile")
        assert page.get_locked_message() is not None

    def test_AUTH_007_locked_user_web(self, driver):
        """
        Test AUTH-007: Locked user receives lockout notification on Web.
        """
        page = LoginPage(driver)
        with pytest.raises(LoginFailedError):
            page.login("lockedUser", "anyPass")
        assert page.get_locked_message() is not None

    def test_AUTH_008_locked_user_mobile(self, driver):
        """
        Test AUTH-008: Locked user receives lockout notification on Mobile.
        """
        page = LoginPage(driver)
        with pytest.raises(LoginFailedError):
            page.login("lockedUserMobile", "anyPass")
        assert page.get_locked_message() is not None

    def test_AUTH_009_password_visibility_toggle_web(self, driver):
        """
        Test AUTH-009: Password visibility toggle on Web.
        """
        page = LoginPage(driver)
        page.toggle_password_visibility()
        assert page.is_password_visible() is True
        page.toggle_password_visibility()
        assert page.is_password_visible() is False

    def test_AUTH_010_password_visibility_toggle_mobile(self, driver):
        """
        Test AUTH-010: Password visibility toggle on Mobile.
        """
        page = LoginPage(driver)
        page.toggle_password_visibility()
        assert page.is_password_visible() is True
        page.toggle_password_visibility()
        assert page.is_password_visible() is False

    def test_AUTH_011_audit_login_attempts(self, driver):
        """
        Test AUTH-011: Audit login attempts for compliance.
        Placeholder: Check for audit log entry (requires backend integration).
        """
        # This would require backend verification; here we check no plain-text credentials in UI logs.
        # For demonstration, we assert no credentials in error messages.
        page = LoginPage(driver)
        with pytest.raises(LoginFailedError):
            page.login("auditUser", "auditPass")
        error_msg = page.get_error_message()
        assert "auditPass" not in error_msg

    def test_AUTH_012_accessibility_web(self, driver):
        """
        Test AUTH-012: Accessibility compliance for login on Web.
        """
        page = LoginPage(driver)
        assert page.check_accessibility() is True

    def test_AUTH_013_accessibility_mobile(self, driver):
        """
        Test AUTH-013: Accessibility compliance for login on Mobile.
        """
        page = LoginPage(driver)
        assert page.check_accessibility() is True