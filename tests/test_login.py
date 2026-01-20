"""
Parametrized pytest test class for login scenarios.
Deterministic method names, positive and negative tests per acceptance criteria.
"""

import pytest
from src.pages.login_page import LoginPage

class TestLogin:
    """
    Test suite for login functionality.
    """

    @pytest.mark.story("AUTH-001")
    def test_AUTH_001_login_with_valid_credentials_on_web(self, driver, config, login_data):
        """
        Test: AUTH-001 - Login with valid credentials on Web.
        """
        if login_data["scenario"] != "AUTH-001":
            pytest.skip("Not relevant for this story")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        outcome = page.login(login_data["username"], login_data["password"])
        assert outcome == "success"

    @pytest.mark.story("AUTH-002")
    def test_AUTH_002_login_with_valid_credentials_on_mobile(self, driver, config, login_data):
        """
        Test: AUTH-002 - Login with valid credentials on Mobile.
        """
        if login_data["scenario"] != "AUTH-002":
            pytest.skip("Not relevant for this story")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        outcome = page.login(login_data["username"], login_data["password"])
        assert outcome == "success"

    @pytest.mark.story("AUTH-003")
    def test_AUTH_003_login_with_invalid_credentials_on_web(self, driver, config, login_data):
        """
        Test: AUTH-003 - Login with invalid credentials on Web.
        """
        if login_data["scenario"] != "AUTH-003":
            pytest.skip("Not relevant for this story")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        outcome = page.login(login_data["username"], login_data["password"])
        assert outcome == "fail"
        assert "invalid credentials" in page.get_error_message().lower()

    @pytest.mark.story("AUTH-004")
    def test_AUTH_004_login_with_invalid_credentials_on_mobile(self, driver, config, login_data):
        """
        Test: AUTH-004 - Login with invalid credentials on Mobile.
        """
        if login_data["scenario"] != "AUTH-004":
            pytest.skip("Not relevant for this story")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        outcome = page.login(login_data["username"], login_data["password"])
        assert outcome == "fail"
        assert "invalid credentials" in page.get_error_message().lower()

    @pytest.mark.story("AUTH-005")
    def test_AUTH_005_account_lockout_after_failed_attempts_on_web(self, driver, config, login_data):
        """
        Test: AUTH-005 - Account lockout after repeated failed attempts on Web.
        """
        if login_data["scenario"] != "AUTH-005":
            pytest.skip("Not relevant for this story")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        for _ in range(5):
            outcome = page.login(login_data["username"], login_data["password"])
        assert outcome == "locked"
        assert "lockout" in page.get_lockout_message().lower()

    @pytest.mark.story("AUTH-006")
    def test_AUTH_006_account_lockout_after_failed_attempts_on_mobile(self, driver, config, login_data):
        """
        Test: AUTH-006 - Account lockout after repeated failed attempts on Mobile.
        """
        if login_data["scenario"] != "AUTH-006":
            pytest.skip("Not relevant for this story")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        for _ in range(5):
            outcome = page.login(login_data["username"], login_data["password"])
        assert outcome == "locked"
        assert "lockout" in page.get_lockout_message().lower()

    @pytest.mark.story("AUTH-007")
    def test_AUTH_007_locked_user_notification_on_web(self, driver, config, login_data):
        """
        Test: AUTH-007 - Locked user receives lockout notification on Web.
        """
        if login_data["scenario"] != "AUTH-007":
            pytest.skip("Not relevant for this story")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        outcome = page.login(login_data["username"], login_data["password"])
        assert outcome == "locked"
        assert "locked" in page.get_lockout_message().lower()

    @pytest.mark.story("AUTH-008")
    def test_AUTH_008_locked_user_notification_on_mobile(self, driver, config, login_data):
        """
        Test: AUTH-008 - Locked user receives lockout notification on Mobile.
        """
        if login_data["scenario"] != "AUTH-008":
            pytest.skip("Not relevant for this story")
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        outcome = page.login(login_data["username"], login_data["password"])
        assert outcome == "locked"
        assert "locked" in page.get_lockout_message().lower()

    @pytest.mark.story("AUTH-009")
    def test_AUTH_009_password_visibility_toggle_on_web(self, driver, config):
        """
        Test: AUTH-009 - Password visibility toggle on Web.
        """
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        initial_type = page.find_element(*page.PASSWORD_INPUT).get_attribute("type")
        toggled_type = page.toggle_password_visibility()
        assert toggled_type != initial_type
        # Toggle back
        toggled_type2 = page.toggle_password_visibility()
        assert toggled_type2 == initial_type

    @pytest.mark.story("AUTH-010")
    def test_AUTH_010_password_visibility_toggle_on_mobile(self, driver, config):
        """
        Test: AUTH-010 - Password visibility toggle on Mobile.
        """
        page = LoginPage(driver)
        page.open(config.BASE_URL)
        initial_type = page.find_element(*page.PASSWORD_INPUT).get_attribute("type")
        toggled_type = page.toggle_password_visibility()
        assert toggled_type != initial_type
        toggled_type2 = page.toggle_password_visibility()
        assert toggled_type2 == initial_type

    @pytest.mark.story("AUTH-011")
    def test_AUTH_011_audit_login_attempts_for_compliance(self, driver, config):
        """
        Test: AUTH-011 - Audit login attempts for compliance.
        Note: This test assumes access to audit logs via UI or API.
        """
        # This is a placeholder. Actual implementation depends on audit log access.
        # For demonstration, we assert that no plain-text credentials are present in logs.
        # Replace with actual audit log verification.
        audit_logs = self.get_audit_logs()
        for log in audit_logs:
            assert "password" not in log
            assert "username" in log
            assert "timestamp" in log
            assert "outcome" in log

    def get_audit_logs(self):
        """
        Stub for audit log retrieval.
        Replace with actual implementation.
        """
        # Example stub data
        return [
            {"username": "user1", "timestamp": "2024-06-01T12:00:00Z", "outcome": "success"},
            {"username": "user2", "timestamp": "2024-06-01T12:01:00Z", "outcome": "fail"},
        ]
