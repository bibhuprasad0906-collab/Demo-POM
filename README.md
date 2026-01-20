# Selenium Pytest Automation Framework - Login Module

## Overview

This is a production-ready, enterprise-grade Selenium pytest automation framework for testing login functionality across web and mobile platforms. The framework implements robust Page Object Model (POM) architecture, comprehensive error handling, and full traceability between test cases and user stories.

## Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Cross-browser Support**: Chrome and Firefox with headless mode
- **Data-driven Testing**: CSV-based test data management
- **Comprehensive Logging**: Detailed logging for debugging and audit trails
- **CI/CD Ready**: GitHub Actions workflow included
- **Traceability**: Complete mapping between user stories and test cases
- **Security Compliant**: No plain-text credential storage, secure token handling
- **Accessibility**: WCAG 2.1 AA compliance considerations

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI pipeline
├── features/
│   └── login.feature              # Gherkin scenarios for documentation
├── src/
│   ├── pages/
│   │   ├── base_page.py          # Abstract base page with safe Selenium wrappers
│   │   └── login_page.py         # Login page object
│   └── utils/
│       ├── config.py              # Configuration management
│       ├── driver_factory.py     # WebDriver instantiation
│       └── exceptions.py         # Custom exceptions
├── tests/
│   ├── data/
│   │   └── login.csv             # Test data for data-driven tests
│   ├── conftest.py               # Pytest fixtures and configuration
│   └── test_login.py             # Login test suite
├── .gitignore                     # Git ignore patterns
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
├── traceability.json             # Story-to-test mapping
└── README.md                      # This file
```

## Prerequisites

- Python 3.8 or higher
- Chrome/Firefox browser installed
- ChromeDriver/GeckoDriver in PATH (or use webdriver-manager)
- pip package manager

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
   cd Demo-POM
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install browser drivers:**
   - **ChromeDriver**: Download from https://chromedriver.chromium.org/
   - **GeckoDriver**: Download from https://github.com/mozilla/geckodriver/releases
   - Add to system PATH or place in project root

## Configuration

The framework uses environment variables for configuration:

| Variable | Description | Default |
|----------|-------------|----------|
| `BASE_URL` | Application base URL | `http://localhost:8000` |
| `BROWSER` | Browser to use (chrome/firefox) | `chrome` |
| `HEADLESS` | Run in headless mode (true/false) | `true` |
| `TIMEOUT` | Default timeout in seconds | `10` |

**Set environment variables:**

