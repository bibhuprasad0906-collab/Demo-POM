# Login Test Automation Suite

## Overview
Production-ready Selenium pytest automation framework for comprehensive login functionality testing across Web and Mobile platforms.

## Features
- ✅ Page Object Model (POM) architecture
- ✅ Data-driven testing with CSV
- ✅ Parametrized pytest tests
- ✅ Cross-browser support (Chrome, Firefox)
- ✅ Headless mode support
- ✅ Robust error handling and custom exceptions
- ✅ Comprehensive logging
- ✅ CI/CD integration with GitHub Actions
- ✅ Full traceability mapping

## Test Coverage
This suite covers 11 authentication scenarios:
- **AUTH-001/002**: Valid login (Web/Mobile)
- **AUTH-003/004**: Invalid credentials (Web/Mobile)
- **AUTH-005/006**: Account lockout after failed attempts (Web/Mobile)
- **AUTH-007/008**: Locked account login attempt (Web/Mobile)
- **AUTH-009/010**: Password visibility toggle (Web/Mobile)
- **AUTH-011**: Audit login attempts

## Project Structure
```
Demo-POM/
├── features/
│   └── login.feature              # Gherkin scenarios
├── src/
│   ├── pages/
│   │   ├── base_page.py          # Base page object
│   │   └── login_page.py         # Login page object
│   └── utils/
│       ├── config.py             # Configuration management
│       ├── driver_factory.py    # WebDriver factory
│       └── exceptions.py        # Custom exceptions
├── tests/
│   ├── conftest.py              # Pytest fixtures
│   ├── test_login.py            # Test cases
│   └── data/
│       └── login.csv            # Test data
├── .github/
│   └── workflows/
│       └── ci.yml               # CI/CD pipeline
├── traceability.json            # Story-to-test mapping
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Prerequisites
- Python 3.8+
- Chrome/Firefox browser
- ChromeDriver/GeckoDriver (automatically managed by Selenium 4.x)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
   cd Demo-POM
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set environment variables for test execution:

```bash
export BASE_URL="https://example.com/login"  # Target application URL
export BROWSER="chrome"                       # chrome or firefox
export HEADLESS="true"                        # true or false
export TIMEOUT="10"                           # Implicit wait timeout in seconds
```

### Windows (PowerShell):
```powershell
$env:BASE_URL="https://example.com/login"
$env:BROWSER="chrome"
$env:HEADLESS="true"
$env:TIMEOUT="10"
```

## Usage

### Run All Tests
```bash
pytest
```

### Run Specific Test
```bash
pytest tests/test_login.py::TestLogin::test_AUTH_001_002_valid_login
```

### Run with Verbose Output
```bash
pytest -v
```

### Run in Headless Mode
```bash
HEADLESS=true pytest
```

### Run with HTML Report
```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

## Test Data Management

Test data is stored in `tests/data/login.csv`:

```csv
username,password,expected,platform,story_id
valid_user_web,valid_pass,success,web,AUTH-001
valid_user_mobile,valid_pass,success,mobile,AUTH-002
...
```

Update this file to add new test scenarios or modify existing data.

## Traceability

The `traceability.json` file maps user stories to test functions:

```json
{
  "AUTH-001": ["test_AUTH_001_002_valid_login"],
  "AUTH-002": ["test_AUTH_001_002_valid_login"],
  ...
}
```

This ensures full bidirectional traceability between requirements and tests.

## CI/CD Integration

GitHub Actions workflow (`.github/workflows/ci.yml`) automatically runs tests on:
- Push to main branch
- Pull requests to main branch

Tests run in headless Chrome on Ubuntu latest.

## Page Object Model

### BasePage
Abstract base class providing safe Selenium wrappers:
- `find_element()`: Safe element location with error handling
- `click_element()`: Safe click with logging
- `enter_text()`: Safe text entry with clear
- `is_element_visible()`: Visibility check

### LoginPage
Login-specific page object:
- `open()`: Navigate to login page
- `login()`: Perform login with validation
- `get_error_message()`: Retrieve error messages
- `get_lockout_message()`: Retrieve lockout messages
- `toggle_password_visibility()`: Toggle password field visibility

## Error Handling

Custom exceptions in `src/utils/exceptions.py`:
- `ElementNotFoundError`: Raised when UI element not found
- `LoginFailedError`: Raised on login failure (invalid credentials, lockout)

## Logging

All page objects use Python's logging module:
- INFO: Normal operations
- ERROR: Failures and exceptions

Logs are output to console during test execution.

## Non-Functional Requirements

- **Performance**: Response time under 2 seconds
- **Accessibility**: WCAG 2.1 AA compliance
- **Security**: No PII in logs, OWASP authentication guidelines
- **Availability**: 99.9% system availability

## Troubleshooting

### WebDriver Issues
- **Error**: WebDriver not found
- **Solution**: Selenium 4.x auto-manages drivers. Ensure internet connectivity.

### Element Not Found
- **Error**: `ElementNotFoundError`
- **Solution**: Update locators in `src/pages/login_page.py` to match actual UI

### Test Data Mismatch
- **Error**: Parametrization errors
- **Solution**: Ensure `tests/data/login.csv` matches test expectations

### CI Failures
- **Error**: Tests fail in CI but pass locally
- **Solution**: Check environment variables in `.github/workflows/ci.yml`

## Maintenance

### Adding New Tests
1. Add scenario to `features/login.feature`
2. Add test data to `tests/data/login.csv`
3. Add test function to `tests/test_login.py`
4. Update `traceability.json`

### Updating Locators
1. Inspect UI elements
2. Update locators in `src/pages/login_page.py`
3. Run tests to verify

### Browser Updates
1. Update browser version
2. Selenium 4.x auto-updates drivers
3. Run tests to verify compatibility

## Best Practices

1. **Explicit Waits**: Use WebDriverWait for dynamic elements
2. **Stable Locators**: Prefer ID > Name > CSS > XPath
3. **Data-Driven**: Externalize test data to CSV
4. **Error Handling**: Always catch and log exceptions
5. **Clean Code**: Follow PEP 8 style guide
6. **Version Control**: Commit frequently with clear messages
7. **Code Reviews**: Review all changes before merge
8. **Documentation**: Keep README and docstrings updated

## Future Enhancements

- [ ] Add Allure reporting integration
- [ ] Implement API-level audit log verification
- [ ] Add support for Safari and Edge browsers
- [ ] Implement parallel test execution
- [ ] Add performance testing with Lighthouse
- [ ] Integrate accessibility testing with axe-core
- [ ] Add visual regression testing
- [ ] Implement test data generation
- [ ] Add database validation
- [ ] Integrate with test management tools (TestRail, Zephyr)

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License.

## Contact

Project Maintainer: bibhuprasad0906-collab
Repository: https://github.com/bibhuprasad0906-collab/Demo-POM/

## Acknowledgments

- Selenium WebDriver documentation
- Pytest documentation
- Page Object Model pattern
- OWASP security guidelines
- WCAG accessibility standards

---

**Note**: Update `BASE_URL` and locators in `src/pages/login_page.py` to match your actual application before running tests.