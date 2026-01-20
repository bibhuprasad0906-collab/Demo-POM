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

  Scenario: AUTH-005_Account_lockout_after_repeated_failed_attempts_on_Web
    Given the login page is open on Web
    When I enter invalid credentials 5 times in a row
    Then my account should be locked and I should see a message indicating the lockout

  Scenario: AUTH-006_Account_lockout_after_repeated_failed_attempts_on_Mobile
    Given the login page is open on Mobile
    When I enter invalid credentials 5 times in a row
    Then my account should be locked and I should see a message indicating the lockout

  Scenario: AUTH-007_Locked_user_receives_lockout_notification_on_Web
    Given my account is locked and the login page is open on Web
    When I enter my credentials and click Login
    Then I should see a message indicating my account is locked and not be logged in

  Scenario: AUTH-008_Locked_user_receives_lockout_notification_on_Mobile
    Given my account is locked and the login page is open on Mobile
    When I enter my credentials and tap Login
    Then I should see a message indicating my account is locked and not be logged in

  Scenario: AUTH-009_Password_visibility_toggle_on_Web
    Given the login page is open on Web
    When I click the password visibility toggle
    Then my password should be shown or hidden accordingly

  Scenario: AUTH-010_Password_visibility_toggle_on_Mobile
    Given the login page is open on Mobile
    When I tap the password visibility toggle
    Then my password should be shown or hidden accordingly

  Scenario: AUTH-011_Audit_login_attempts_for_compliance
    Given users attempt to log in
    When I review the audit logs
    Then I should see all login attempts with timestamps, user identifiers, and outcomes, but no plain-text credentials
