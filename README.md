# Selenium Pytest Automation Framework - Login Module

## Overview

This is a production-ready, enterprise-grade Selenium pytest automation framework for testing login functionality across Web and Mobile platforms. The framework implements the Page Object Model (POM) pattern, supports data-driven testing, and includes comprehensive traceability mapping.

## Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Data-Driven Testing**: CSV-based test data management
- **Cross-Browser Support**: Chrome and Firefox with headless mode
- **Robust Error Handling**: Custom exceptions and comprehensive logging
- **Traceability**: Complete mapping between user stories, scenarios, and test cases
- **CI/CD Ready**: GitHub Actions workflow included
- **Accessibility Testing**: WCAG 2.1 AA compliance checks
- **Security**: No plain-text credential storage, secure audit logging

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI pipeline
├── features/
│   └── login.feature              # Gherkin feature file
├── src/
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py          # Base page object with common methods
│   │   └── login_page.py         # Login page object
│   └── utils/
│       ├── __init__.py
│       ├── config.py              # Configuration management
│       ├── driver_factory.py     # WebDriver factory
│       └── exceptions.py         # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures and configuration
│   ├── test_login.py             # Login test cases
│   └── data/
│       └── login.csv             # Test data
├── .gitignore
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
├── traceability.json             # Story-to-test mapping
└── README.md                      # This file
```

## Test Coverage

This framework covers 13 authentication scenarios:

- **AUTH-001**: Login with valid credentials on Web
- **AUTH-002**: Login with valid credentials on Mobile
- **AUTH-003**: Login with invalid credentials on Web
- **AUTH-004**: Login with invalid credentials on Mobile
- **AUTH-005**: Account lockout after repeated failed attempts on Web
- **AUTH-006**: Account lockout after repeated failed attempts on Mobile
- **AUTH-007**: Locked user receives lockout notification on Web
- **AUTH-008**: Locked user receives lockout notification on Mobile
- **AUTH-009**: Password visibility toggle on Web
- **AUTH-010**: Password visibility toggle on Mobile
- **AUTH-011**: Audit login attempts for compliance
- **AUTH-012**: Accessibility compliance for login on Web
- **AUTH-013**: Accessibility compliance for login on Mobile

## Prerequisites

- Python 3.8 or higher
- Chrome or Firefox browser
- ChromeDriver or GeckoDriver (matching your browser version)
- pip (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
   cd Demo-POM
   ```

2. **Create a virtual environment (recommended):**
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
   - Ensure the driver is in your system PATH

## Configuration

The framework uses environment variables for configuration. Set these before running tests:

```bash
export BASE_URL="http://localhost:8080"  # Application base URL
export BROWSER="chrome"                   # Browser: chrome or firefox
export HEADLESS="true"                    # Headless mode: true or false
export TIMEOUT="10"                       # Element wait timeout in seconds
```

**Windows (PowerShell):**
```powershell
$env:BASE_URL="http://localhost:8080"
$env:BROWSER="chrome"
$env:HEADLESS="true"
$env:TIMEOUT="10"
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
pytest --html=report.html --self-contained-html
```

## Test Data Management

Test data is stored in `tests/data/login.csv`. The CSV file contains:

- `username`: Test username
- `password`: Test password
- `expected`: Expected result (success/fail/locked)
- `story`: Associated story ID

**Example:**
```csv
username,password,expected,story
validUser,validPass,success,AUTH-001
invalidUser,invalidPass,fail,AUTH-003
```

To add new test data, simply add rows to the CSV file.

## Page Objects

### BasePage
Provides common methods for all page objects:
- `find_element(locator)`: Safely find element with explicit wait
- `click(locator)`: Click element
- `send_keys(locator, value)`: Enter text
- `is_visible(locator)`: Check element visibility
- `get_text(locator)`: Get element text

### LoginPage
Implements login-specific functionality:
- `login(username, password)`: Perform login
- `get_error_message()`: Get error message
- `get_locked_message()`: Get lockout message
- `toggle_password_visibility()`: Toggle password visibility
- `is_password_visible()`: Check password visibility
- `check_accessibility()`: Verify accessibility compliance

## Traceability

The `traceability.json` file maps user stories to test methods:

```json
{
  "AUTH-001": ["test_AUTH_001_login_valid_web"],
  "AUTH-002": ["test_AUTH_002_login_valid_mobile"],
  ...
}
```

This ensures complete traceability from requirements to test execution.

## CI/CD Integration

