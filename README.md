# Selenium Login Test Suite - Production-Ready Automation Framework

## Overview

This repository contains a production-ready, enterprise-grade Selenium pytest automation framework for comprehensive login functionality testing. The suite implements robust error handling, secure credential management, and full traceability from requirements to test execution.

## Project Structure

```
Demo-POM/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI pipeline
├── features/
│   └── login.feature              # Gherkin scenarios for login
├── src/
│   ├── pages/
│   │   ├── base_page.py          # Abstract base page object
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
├── traceability.json             # Requirements-to-tests mapping
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Robust Error Handling**: Custom exceptions and safe Selenium wrappers
- **Data-Driven Testing**: CSV-based test data with pytest parametrization
- **Environment Configuration**: Flexible config via environment variables
- **Cross-Browser Support**: Chrome and Firefox with headless mode
- **CI/CD Ready**: GitHub Actions workflow for automated testing
- **Full Traceability**: JSON mapping from user stories to test cases
- **Security Compliant**: No plain-text credentials in logs or commits
- **Accessibility Testing**: WCAG 2.1 AA compliance checks

## Test Coverage

The suite covers 12 authentication user stories:

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

## Prerequisites

- Python 3.8 or higher
- Chrome/Firefox browser
- ChromeDriver/GeckoDriver (automatically managed by Selenium 4.x)
- pip package manager

## Installation

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
export BASE_URL="https://example.com"  # Target application URL
export BROWSER="chrome"                 # chrome or firefox
export HEADLESS="true"                  # true or false
export TIMEOUT="10"                     # Implicit wait timeout in seconds
```

On Windows:
```cmd
set BASE_URL=https://example.com
set BROWSER=chrome
set HEADLESS=true
set TIMEOUT=10
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test:
```bash
pytest tests/test_login.py::TestLogin::test_AUTH_001_login_valid_web
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
export HEADLESS=true
pytest
```

## Test Data Management

Test data is stored in `tests/data/login.csv`. Update this file to add new test scenarios:

```csv
username,password,expected,platform,story
valid_user_web,valid_pass,success,web,AUTH-001
invalid_user_web,invalid_pass,fail,web,AUTH-003
```

## Continuous Integration

The repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

- Runs on every push and pull request to main branch
- Sets up Python 3.10 environment
- Installs dependencies
- Executes all tests in headless Chrome
- Reports test results

## Traceability

The `traceability.json` file maps user story IDs to test function names, ensuring complete requirements coverage:

```json
{
  "AUTH-001": ["test_AUTH_001_login_valid_web"],
  "AUTH-002": ["test_AUTH_002_login_valid_mobile"]
}
```

## Page Objects

### BasePage
Abstract base class providing:
- Safe element finding with explicit waits
- Robust click and text entry methods
- Element visibility checks
- Comprehensive error handling

### LoginPage
Login-specific page object with:
- Login operation
- Dashboard verification
- Error message retrieval
- Lockout message retrieval
- Password visibility toggle

## Maintenance

### Updating Locators
When UI changes, update locators in `src/pages/login_page.py`:

```python
USERNAME_INPUT = (By.ID, "new_username_id")
PASSWORD_INPUT = (By.ID, "new_password_id")
```

### Adding New Tests
1. Add scenario to `features/login.feature`
2. Add test data to `tests/data/login.csv`
3. Implement test method in `tests/test_login.py`
4. Update `traceability.json`

### Extending Page Objects
For new pages, inherit from `BasePage`:

```python
from src.pages.base_page import BasePage

class DashboardPage(BasePage):
    # Define locators and methods
    pass
```

## Troubleshooting

### Driver Issues
- Ensure browser is installed and up to date
- Selenium 4.x manages drivers automatically
- For manual driver management, add driver to PATH

### Element Not Found
- Verify locators in page objects match actual UI
- Increase TIMEOUT if elements load slowly
- Check for dynamic content or iframes

### Test Failures
- Review test logs for detailed error messages
- Check screenshots (if screenshot-on-failure is enabled)
- Verify test data in CSV matches expected format
- Ensure BASE_URL is correct and accessible

### CI Failures
- Check GitHub Actions logs for specific errors
- Verify all environment variables are set
- Ensure dependencies are correctly specified in requirements.txt

## Security

- **No Credentials in Code**: All credentials are externalized
- **No Plain-Text Logging**: Audit logs never store plain-text passwords
- **Token Management**: GitHub tokens are used securely and never committed
- **Secrets Management**: Use environment variables or secret managers

## Non-Functional Requirements

- **Performance**: Login response time < 2 seconds
- **Availability**: System availability 99.9%
- **Accessibility**: WCAG 2.1 AA compliance
- **Security**: OWASP authentication guidelines compliance
- **Audit**: All login attempts logged without exposing credentials

## Best Practices

1. **Keep Tests Independent**: Each test should be self-contained
2. **Use Explicit Waits**: Avoid implicit waits for better control
3. **Maintain Page Objects**: Keep page logic separate from test logic
4. **Update Traceability**: Always map new tests to requirements
5. **Review Logs**: Regularly check logs for warnings and errors
6. **Run Locally First**: Test changes locally before pushing
7. **Document Changes**: Update README and comments for significant changes

## Future Enhancements

- Integration with Allure for advanced reporting
- Parallel test execution with pytest-xdist
- Visual regression testing
- API test integration
- Performance testing integration
- Extended accessibility testing with axe-core
- Multi-language support
- Database validation

## Support

For issues, questions, or contributions:
- Open an issue in the GitHub repository
- Review existing documentation
- Check troubleshooting section
- Contact the QA team

## License

This project is proprietary and confidential.

## Contributors

- Senior Automation and Quality Engineering Team

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Production-Ready