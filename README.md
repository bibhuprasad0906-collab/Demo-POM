# Selenium Pytest Automation Framework - Login Module

## Overview
This is a production-ready, enterprise-grade Selenium pytest automation framework for testing login functionality across Web and Mobile platforms. The framework implements the Page Object Model (POM) pattern and follows industry best practices for maintainability, scalability, and security.

## Features
- **Page Object Model**: Clean separation of test logic and page interactions
- **Cross-browser Support**: Chrome and Firefox with headless mode
- **Data-driven Testing**: CSV-based test data management
- **Robust Error Handling**: Custom exceptions and comprehensive logging
- **CI/CD Ready**: GitHub Actions workflow included
- **Traceability**: Full mapping between user stories and test cases
- **Security Compliant**: No credential exposure, audit-ready logging

## Test Coverage
This framework covers the following authentication scenarios:
- AUTH-001: Login with valid credentials on Web
- AUTH-002: Login with valid credentials on Mobile
- AUTH-003: Login with invalid credentials on Web
- AUTH-004: Login with invalid credentials on Mobile
- AUTH-005: Account lockout after repeated failed attempts on Web
- AUTH-006: Account lockout after repeated failed attempts on Mobile
- AUTH-007: Login attempt with locked account on Web
- AUTH-008: Login attempt with locked account on Mobile
- AUTH-009: Password visibility toggle on Web
- AUTH-010: Password visibility toggle on Mobile
- AUTH-011: Audit login attempts for compliance

## Directory Structure
```
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── features/
│   └── login.feature
├── src/
│   ├── pages/
│   │   ├── base_page.py
│   │   └── login_page.py
│   └── utils/
│       ├── config.py
│       ├── driver_factory.py
│       └── exceptions.py
├── tests/
│   ├── data/
│   │   └── login.csv
│   ├── conftest.py
│   └── test_login.py
├── traceability.json
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Chrome/Firefox browser
- ChromeDriver/GeckoDriver (matching browser version)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
   cd Demo-POM
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download and install WebDriver:
   - **ChromeDriver**: https://chromedriver.chromium.org/
   - **GeckoDriver**: https://github.com/mozilla/geckodriver/releases
   - Ensure the driver is in your system PATH

## Configuration

The framework uses environment variables for configuration:

| Variable | Description | Default |
|----------|-------------|----------|
| BASE_URL | Application base URL | http://localhost:8080 |
| BROWSER | Browser to use (chrome/firefox) | chrome |
| HEADLESS | Run in headless mode (true/false) | true |
| TIMEOUT | Default timeout in seconds | 10 |

### Setting Environment Variables

**Linux/Mac:**
```bash
export BASE_URL=https://your-app-url.com
export BROWSER=chrome
export HEADLESS=true
export TIMEOUT=10
```

**Windows:**
```cmd
set BASE_URL=https://your-app-url.com
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

### Run in headless mode:
```bash
HEADLESS=true pytest
```

### Run with specific browser:
```bash
BROWSER=firefox pytest
```

### Generate HTML report:
```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

## Test Data Management

Test data is stored in `tests/data/login.csv`. Each row represents a test scenario with the following columns:
- **username**: Test username
- **password**: Test password
- **expected**: Expected outcome (success/fail/locked)
- **platform**: Target platform (web/mobile)
- **story**: Associated user story ID

To add new test data:
1. Open `tests/data/login.csv`
2. Add a new row with appropriate values
3. Update `tests/test_login.py` if new test methods are needed

## Page Objects

### BasePage
Abstract base class providing common Selenium operations:
- `find_element(locator)`: Safe element finding with explicit waits
- `click_element(locator)`: Safe element clicking
- `enter_text(locator, text)`: Safe text input

### LoginPage
Implements login-specific functionality:
- `open(base_url)`: Navigate to login page
- `login(username, password)`: Perform login
- `is_error_displayed()`: Check for error messages
- `is_lockout_displayed()`: Check for lockout messages
- `toggle_password_visibility()`: Toggle password visibility

## Locator Strategy

The framework uses ID-based locators by default. Update locators in `src/pages/login_page.py` to match your application:

```python
USERNAME_INPUT = (By.ID, "username")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "loginBtn")
ERROR_MESSAGE = (By.ID, "errorMsg")
DASHBOARD = (By.ID, "dashboard")
LOCKOUT_MESSAGE = (By.ID, "lockoutMsg")
PASSWORD_TOGGLE = (By.ID, "passwordToggle")
```

## CI/CD Integration

The framework includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:
- Runs on push and pull requests to main branch
- Sets up Python environment
- Installs dependencies
- Executes tests in headless Chrome
- Fails fast on first error

## Traceability

The `traceability.json` file maps user story IDs to test methods, ensuring full traceability:

```json
{
  "AUTH-001": ["test_AUTH_001_002_valid_login"],
  "AUTH-002": ["test_AUTH_001_002_valid_login"],
  ...
}
```

## Troubleshooting

### Driver Errors
- **Issue**: WebDriver not found
- **Solution**: Ensure ChromeDriver/GeckoDriver is installed and in PATH. Check browser version compatibility.

### Element Not Found
- **Issue**: ElementNotFoundError raised
- **Solution**: Update locators in `src/pages/login_page.py` to match actual application DOM. Use browser DevTools to inspect elements.

### Timeout Errors
- **Issue**: Tests timing out
- **Solution**: Increase TIMEOUT environment variable or check application performance.

### Data Mismatches
- **Issue**: Test failures due to incorrect data
- **Solution**: Validate `tests/data/login.csv` for correct usernames/passwords and expected outcomes.

### CI Failures
- **Issue**: Tests pass locally but fail in CI
- **Solution**: Check CI logs for missing dependencies or driver issues. Ensure headless mode is properly configured.

## Best Practices

1. **Keep locators up-to-date**: Regularly review and update locators when UI changes
2. **Use explicit waits**: Avoid implicit waits and sleep statements
3. **Maintain test data**: Keep CSV files clean and well-documented
4. **Handle credentials securely**: Never commit credentials to version control
5. **Run tests regularly**: Schedule nightly CI runs for continuous monitoring
6. **Review traceability**: Update traceability.json when stories evolve
7. **Code quality**: Use linting tools (flake8, pylint) for code quality

## Future Enhancements

- Integrate backend audit log validation for AUTH-011
- Add reporting (pytest-html, Allure)
- Expand test data for edge cases (SQL injection, XSS)
- Add accessibility checks (axe-selenium-python)
- Extend Page Objects for dashboard and other flows
- Implement parallel test execution
- Add visual regression testing
- Integrate with test management tools

## Maintenance Guidelines

1. **Weekly**: Review test results and update failing tests
2. **Monthly**: Update dependencies and WebDriver versions
3. **Quarterly**: Review and refactor test code for maintainability
4. **Annually**: Conduct full framework audit and optimization

## Support and Contact

For issues, questions, or contributions, please:
- Open an issue on GitHub
- Submit a pull request with improvements
- Contact the QA team for support

## License

This project is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Maintained by**: Senior Automation and Quality Engineering Team