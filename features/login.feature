Feature: Login functionality

  Scenario: AUTH-001 - Login with valid credentials on Web
    Given the login page is open on Web
    When I enter a valid username and valid password and click Login
    Then I should be redirected to my dashboard within 2 seconds

  Scenario: AUTH-002 - Login with valid credentials on Mobile
    Given the login screen is open on Mobile
    When I enter a valid username and valid password and tap Login
    Then I should be redirected to my dashboard within 2 seconds

  Scenario: AUTH-003 - Login with invalid credentials on Web
    Given the login page is open on Web
    When I enter an invalid username or password and click Login
    Then I should see an error message indicating invalid credentials
    And I should not be logged in

  Scenario: AUTH-004 - Login with invalid credentials on Mobile
    Given the login screen is open on Mobile
    When I enter an invalid username or password and tap Login
    Then I should see an error message indicating invalid credentials
    And I should not be logged in

  Scenario: AUTH-005 - Account lockout after repeated failed attempts on Web
    Given the login page is open on Web
    When I enter invalid credentials 5 times in a row
    Then my account should be locked
    And I should see a message indicating my account is locked

  Scenario: AUTH-006 - Account lockout after repeated failed attempts on Mobile
    Given the login screen is open on Mobile
    When I enter invalid credentials 5 times in a row
    Then my account should be locked
    And I should see a message indicating my account is locked

  Scenario: AUTH-007 - Locked user receives lockout notification on Web
    Given my account is locked
    When I attempt to log in on Web
    Then I should see a message indicating my account is locked
    And I should not be logged in

  Scenario: AUTH-008 - Locked user receives lockout notification on Mobile
    Given my account is locked
    When I attempt to log in on Mobile
    Then I should see a message indicating my account is locked
    And I should not be logged in

  Scenario: AUTH-009 - Password visibility toggle on Web
    Given the login page is open on Web
    When I click the password visibility toggle
    Then my password input should be shown or hidden accordingly

  Scenario: AUTH-010 - Password visibility toggle on Mobile
    Given the login screen is open on Mobile
    When I tap the password visibility toggle
    Then my password input should be shown or hidden accordingly

  Scenario: AUTH-011 - Audit login attempts for compliance
    Given a user attempts to log in
    When the attempt is processed
    Then an audit log entry is created without storing plain-text credentials

  Scenario: AUTH-012 - Accessibility compliance for login on Web
    Given the login page is open on Web
    When I use assistive technologies
    Then all login fields and controls should be accessible per WCAG 2.1 AA

  Scenario: AUTH-013 - Accessibility compliance for login on Mobile
    Given the login screen is open on Mobile
    When I use assistive technologies
    Then all login fields and controls should be accessible per WCAG 2.1 AA