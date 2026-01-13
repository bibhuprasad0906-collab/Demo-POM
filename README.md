# Selenium Pytest Automation Suite - Login Module

## Overview
This is a production-ready, enterprise-grade Selenium pytest automation suite for testing login functionality across Web and Mobile environments. The suite implements the Page Object Model (POM) pattern and follows industry best practices for maintainability, scalability, and security.

## Features
- **Page Object Model**: Clean separation of test logic and UI interactions
- **Robust Error Handling**: Custom exceptions and comprehensive logging
- **Data-Driven Testing**: CSV-based test data for scalable parametrization
- **Multi-Browser Support**: Chrome and Firefox with headless mode
- **Environment Configuration**: Flexible configuration via environment variables
- **Traceability**: Complete mapping between user stories and test cases
- **CI/CD Ready**: GitHub Actions workflow for automated testing
- **Security Compliant**: No credential leakage, audit-ready logging

## Test Coverage
This suite covers 12 authentication scenarios:
- **AUTH-001/002**: Valid login on Web/Mobile
- **AUTH-003/004**: Invalid login on Web/Mobile
- **AUTH-005/006**: Account lockout after failed attempts on Web/Mobile
- **AUTH-007/008**: Locked user message display on Web/Mobile
- **AUTH-009/010**: Password visibility toggle on Web/Mobile
- **AUTH-011**: Audit login attempts for compliance
- **AUTH-012**: Monitor account lockout events

## Directory Structure
```
.
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI pipeline
├── features/
│   └── login.feature              # Gherkin feature file
├── src/
│   ├── pages/
│   │   ├── base_page.py          # Base page object class
│   │   └── login_page.py         # Login page object
│   └── utils/
│       ├── config.py              # Configuration management
│       ├── driver_factory.py     # WebDriver factory
│       └── exceptions.py         # Custom exceptions
├── tests/
│   ├── data/
│   │   └── login.csv             # Test data
│   ├── conftest.py               # Pytest fixtures
│   └── test_login.py             # Login test cases
├── traceability.json              # Story-to-test mapping
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Prerequisites
- Python 3.8 or higher
- Chrome or Firefox browser
- ChromeDriver or GeckoDriver (matching browser version)
- pip package manager

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
   cd Demo-POM
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download WebDriver**:
   - For Chrome: Download [ChromeDriver](https://chromedriver.chromium.org/)
   - For Firefox: Download [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
   - Add the driver to your system PATH

## Configuration

The suite uses environment variables for configuration. Set these before running tests:

```bash
export BASE_URL="http://localhost:8080"  # Application base URL
export BROWSER="chrome"                   # Browser: chrome or firefox
export HEADLESS="true"                    # Headless mode: true or false
export TIMEOUT="10"                       # Implicit wait timeout in seconds
```

On Windows:
```cmd
set BASE_URL=http://localhost:8080
set BROWSER=chrome
set HEADLESS=true
set TIMEOUT=10
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test file:
```bash
pytest tests/test_login.py
```

### Run specific test:
```bash
pytest tests/test_login.py::TestLogin::test_AUTH_001_002_valid_login
```

### Run with verbose output:
```bash
pytest -v
```

### Run with HTML report:
```bash
pytest --html=report.html --self-contained-html
```

### Run in headless mode:
```bash
HEADLESS=true pytest
```

### Run with specific browser:
```bash
BROWSER=firefox pytest
```

## Test Data Management

Test data is stored in `tests/data/login.csv`. The CSV file contains:
- `story_id`: User story identifier
- `env`: Environment (Web/Mobile)
- `username`: Test username
- `password`: Test password
- `expected`: Expected outcome (success/fail/lockout/locked)

To add new test data, simply add rows to the CSV file following the same format.

## Page Objects

### BasePage
Provides common Selenium operations with robust error handling:
- `find_element(locator, timeout)`: Safe element lookup
- `click(locator)`: Safe click operation
- `enter_text(locator, text)`: Safe text input
- `is_visible(locator)`: Visibility check

### LoginPage
Encapsulates login page interactions:
- `open(base_url)`: Navigate to login page
- `login(username, password, expect_success, timeout)`: Perform login
- `get_error_message()`: Retrieve error message
- `get_lockout_message()`: Retrieve lockout message
- `toggle_password_visibility()`: Toggle password visibility
- `is_password_visible()`: Check password visibility state

## Traceability

The `traceability.json` file maps user stories to test functions:
```json
{
  "AUTH-001": ["test_AUTH_001_002_valid_login"],
  "AUTH-002": ["test_AUTH_001_002_valid_login"],
  ...
}
```

This ensures complete coverage and audit compliance.

## CI/CD Integration

The suite includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:
- Runs on every push and pull request to main branch
- Sets up Python 3.10 environment
- Installs dependencies
- Runs tests in headless Chrome mode
- Fails fast on first error

## Troubleshooting

### WebDriver Issues
- **Error**: "WebDriver not found"
  - **Solution**: Ensure ChromeDriver/GeckoDriver is in your PATH and matches your browser version

### Element Not Found
- **Error**: `ElementNotFoundError`
  - **Solution**: Verify locators in `src/pages/login_page.py` match your application's UI
  - **Solution**: Increase timeout in config if elements load slowly

### Login Failures
- **Error**: `LoginFailedError`
  - **Solution**: Check that BASE_URL is correct and application is running
  - **Solution**: Verify test credentials in `tests/data/login.csv`

### CSV Data Mismatch
- **Error**: Test parametrization fails
  - **Solution**: Ensure `tests/data/login.csv` exists and has correct headers
  - **Solution**: Check CSV format (no extra spaces, proper encoding)

## Security Considerations

- **No Credential Storage**: Credentials are never logged or persisted
- **Audit Compliance**: All operations are logged without exposing sensitive data
- **Token Security**: GitHub tokens are used in-memory only and never committed
- **OWASP Compliance**: Follows OWASP authentication testing guidelines

## Best Practices

1. **Always run tests in a controlled environment** (dev/staging, never production)
2. **Keep test data separate** from test logic
3. **Update locators** when UI changes
4. **Review traceability** after adding new stories
5. **Run tests in CI/CD** before merging code
6. **Use headless mode** for faster execution in CI/CD
7. **Monitor test execution time** and optimize slow tests

## Future Enhancements

- **Reporting**: Integrate Allure or pytest-html for richer test reports
- **Accessibility**: Add axe-selenium-python for WCAG compliance checks
- **API Testing**: Extend suite to include API-level authentication tests
- **Performance**: Add response time assertions and performance benchmarks
- **Cross-Browser**: Expand to Safari, Edge, and mobile browsers
- **Parallel Execution**: Implement pytest-xdist for parallel test runs
- **Visual Regression**: Add screenshot comparison for UI validation

## Maintenance

- **Weekly**: Review test execution logs and update flaky tests
- **Monthly**: Update dependencies and WebDriver versions
- **Quarterly**: Review and refactor page objects for maintainability
- **Per Release**: Update traceability.json and test data

## Support

For issues, questions, or contributions:
- Create an issue in the GitHub repository
- Review existing documentation and troubleshooting guides
- Contact the QA team for assistance

## License

This project is proprietary and confidential. Unauthorized distribution is prohibited.

---

**Generated by**: Senior Automation and Quality Engineering Agent
**Last Updated**: 2024
**Version**: 1.0.0