```bash
# Linux/Mac
export BASE_URL="https://your-app.com"
export BROWSER="chrome"
export HEADLESS="true"
export TIMEOUT="10"

# Windows
set BASE_URL=https://your-app.com
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
pytest tests/test_login.py::TestLogin::test_AUTH_001_login_valid_web
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

## Test Coverage

The framework covers the following authentication scenarios:

| Story ID | Test Case | Description | Priority |
|----------|-----------|-------------|----------|
| AUTH-001 | test_AUTH_001_login_valid_web | Login with valid credentials on Web | P1 |
| AUTH-002 | test_AUTH_002_login_valid_mobile | Login with valid credentials on Mobile | P1 |
| AUTH-003 | test_AUTH_003_login_invalid_web | Login with invalid credentials on Web | P1 |
| AUTH-004 | test_AUTH_004_login_invalid_mobile | Login with invalid credentials on Mobile | P1 |
| AUTH-005 | test_AUTH_005_account_lockout_web | Account lockout after 5 failed attempts on Web | P1 |
| AUTH-006 | test_AUTH_006_account_lockout_mobile | Account lockout after 5 failed attempts on Mobile | P1 |
| AUTH-007 | test_AUTH_007_locked_user_web | Display lockout message to Locked User on Web | P1 |
| AUTH-008 | test_AUTH_008_locked_user_mobile | Display lockout message to Locked User on Mobile | P1 |
| AUTH-009 | test_AUTH_009_password_visibility_toggle_web | Password visibility toggle on Web | P2 |
| AUTH-010 | test_AUTH_010_password_visibility_toggle_mobile | Password visibility toggle on Mobile | P2 |
| AUTH-011 | test_AUTH_011_audit_login_attempts | Audit login attempts for security monitoring | P1 |

## Traceability

Complete traceability mapping is maintained in `traceability.json`. Each test method is deterministically named to match its story ID for easy tracking and reporting.

## CI/CD Integration

The framework includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

- Runs on every push and pull request to main branch
- Sets up Python environment
- Installs dependencies
- Runs tests in headless Chrome mode
- Fails fast on first test failure

**To use CI/CD:**

1. Add `BASE_URL` as a GitHub secret in repository settings
2. Push code to trigger workflow
3. View results in Actions tab

## Troubleshooting

### Common Issues and Solutions:

**1. ElementNotFoundError**
- **Cause**: UI element locator is incorrect or element not present
- **Solution**: Verify locator values in `src/pages/login_page.py` match actual application
- **Debug**: Add explicit waits or increase timeout

**2. LoginFailedError**
- **Cause**: Invalid credentials or application state
- **Solution**: Verify test data in `tests/data/login.csv` and application state
- **Debug**: Check application logs and network requests

**3. WebDriverException**
- **Cause**: Browser driver not found or incompatible version
- **Solution**: Install correct driver version matching browser version
- **Debug**: Verify driver is in PATH: `which chromedriver` or `where chromedriver`

**4. TimeoutException**
- **Cause**: Page load or element appearance exceeds timeout
- **Solution**: Increase `TIMEOUT` environment variable
- **Debug**: Check network latency and application performance

**5. Data mismatch in parametrized tests**
- **Cause**: CSV data format incorrect or missing columns
- **Solution**: Validate CSV structure matches expected format
- **Debug**: Check `tests/data/login.csv` for proper headers and data

**6. Headless mode failures**
- **Cause**: Some UI elements behave differently in headless mode
- **Solution**: Run in headed mode for debugging: `HEADLESS=false pytest`
- **Debug**: Add screenshots on failure (already implemented in conftest.py)

## Maintenance Guidelines

### Adding New Test Cases:

1. **Update test data**: Add new row to `tests/data/login.csv`
2. **Create test method**: Add new parametrized test in `tests/test_login.py`
3. **Update traceability**: Add mapping to `traceability.json`
4. **Document**: Update this README with new test case details

### Updating Page Objects:

1. **Identify new elements**: Inspect application UI for new locators
2. **Update page class**: Add new locators and methods to `src/pages/login_page.py`
3. **Test locally**: Verify changes work in both headed and headless modes
4. **Update tests**: Modify test methods to use new page object methods

### Extending to New Modules:

1. **Create new page object**: Add new file in `src/pages/`
2. **Create new test file**: Add new file in `tests/`
3. **Add test data**: Create new CSV in `tests/data/` if needed
4. **Update CI**: Modify `.github/workflows/ci.yml` if needed
5. **Document**: Create module-specific documentation

## Security Considerations

- **No credential storage**: Never commit credentials to repository
- **Environment variables**: Use environment variables for sensitive data
- **Token handling**: GitHub tokens are used in-memory only and never logged
- **Audit compliance**: All login attempts are auditable without storing plain-text credentials
- **Secret scrubbing**: All outputs are sanitized to prevent credential leakage

## Non-Functional Requirements

- **Performance**: Dashboard load time under 2 seconds
- **Availability**: System availability 99.9%
- **Accessibility**: WCAG 2.1 AA compliance
- **Security**: OWASP authentication guidelines compliance
- **Audit**: Complete audit trail without plain-text credential storage

## Future Enhancements

- [ ] Integrate Allure reporting for rich test reports
- [ ] Add API-level authentication tests
- [ ] Implement visual regression testing
- [ ] Add performance testing with Lighthouse
- [ ] Extend to additional modules (dashboard, profile, etc.)
- [ ] Add accessibility testing with axe-core
- [ ] Implement parallel test execution
- [ ] Add database validation for audit logs
- [ ] Create Docker container for consistent test environment
- [ ] Add load testing scenarios

## Support and Contact

For issues, questions, or contributions:

- **Repository**: https://github.com/bibhuprasad0906-collab/Demo-POM
- **Issues**: https://github.com/bibhuprasad0906-collab/Demo-POM/issues

## License

This project is licensed under the MIT License.

## Acknowledgments

- Selenium WebDriver community
- Pytest framework contributors
- Page Object Model pattern advocates

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Production Ready