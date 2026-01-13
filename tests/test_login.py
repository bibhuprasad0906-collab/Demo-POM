"""
Parametrized pytest test class for login scenarios.
Deterministic method names, robust error handling, traceability to story IDs.
"""

import pytest
from src.pages.login_page import LoginPage
from src.utils.exceptions import LoginFailedError

class TestLogin:

    @pytest.mark.story("AUTH-001")
    @pytest.mark.P1
    @pytest.mark.login
    @pytest.mark.positive
    def test_AUTH_001_valid_login_web(self, driver, base_url):
        """
        Test: AUTH-001 - Login with valid credentials on Web
        Persona: Registered User
        Priority: P1
        Description: As a Registered User, I want to log in to the application via the web 
                     so that I can access my dashboard.
        """
        page = LoginPage(driver)
        page.open(base_url)
        result = page.login("valid_user", "Valid@123")
        assert result is True, "User should be redirected to dashboard"

    @pytest.mark.story("AUTH-003")
    @pytest.mark.P1
    @pytest.mark.login
    @pytest.mark.negative
    def test_AUTH_003_invalid_login_web(self, driver, base_url):
        """
        Test: AUTH-003 - Login with invalid credentials on Web
        Persona: Registered User
        Priority: P1
        Description: As a Registered User, I want to be notified when I enter invalid credentials 
                     on the web so that I can correct my input.
        """
        page = LoginPage(driver)
        page.open(base_url)
        try:
            result = page.login("invalid_user", "Invalid@123")
            assert result is False, "Error message should be displayed"
            assert page.is_visible(*page.ERROR_MESSAGE), "Error message should be visible"
            assert page.is_visible(*page.USERNAME_INPUT), "Should remain on login page"
        except LoginFailedError as e:
            assert "locked" not in str(e).lower(), "Account should not be locked for this test"

    @pytest.mark.story("AUTH-005")
    @pytest.mark.P1
    @pytest.mark.login
    @pytest.mark.negative
    def test_AUTH_005_account_lockout_web(self, driver, base_url):
        """
        Test: AUTH-005 - Account lockout after repeated failed attempts on Web
        Persona: Registered User
        Priority: P1
        Description: As a Registered User, I want my account to be locked after repeated failed 
                     login attempts on the web to protect against unauthorized access.
        """
        page = LoginPage(driver)
        page.open(base_url)
        locked = False
        for i in range(5):
            try:
                page.login("lockout_user", "WrongPassword")
            except LoginFailedError as e:
                if "locked" in str(e).lower():
                    locked = True
                    break
        assert locked, "Account should be locked after 5 failed attempts"
        assert page.is_visible(*page.LOCKED_MESSAGE), "Locked message should be visible"

    @pytest.mark.story("AUTH-007")
    @pytest.mark.P1
    @pytest.mark.login
    @pytest.mark.negative
    def test_AUTH_007_locked_user_web(self, driver, base_url):
        """
        Test: AUTH-007 - Locked user receives lockout notification on Web
        Persona: Locked User
        Priority: P1
        Description: As a Locked User, I want to be notified that my account is locked when I 
                     attempt to log in on the web so that I know why I cannot access my account.
        """
        page = LoginPage(driver)
        page.open(base_url)
        with pytest.raises(LoginFailedError):
            page.login("locked_user", "AnyPassword")
        assert page.is_visible(*page.LOCKED_MESSAGE), "Locked message should be visible"
        assert not page.is_visible(*page.DASHBOARD), "Dashboard should not be accessible"

    @pytest.mark.story("AUTH-009")
    @pytest.mark.P2
    @pytest.mark.login
    @pytest.mark.positive
    def test_AUTH_009_password_toggle_web(self, driver, base_url):
        """
        Test: AUTH-009 - Password visibility toggle on Web
        Persona: Registered User
        Priority: P2
        Description: As a Registered User, I want to toggle password visibility on the web login 
                     page so that I can verify my password entry.
        """
        page = LoginPage(driver)
        page.open(base_url)
        # Initially masked
        assert page.is_password_masked(), "Password should be masked initially"
        # Toggle to show
        shown = page.toggle_password_visibility()
        assert shown, "Password should be shown in plain text"
        # Toggle to mask again
        shown = page.toggle_password_visibility()
        assert not shown, "Password should be masked again"

    @pytest.mark.story("AUTH-012")
    @pytest.mark.P1
    @pytest.mark.login
    @pytest.mark.positive
    def test_AUTH_012_accessibility_login_form(self, driver, base_url):
        """
        Test: AUTH-012 - Accessibility compliance for login forms
        Persona: Registered User
        Priority: P1
        Description: As a Registered User, I want the login forms to be accessible so that users 
                     with disabilities can log in without barriers.
        """
        page = LoginPage(driver)
        page.open(base_url)
        # Accessibility checks (simplified, real tests use axe or pa11y)
        assert page.is_visible(*page.USERNAME_INPUT), "Username field should be accessible"
        assert page.is_visible(*page.PASSWORD_INPUT), "Password field should be accessible"
        assert page.is_visible(*page.LOGIN_BUTTON), "Login button should be accessible"


class TestLoginDataDriven:
    """
    Data-driven tests using CSV parametrization.
    """

    @pytest.mark.story("AUTH-001")
    @pytest.mark.P1
    def test_login_with_csv_data(self, driver, base_url, login_row):
        """
        Test: Data-driven login test using CSV data
        """
        if "scenario" not in login_row:
            pytest.skip("No scenario defined in CSV row")
        
        page = LoginPage(driver)
        page.open(base_url)
        
        scenario = login_row["scenario"]
        username = login_row["username"]
        password = login_row["password"]
        
        if "valid" in scenario.lower():
            result = page.login(username, password)
            assert result is True, f"Valid login should succeed for {username}"
        elif "invalid" in scenario.lower():
            try:
                result = page.login(username, password)
                assert result is False, f"Invalid login should fail for {username}"
            except LoginFailedError:
                pass  # Expected for invalid credentials
        elif "locked" in scenario.lower():
            with pytest.raises(LoginFailedError):
                page.login(username, password)
            assert page.is_visible(*page.LOCKED_MESSAGE), "Locked message should be visible"