The framework includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. Runs on push and pull requests to main branch
2. Sets up Python 3.10
3. Installs dependencies
4. Runs tests in headless Chrome
5. Fails fast on first test failure

## Troubleshooting

### Driver Not Found
**Problem**: `selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

**Solution**: 
- Download the correct ChromeDriver version for your Chrome browser
- Add ChromeDriver to your system PATH
- Or specify the driver path in `driver_factory.py`

### Element Not Found
**Problem**: `ElementNotFoundError: Element not found: (By.ID, 'username')`

**Solution**:
- Verify the application is running at BASE_URL
- Check that element locators in `login_page.py` match your application's HTML
- Increase TIMEOUT if elements load slowly

### Test Data Mismatch
**Problem**: Tests fail due to incorrect test data

**Solution**:
- Verify `tests/data/login.csv` has correct columns: username, password, expected, story
- Ensure test data matches your application's user accounts
- Check for trailing spaces or special characters in CSV

### Accessibility Test Failures
**Problem**: `test_AUTH_012_accessibility_web` fails

**Solution**:
- Ensure your application's login form has proper ARIA labels
- Add `aria-label` attributes to username, password, and login button elements
- Verify WCAG 2.1 AA compliance using browser accessibility tools

### Headless Mode Issues
**Problem**: Tests pass in normal mode but fail in headless mode

**Solution**:
- Add `--window-size=1920,1080` to browser options (already included)
- Some elements may behave differently in headless mode
- Check for JavaScript errors in headless mode

## Best Practices

1. **Keep page objects clean**: Only include page-specific methods
2. **Use explicit waits**: Avoid `time.sleep()`, use WebDriverWait
3. **Maintain test data**: Keep CSV files up-to-date with valid test accounts
4. **Update locators**: When UI changes, update locators in page objects
5. **Run tests regularly**: Integrate with CI/CD for continuous validation
6. **Review traceability**: Keep `traceability.json` synchronized with test cases
7. **Security**: Never commit credentials or tokens to version control

## Extending the Framework

### Adding New Page Objects

1. Create a new file in `src/pages/`
2. Inherit from `BasePage`
3. Define locators as class variables
4. Implement page-specific methods

**Example:**
```python
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class DashboardPage(BasePage):
    WELCOME_MESSAGE = (By.ID, "welcomeMsg")
    LOGOUT_BUTTON = (By.ID, "logoutBtn")
    
    def get_welcome_message(self):
        return self.get_text(self.WELCOME_MESSAGE)
    
    def logout(self):
        self.click(self.LOGOUT_BUTTON)
```

### Adding New Test Cases

1. Add test data to `tests/data/login.csv`
2. Create test method in `tests/test_login.py`
3. Update `traceability.json`
4. Follow naming convention: `test_<STORY_ID>_<description>`

### Adding New Browsers

1. Update `src/utils/driver_factory.py`
2. Add browser-specific options
3. Update documentation

## Non-Functional Requirements

This framework addresses the following NFRs:

- **Performance**: Response time validation (under 2 seconds)
- **Security**: No plain-text credential storage, secure audit logging
- **Accessibility**: WCAG 2.1 AA compliance checks
- **Availability**: System availability monitoring (99.9%)
- **Compliance**: OWASP authentication guidelines

## Maintenance

### Regular Tasks

1. **Update dependencies**: Run `pip list --outdated` and update `requirements.txt`
2. **Update drivers**: Keep ChromeDriver/GeckoDriver in sync with browser versions
3. **Review test data**: Ensure test accounts are valid and active
4. **Update locators**: When UI changes, update page objects
5. **Review traceability**: Keep story-to-test mapping current

### Quarterly Reviews

1. Review and update test coverage
2. Analyze test execution trends
3. Optimize slow tests
4. Update documentation
5. Review security practices

## Support and Contact

For issues, questions, or contributions:

- **GitHub Issues**: https://github.com/bibhuprasad0906-collab/Demo-POM/issues
- **Pull Requests**: https://github.com/bibhuprasad0906-collab/Demo-POM/pulls

## License

This project is provided as-is for demonstration and educational purposes.

## Changelog

### Version 1.0.0 (Initial Release)
- Complete login module automation
- 13 test scenarios covering Web and Mobile
- Page Object Model implementation
- Data-driven testing support
- CI/CD integration
- Comprehensive documentation
- Traceability mapping

---

**Note**: This framework is designed for enterprise-grade quality assurance and follows industry best practices for test automation, security, and maintainability.