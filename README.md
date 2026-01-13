# Selenium Pytest Automation Framework

## Overview
This is a production-ready Selenium pytest automation framework for testing login functionality across web and mobile platforms. The framework implements the Page Object Model (POM) pattern, supports data-driven testing, and includes comprehensive error handling and reporting capabilities.

## Features
- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Data-Driven Testing**: CSV-based test data management
- **Cross-Browser Support**: Chrome and Firefox with headless mode
- **Robust Error Handling**: Custom exceptions and detailed logging
- **CI/CD Ready**: GitHub Actions workflow included
- **Traceability**: Story-to-test mapping for audit and coverage
- **Accessibility Testing**: WCAG 2.1 AA compliance checks
- **Security**: No plain-text credential storage in logs

## Directory Structure
```
.
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
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
│   ├── conftest.py
│   ├── test_login.py
│   └── data/
│       └── login.csv
├── traceability.json
└── .github/
    └── workflows/
        └── ci.yml
```

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Chrome or Firefox browser
- ChromeDriver or GeckoDriver (for Selenium)

## Installation

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

4. Download browser drivers:
   - **ChromeDriver**: https://chromedriver.chromium.org/
   - **GeckoDriver**: https://github.com/mozilla/geckodriver/releases
   - Add the driver to your system PATH

## Configuration

The framework uses environment variables for configuration:

- `BASE_URL`: Application base URL (default: http://localhost:8080/login)
- `BROWSER`: Browser to use - chrome or firefox (default: chrome)
- `HEADLESS`: Run in headless mode - true or false (default: true)
- `TIMEOUT`: Implicit wait timeout in seconds (default: 10)

### Setting Environment Variables

**Linux/Mac:**
```bash
export BASE_URL=http://your-app-url.com/login
export BROWSER=chrome
export HEADLESS=true
export TIMEOUT=10
```

**Windows:**
```cmd
set BASE_URL=http://your-app-url.com/login
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

### Run tests with specific marker:
```bash
pytest -m story_AUTH_001
```

### Run tests in verbose mode:
```bash
pytest -v
```

### Run tests with HTML report:
```bash
pytest --html=report.html --self-contained-html
```

### Run tests in parallel:
```bash
pytest -n auto
```

## Test Data Management

Test data is stored in CSV files under `tests/data/`. The framework uses pytest parametrization to run data-driven tests.

**Example: tests/data/login.csv**
```csv
username,password,scenario
validUser,validPass,AUTH-001_valid
invalidUser,invalidPass,AUTH-003_invalid
lockedUser,anyPass,AUTH-007_locked
```

## Test Coverage

The framework covers the following authentication scenarios:

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
- **AUTH-011**: Audit login attempts
- **AUTH-012**: Accessibility compliance for login forms

## Traceability

The `traceability.json` file maps user stories to test cases for audit and coverage tracking:

```json
{
  "AUTH-001": ["test_AUTH_001_valid_login_web"],
  "AUTH-003": ["test_AUTH_003_invalid_login_web"],
  "AUTH-005": ["test_AUTH_005_account_lockout_web"],
  "AUTH-007": ["test_AUTH_007_locked_user_web"],
  "AUTH-009": ["test_AUTH_009_password_toggle_web"],
  "AUTH-012": ["test_AUTH_012_accessibility_login_form"]
}
```

## CI/CD Integration

The framework includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:
- Runs on every push and pull request
- Sets up Python environment
- Installs dependencies
- Runs tests in headless Chrome
- Fails fast on first error

## Troubleshooting

### Common Issues

**1. ElementNotFoundError**
- **Cause**: Locator values are incorrect or page hasn't loaded
- **Solution**: Verify locator values in page objects and increase timeout

**2. LoginFailedError**
- **Cause**: Invalid credentials or account state
- **Solution**: Validate test data in CSV files and check account status

**3. WebDriver not launching**
- **Cause**: Browser driver not installed or not in PATH
- **Solution**: Download correct driver version and add to system PATH

**4. CSV data mismatch**
- **Cause**: CSV columns don't match test expectations
- **Solution**: Ensure CSV headers match parameter names in tests

**5. CI failures**
- **Cause**: Environment variables not set or headless mode issues
- **Solution**: Check GitHub Actions secrets and browser compatibility

## Best Practices

1. **Never commit credentials**: Use environment variables or secure vaults
2. **Keep locators updated**: Review and update page objects when UI changes
3. **Maintain test data**: Regularly update CSV files with valid test scenarios
4. **Run tests locally**: Before pushing, run full test suite locally
5. **Review logs**: Check logs for warnings and errors after test runs
6. **Update traceability**: Keep traceability.json in sync with test changes

## Extending the Framework

### Adding New Page Objects

1. Create a new file in `src/pages/`
2. Inherit from `BasePage`
3. Define locators and methods
4. Import and use in test files

**Example:**
```python
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class DashboardPage(BasePage):
    WELCOME_MESSAGE = (By.ID, "welcome")
    
    def get_welcome_message(self):
        return self.get_text(*self.WELCOME_MESSAGE)
```

### Adding New Tests

1. Create test methods in `tests/test_*.py`
2. Use `@pytest.mark.story()` decorator for traceability
3. Add test data to CSV files
4. Update `traceability.json`

## Maintenance Guidelines

- **Weekly**: Review test results and update failing tests
- **Monthly**: Update dependencies and browser drivers
- **Quarterly**: Review and refactor page objects and test data
- **Annually**: Conduct full framework audit and optimization

## Security Considerations

- All credentials are loaded from environment variables
- No plain-text passwords in code or logs
- Audit logs exclude sensitive information
- GitHub tokens are stored as secrets
- Test data is sanitized before logging

## Performance Optimization

- Use headless mode for faster execution
- Run tests in parallel with pytest-xdist
- Implement smart waits instead of sleep()
- Cache browser sessions where appropriate
- Use data-driven tests to reduce code duplication

## Accessibility Testing

The framework includes basic accessibility checks for WCAG 2.1 AA compliance. For comprehensive testing, integrate:
- **axe-selenium-python**: Automated accessibility testing
- **pa11y**: Command-line accessibility testing tool

## Reporting

For enhanced reporting, install additional plugins:
```bash
pip install pytest-html allure-pytest
```

Generate Allure reports:
```bash
pytest --alluredir=./allure-results
allure serve ./allure-results
```

## Support and Contribution

For issues, questions, or contributions:
1. Open an issue on GitHub
2. Submit a pull request with detailed description
3. Follow coding standards and include tests
4. Update documentation as needed

## License

This project is licensed under the MIT License.

## Contact

For questions or support, contact the QA Engineering team.

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Maintained By**: Senior Automation and Quality Engineering Team