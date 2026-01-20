Feature: Login functionality

  Scenario: AUTH-001_Login_with_valid_credentials_on_Web
    Given the login page is open on Web
    When I enter a valid username and valid password and click Login
    Then I should be redirected to my dashboard within 2 seconds

  Scenario: AUTH-002_Login_with_valid_credentials_on_Mobile
    Given the login page is open on Mobile
    When I enter a valid username and valid password and tap Login
    Then I should be redirected to my dashboard within 2 seconds

  Scenario: AUTH-003_Login_with_invalid_credentials_on_Web
    Given the login page is open on Web
    When I enter an invalid username or invalid password and click Login
    Then I should see an error message indicating invalid credentials and not be logged in

  Scenario: AUTH-004_Login_with_invalid_credentials_on_Mobile
    Given the login page is open on Mobile
    When I enter an invalid username or invalid password and tap Login
    Then I should see an error message indicating invalid credentials and not be logged in

  Scenario: AUTH-005_Account_lockout_after_failed_attempts_on_Web
    Given the login page is open on Web
    When I enter invalid credentials 5 times in a row
    Then my account should be locked and I should see a message indicating the lockout

  Scenario: AUTH-006_Account_lockout_after_failed_attempts_on_Mobile
    Given the login page is open on Mobile
    When I enter invalid credentials 5 times in a row
    Then my account should be locked and I should see a message indicating the lockout

  Scenario: AUTH-007_Display_lockout_message_to_Locked_User_on_Web
    Given my account is locked and the login page is open on Web
    When I enter my credentials and click Login
    Then I should see a message indicating my account is locked and not be logged in

  Scenario: AUTH-008_Display_lockout_message_to_Locked_User_on_Mobile
    Given my account is locked and the login page is open on Mobile
    When I enter my credentials and tap Login
    Then I should see a message indicating my account is locked and not be logged in

  Scenario: AUTH-009_Toggle_password_visibility_on_Web
    Given the login page is open on Web
    When I click the password visibility toggle
    Then my password input should be shown or hidden accordingly

  Scenario: AUTH-010_Toggle_password_visibility_on_Mobile
    Given the login page is open on Mobile
    When I tap the password visibility toggle
    Then my password input should be shown or hidden accordingly

  Scenario: AUTH-011_Audit_login_attempts_for_security_monitoring
    Given a user attempts to log in
    When the attempt is processed
    Then an audit log entry is created without storing plain-text credentials