Feature: Login functionality
  As a user of the application
  I want to be able to log in securely
  So that I can access my account and dashboard

  Background:
    Given the application is accessible
    And the login page/screen is available

  @auth @login @positive @p1 @web
  Scenario: AUTH-001 - Login with valid credentials on Web
    Given the login page is open on the web
    When I enter a valid username and valid password and click Login
    Then I should be redirected to my dashboard within 2 seconds
    And the response time should be under 2 seconds
    And no plain-text credentials should be stored in audit logs

  @auth @login @positive @p1 @mobile
  Scenario: AUTH-002 - Login with valid credentials on Mobile
    Given the login screen is open on the mobile app
    When I enter a valid username and valid password and tap Login
    Then I should be redirected to my dashboard within 2 seconds
    And the response time should be under 2 seconds
    And no plain-text credentials should be stored in audit logs

  @auth @login @negative @p1 @web
  Scenario: AUTH-003 - Login with invalid credentials on Web
    Given the login page is open on the web
    When I enter an invalid username or invalid password and click Login
    Then I should see an error message indicating invalid credentials
    And I should remain on the login page
    And no plain-text credentials should be stored in audit logs

  @auth @login @negative @p1 @mobile
  Scenario: AUTH-004 - Login with invalid credentials on Mobile
    Given the login screen is open on the mobile app
    When I enter an invalid username or invalid password and tap Login
    Then I should see an error message indicating invalid credentials
    And I should remain on the login screen
    And no plain-text credentials should be stored in audit logs

  @auth @login @security @p1 @web
  Scenario: AUTH-005 - Account lockout after repeated failed attempts on Web
    Given the login page is open on the web
    When I enter invalid credentials more than the allowed number of times consecutively
    Then my account should be locked
    And I should see a message indicating the account is locked
    And the lockout should comply with OWASP authentication guidelines

  @auth @login @security @p1 @mobile
  Scenario: AUTH-006 - Account lockout after repeated failed attempts on Mobile
    Given the login screen is open on the mobile app
    When I enter invalid credentials more than the allowed number of times consecutively
    Then my account should be locked
    And I should see a message indicating the account is locked
    And the lockout should comply with OWASP authentication guidelines

  @auth @login @security @p1 @web
  Scenario: AUTH-007 - Locked user login attempt on Web
    Given my account is locked
    And the login page is open on the web
    When I enter my username and password and click Login
    Then I should see a message indicating my account is locked
    And I should not be logged in
    And no plain-text credentials should be stored in audit logs

  @auth @login @security @p1 @mobile
  Scenario: AUTH-008 - Locked user login attempt on Mobile
    Given my account is locked
    And the login screen is open on the mobile app
    When I enter my username and password and tap Login
    Then I should see a message indicating my account is locked
    And I should not be logged in
    And no plain-text credentials should be stored in audit logs

  @auth @login @positive @p2 @web
  Scenario: AUTH-009 - Password visibility toggle on Web
    Given the login page is open on the web
    When I click the password visibility toggle
    Then my password input should be shown or hidden accordingly
    And the toggle should be accessible per WCAG 2.1 AA standards

  @auth @login @positive @p2 @mobile
  Scenario: AUTH-010 - Password visibility toggle on Mobile
    Given the login screen is open on the mobile app
    When I tap the password visibility toggle
    Then my password input should be shown or hidden accordingly
    And the toggle should be accessible per WCAG 2.1 AA standards

  @auth @security @p1
  Scenario: AUTH-011 - Audit login attempts
    Given users attempt to log in
    When a login attempt occurs
    Then an audit log entry is created
    And the audit log does not store plain-text credentials
    And the audit log includes timestamp, username, and outcome
    And the system maintains 99.9% availability