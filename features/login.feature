Feature: Login functionality

  Scenario: AUTH-001 - Login with valid credentials on Web
    Given the login page is open on a web browser
    When I enter a valid username and valid password and click Login
    Then I should be redirected to my dashboard within 2 seconds

  Scenario: AUTH-002 - Login with valid credentials on Mobile
    Given the login screen is open on the mobile app
    When I enter a valid username and valid password and tap Login
    Then I should be redirected to my dashboard within 2 seconds

  Scenario: AUTH-003 - Login with invalid credentials on Web
    Given the login page is open on a web browser
    When I enter an invalid username or password and click Login
    Then I should see an error message indicating invalid credentials
    And I should remain on the login page

  Scenario: AUTH-004 - Login with invalid credentials on Mobile
    Given the login screen is open on the mobile app
    When I enter an invalid username or password and tap Login
    Then I should see an error message indicating invalid credentials
    And I should remain on the login screen

  Scenario: AUTH-005 - Account lockout after repeated failed attempts on Web
    Given the login page is open on a web browser
    When I enter invalid credentials 5 times in a row
    Then my account should be locked
    And I should see a message indicating my account is locked

  Scenario: AUTH-006 - Account lockout after repeated failed attempts on Mobile
    Given the login screen is open on the mobile app
    When I enter invalid credentials 5 times in a row
    Then my account should be locked
    And I should see a message indicating my account is locked

  Scenario: AUTH-007 - Locked user receives lockout notification on Web
    Given my account is locked
    When I attempt to log in on the web
    Then I should see a message indicating my account is locked
    And I should not be able to access the dashboard

  Scenario: AUTH-008 - Locked user receives lockout notification on Mobile
    Given my account is locked
    When I attempt to log in on the mobile app
    Then I should see a message indicating my account is locked
    And I should not be able to access the dashboard

  Scenario: AUTH-009 - Password visibility toggle on Web
    Given the login page is open on a web browser
    When I click the password visibility toggle
    Then my password should be shown in plain text
    When I click the toggle again
    Then my password should be masked

  Scenario: AUTH-010 - Password visibility toggle on Mobile
    Given the login screen is open on the mobile app
    When I tap the password visibility toggle
    Then my password should be shown in plain text
    When I tap the toggle again
    Then my password should be masked

  Scenario: AUTH-011 - Audit login attempts
    Given a user attempts to log in (success or failure)
    When the attempt is processed
    Then an audit log entry is created without storing plain-text credentials
    And the log includes timestamp, username, result (success/failure/lockout), and environment

  Scenario: AUTH-012 - Accessibility compliance for login forms
    Given the login page or screen is open
    When I use assistive technologies
    Then all form fields, buttons, and error messages are accessible according to WCAG 2.1 AA