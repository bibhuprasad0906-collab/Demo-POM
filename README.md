# Selenium Pytest Automation Framework

## Overview
This is a production-ready Selenium pytest automation framework implementing the Page Object Model (POM) pattern for UI testing. The framework is designed for enterprise-grade quality assurance with robust error handling, comprehensive logging, and full traceability.

## Features
- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Data-Driven Testing**: CSV-based test data management
- **Cross-Browser Support**: Chrome and Firefox with headless mode
- **Robust Error Handling**: Custom exceptions and comprehensive logging
- **Traceability**: Full mapping between user stories and test cases
- **CI/CD Ready**: GitHub Actions workflow included
- **Security Compliant**: No credential exposure, OWASP-aligned practices

## Project Structure
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

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Chrome or Firefox browser
- ChromeDriver or GeckoDriver (managed automatically by Selenium 4.x)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
   cd Demo-POM
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set environment variables to configure test execution:

```bash
export BASE_URL="http://localhost:8080"  # Application base URL
export BROWSER="chrome"                   # Browser: chrome or firefox
export HEADLESS="true"                    # Headless mode: true or false
export TIMEOUT="10"                       # Default timeout in seconds
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

### Run tests with specific markers:
```bash
pytest -m "story('AUTH-001')"
```

### Run tests with verbose output:
```bash
pytest -v
```

### Run tests with HTML report:
```bash
pytest --html=report.html --self-contained-html
```

## Test Data Management

Test data is stored in CSV files under `tests/data/`. Example format:

```csv
scenario,username,password,expected
AUTH-001,validUser,validPass,success
AUTH-003,invalidUser,invalidPass,fail
```

## Traceability

The `traceability.json` file maps user stories to test methods:

```json
{
  "AUTH-001": ["test_AUTH_001_login_with_valid_credentials_on_web"],
  "AUTH-003": ["test_AUTH_003_login_with_invalid_credentials_on_web"]
}
```

## Page Objects

### BasePage
Abstract base class providing safe Selenium wrappers:
- `find_element(by, value)`: Safe element location with explicit waits
- `click_element(by, value)`: Safe click with error handling
- `enter_text(by, value, text)`: Safe text entry with clear
- `is_element_visible(by, value)`: Visibility check

### LoginPage
Implements login functionality:
- `open(base_url)`: Navigate to login page
- `login(username, password)`: Perform login action
- `get_error_message()`: Retrieve error message text
- `get_lockout_message()`: Retrieve lockout message text
- `toggle_password_visibility()`: Toggle password field visibility

## Error Handling

Custom exceptions in `src/utils/exceptions.py`:
- `ElementNotFoundError`: Raised when UI element is not found
- `LoginFailedError`: Raised when login operation fails

## Logging

All operations are logged with appropriate levels:
- INFO: Normal operations
- WARNING: Performance degradation or non-critical issues
- ERROR: Failures and exceptions

Logs are written to console and can be configured for file output.

## CI/CD Integration

GitHub Actions workflow (`.github/workflows/ci.yml`) runs tests automatically on:
- Push to main branch
- Pull requests to main branch

Workflow includes:
- Python environment setup
- Dependency installation
- Browser installation
- Test execution with environment variables

## Troubleshooting

### Driver Issues
- **Error**: WebDriver not found
- **Solution**: Selenium 4.x manages drivers automatically. Ensure you have the latest version.

### Element Not Found
- **Error**: ElementNotFoundError
- **Solution**: Update locators in page objects to match actual application UI

### Timeout Issues
- **Error**: TimeoutException
- **Solution**: Increase TIMEOUT environment variable or check application responsiveness

### Data Mismatch
- **Error**: Test skipped or failed due to data issues
- **Solution**: Verify CSV headers and values match expected format

## Best Practices

1. **Locator Strategy**: Use stable locators (ID > Name > CSS > XPath)
2. **Explicit Waits**: Always use explicit waits for dynamic elements
3. **Data Separation**: Keep test data separate from test logic
4. **Error Handling**: Use custom exceptions for clear error reporting
5. **Logging**: Log all significant operations for debugging
6. **Traceability**: Maintain mapping between stories and tests
7. **Security**: Never commit credentials or sensitive data

## Maintenance Guidelines

### Adding New Tests
1. Add test case to appropriate JSON structure
2. Update CSV data file if needed
3. Create or update page object methods
4. Implement test method in test class
5. Update traceability.json
6. Run tests locally before committing

### Updating Page Objects
1. Identify changed UI elements
2. Update locators in page object
3. Update methods if interaction pattern changed
4. Run affected tests to verify
5. Update documentation if needed

### Extending Framework
1. Add new page objects under `src/pages/`
2. Add new utilities under `src/utils/`
3. Add new test files under `tests/`
4. Update requirements.txt for new dependencies
5. Update CI workflow if needed

## Non-Functional Requirements

This framework addresses:
- **Performance**: Response time validation (< 2s for login)
- **Security**: No plain-text credentials in logs, OWASP compliance
- **Accessibility**: WCAG 2.1 AA compliance validation ready
- **Availability**: Designed for 99.9% system availability testing

## Support and Contact

For issues, questions, or contributions:
- Create an issue in the GitHub repository
- Review existing documentation and troubleshooting guides
- Check traceability.json for test coverage

## License

This project is provided as-is for quality assurance purposes.

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Maintained By**: Quality Engineering Team