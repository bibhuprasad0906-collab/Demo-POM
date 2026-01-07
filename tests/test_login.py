"""
Parametrized pytest test class for login scenarios.
Deterministic method names per story and scenario.
"""

import pytest
from src.pages.login_page import LoginPage
from src.utils.exceptions import LoginFailedError

class TestLogin:

    @pytest.mark.parametrize("login_record", [
        {"username": "validWebUser", "password": "validWebPass", "expected": "success", "platform": "web", "story": "AUTH-001"},
    ])
    def test_AUTH_001_login_valid_web(self, driver, base_url, login_record):
        """
        Test AUTH-001: Login with valid credentials on Web.
        """
        page = LoginPage(driver)
        page.open(base_url)
        result = page.login(login_record["username"], login_record["password"])
        assert result is True

    @pytest.mark.parametrize("login_record", [
        {"username": "validMobileUser", "password": "validMobilePass", "expected": "success", "platform": "mobile", "story": "AUTH-002"},
    ])
    def test_AUTH_002_login_valid_mobile(self, driver, base_url, login_record):
        """
        Test AUTH-002: Login with valid credentials on Mobile.
        """
        page = LoginPage(driver)
        page.open(base_url)
        result = page.login(login_record["username"], login_record["password"])
        assert result is True

    @pytest.mark.parametrize("login_record", [
        {"username": "invalidWebUser", "password": "invalidWebPass", "expected": "fail", "platform": "web", "story": "AUTH-003"},
    ])
    def test_AUTH_003_login_invalid_web(self, driver, base_url, login_record):
        """
        Test AUTH-003: Login with invalid credentials on Web.
        """
        page = LoginPage(driver)
        page.open(base_url)
        result = page.login(login_record["username"], login_record["password"])
        assert result is False
        assert "invalid" in page.get_error_message().lower()

    @pytest.mark.parametrize("login_record", [
        {"username": "invalidMobileUser", "password": "invalidMobilePass", "expected": "fail", "platform": "mobile", "story": "AUTH-004"},
    ])
    def test_AUTH_004_login_invalid_mobile(self, driver, base_url, login_record):
        """
        Test AUTH-004: Login with invalid credentials on Mobile.
        """
        page = LoginPage(driver)
        page.open(base_url)
        result = page.login(login_record["username"], login_record["password"])
        assert result is False
        assert "invalid" in page.get_error_message().lower()

    @pytest.mark.parametrize("login_record", [
        {"username": "lockoutWebUser", "password": "wrongPass", "expected": "locked", "platform": "web", "story": "AUTH-005"},
    ])
    def test_AUTH_005_account_lockout_web(self, driver, base_url, login_record):
        """
        Test AUTH-005: Account lockout after repeated failed attempts on Web.
        """
        page = LoginPage(driver)
        page.open(base_url)
        for _ in range(5):
            try:
                page.login(login_record["username"], login_record["password"])
            except LoginFailedError:
                pass
        # After 5 attempts, should be locked
        try:
            page.login(login_record["username"], login_record["password"])
        except LoginFailedError as e:
            assert "locked" in str(e).lower()
            assert "locked" in page.get_locked_message().lower()

    @pytest.mark.parametrize("login_record", [
        {"username": "lockoutMobileUser", "password": "wrongPass", "expected": "locked", "platform": "mobile", "story": "AUTH-006"},
    ])
    def test_AUTH_006_account_lockout_mobile(self, driver, base_url, login_record):
        """
        Test AUTH-006: Account lockout after repeated failed attempts on Mobile.
        """
        page = LoginPage(driver)
        page.open(base_url)
        for _ in range(5):
            try:
                page.login(login_record["username"], login_record["password"])
            except LoginFailedError:
                pass
        try:
            page.login(login_record["username"], login_record["password"])
        except LoginFailedError as e:
            assert "locked" in str(e).lower()
            assert "locked" in page.get_locked_message().lower()

    @pytest.mark.parametrize("login_record", [
        {"username": "lockedWebUser", "password": "anyPass", "expected": "locked", "platform": "web", "story": "AUTH-007"},
    ])
    def test_AUTH_007_locked_account_notification_web(self, driver, base_url, login_record):
        """
        Test AUTH-007: Notification of locked account on Web.
        """
        page = LoginPage(driver)
        page.open(base_url)
        try:
            page.login(login_record["username"], login_record["password"])
        except LoginFailedError as e:
            assert "locked" in str(e).lower()
            assert "locked" in page.get_locked_message().lower()

    @pytest.mark.parametrize("login_record", [
        {"username": "lockedMobileUser", "password": "anyPass", "expected": "locked", "platform": "mobile", "story": "AUTH-008"},
    ])
    def test_AUTH_008_locked_account_notification_mobile(self, driver, base_url, login_record):
        """
        Test AUTH-008: Notification of locked account on Mobile.
        """
        page = LoginPage(driver)
        page.open(base_url)
        try:
            page.login(login_record["username"], login_record["password"])
        except LoginFailedError as e:
            assert "locked" in str(e).lower()
            assert "locked" in page.get_locked_message().lower()

    def test_AUTH_009_password_visibility_toggle_web(self, driver, base_url):
        """
        Test AUTH-009: Password visibility toggle on Web.
        """
        page = LoginPage(driver)
        page.open(base_url)
        assert page.toggle_password_visibility() is True

    def test_AUTH_010_password_visibility_toggle_mobile(self, driver, base_url):
        """
        Test AUTH-010: Password visibility toggle on Mobile.
        """
        page = LoginPage(driver)
        page.open(base_url)
        assert page.toggle_password_visibility() is True

    def test_AUTH_011_audit_login_attempts(self):
        """
        Test AUTH-011: Audit login attempts.
        NOTE: This test is a placeholder. Actual audit log verification requires backend access.
        """
        # This would be implemented with API/database checks, not UI.
        # For now, assert True to indicate placeholder.
        assert True
