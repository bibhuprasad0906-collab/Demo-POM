# Selenium Pytest Automation Framework

## Overview

This is a production-ready, enterprise-grade test automation framework built with Selenium WebDriver and pytest. The framework implements the Page Object Model (POM) design pattern and provides comprehensive test coverage for authentication and login functionality.

## Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Pytest Framework**: Robust test execution with fixtures, markers, and hooks
- **Multi-Browser Support**: Chrome and Firefox with headless mode
- **Screenshot on Failure**: Automatic screenshot capture for failed tests
- **Comprehensive Logging**: Detailed execution logs for debugging and audit
- **Traceability**: Complete mapping between user stories and test cases
- **CI/CD Ready**: GitHub Actions workflow for automated testing
- **Security Compliant**: No credential leakage, secure handling of sensitive data
- **WCAG 2.1 AA Compliance**: Accessibility testing support

## Project Structure

```
Demo-POM/
├── tests/
│   ├── conftest.py              # Pytest fixtures and configuration
│   ├── test_login.py            # Login test cases (AUTH-001 to AUTH-012)
│   └── data/
│       └── login.csv            # Test data for data-driven testing
├── src/
│   ├── pages/
│   │   ├── base_page.py         # Base page object class
│   │   └── login_page.py        # Login page object
│   └── utils/
│       ├── config.py             # Configuration management
│       ├── driver_factory.py    # WebDriver factory
│       └── exceptions.py        # Custom exceptions
├── logs/                         # Test execution logs (auto-generated)
├── screenshots/                  # Failure screenshots (auto-generated)
├── features/
│   └── login.feature            # Gherkin feature files
├── .github/
│   └── workflows/
│       └── ci.yml               # CI/CD pipeline configuration
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
├── .gitignore                    # Git ignore rules
├── traceability.json            # Test case traceability mapping
└── README.md                     # This file
```

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Chrome or Firefox browser
- ChromeDriver or GeckoDriver (automatically managed by webdriver-manager)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
cd Demo-POM
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Set the following environment variables to configure test execution:

```bash
# Application URL
export BASE_URL="http://localhost:8080"

# Browser selection (chrome or firefox)
export BROWSER="chrome"

# Headless mode (true or false)
export HEADLESS="true"

# Timeout in seconds
export TIMEOUT="10"
```

### pytest.ini Configuration

The `pytest.ini` file contains pytest-specific configuration:

```ini
[pytest]
markers =
    story: User story ID
    priority: Test priority (P1, P2, P3)
    smoke: Smoke tests
    regression: Regression tests

addopts =
    -v
    --tb=short
    --strict-markers
    --html=reports/report.html
    --self-contained-html
```

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test File

```bash
pytest tests/test_login.py
```

### Run Tests by Story ID

```bash
pytest -m "story('AUTH-001')"
```

### Run Tests by Priority

```bash
pytest -m "priority('P1')"
```

### Run Tests with Custom Browser

```bash
pytest --browser=firefox tests/
```

### Run Tests in Headless Mode

```bash
pytest --headless=true tests/
```

### Run Tests with HTML Report

```bash
pytest --html=reports/report.html --self-contained-html tests/
```

### Run Tests in Parallel

```bash
pytest -n 4 tests/  # Run with 4 workers
```

## Test Coverage

### Authentication Test Cases

| Test ID | Story ID | Description | Priority |
|---------|----------|-------------|----------|
| test_AUTH_001_valid_login_web | AUTH-001 | Login with valid credentials on Web | P1 |
| test_AUTH_002_valid_login_mobile | AUTH-002 | Login with valid credentials on Mobile | P1 |
| test_AUTH_003_invalid_login_web | AUTH-003 | Login with invalid credentials on Web | P1 |
| test_AUTH_004_invalid_login_mobile | AUTH-004 | Login with invalid credentials on Mobile | P1 |
| test_AUTH_005_account_lockout_web | AUTH-005 | Account lockout after failed attempts on Web | P1 |
| test_AUTH_006_account_lockout_mobile | AUTH-006 | Account lockout after failed attempts on Mobile | P1 |
| test_AUTH_007_locked_user_login_web | AUTH-007 | Locked user login attempt on Web | P1 |
| test_AUTH_008_locked_user_login_mobile | AUTH-008 | Locked user login attempt on Mobile | P1 |
| test_AUTH_009_password_visibility_toggle_web | AUTH-009 | Password visibility toggle on Web | P2 |
| test_AUTH_010_password_visibility_toggle_mobile | AUTH-010 | Password visibility toggle on Mobile | P2 |
| test_AUTH_011_audit_login_events | AUTH-011 | Audit login events for compliance | P1 |
| test_AUTH_012_monitor_account_lockout_events | AUTH-012 | Monitor account lockout events | P2 |

## Traceability Matrix

The `traceability.json` file provides complete mapping between user stories, scenarios, and test cases:

```json
{
  "AUTH-001": ["test_AUTH_001_valid_login_web"],
  "AUTH-002": ["test_AUTH_002_valid_login_mobile"],
  "AUTH-003": ["test_AUTH_003_invalid_login_web"],
  ...
}
```

## CI/CD Integration

### GitHub Actions

The framework includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

- Runs on every push and pull request
- Sets up Python environment
- Installs dependencies
- Executes tests in headless Chrome
- Generates test reports
- Archives screenshots and logs

### Running CI Pipeline Locally

```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS

# Run workflow locally
act push
```

## Logging and Reporting

### Logs

Test execution logs are stored in `logs/test_execution.log` with the following format:

```
2024-01-15 10:30:45 - conftest - INFO - Test execution started
2024-01-15 10:30:46 - conftest - INFO - Initializing chrome driver (headless=True)
2024-01-15 10:30:50 - test_login - INFO - Running test_AUTH_001_valid_login_web
```

### Screenshots

Screenshots are automatically captured on test failure and stored in `screenshots/` with timestamp:

```
screenshots/test_AUTH_003_invalid_login_web_20240115_103050.png
```

### HTML Reports

Generate HTML reports using pytest-html:

```bash
pytest --html=reports/report.html --self-contained-html tests/
```

## Security and Compliance

### Credential Management

- **No hardcoded credentials**: All credentials are externalized
- **Environment variables**: Sensitive data via environment variables
- **Audit logging**: No plain-text credentials in logs
- **Secure transmission**: HTTPS for production environments

### Compliance

- **WCAG 2.1 AA**: Accessibility compliance testing
- **Audit trails**: Complete traceability of test execution
- **Data privacy**: No PII in logs or screenshots
- **System availability**: 99.9% uptime validation

## Troubleshooting

### Common Issues

#### 1. WebDriver Not Found

**Error**: `selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH`

**Solution**: The framework uses `webdriver-manager` to automatically download and manage drivers. Ensure it's installed:

```bash
pip install webdriver-manager
```

#### 2. Element Not Found

**Error**: `ElementNotFoundError: Element not found: (By.ID, 'username')`

**Solution**: 
- Verify the application is running at the configured BASE_URL
- Check that element locators in page objects match the actual UI
- Increase timeout in `src/utils/config.py`

#### 3. Tests Fail in Headless Mode

**Error**: Tests pass in headed mode but fail in headless

**Solution**:
- Add explicit waits for dynamic content
- Increase window size in headless options
- Check for JavaScript errors in console logs

#### 4. Permission Denied on Screenshots

**Error**: `PermissionError: [Errno 13] Permission denied: 'screenshots/'`

**Solution**:
```bash
mkdir -p screenshots logs
chmod 755 screenshots logs
```

## Best Practices

### Test Design

1. **Atomic Tests**: Each test should be independent and self-contained
2. **Explicit Waits**: Use WebDriverWait instead of implicit waits for dynamic elements
3. **Stable Locators**: Prefer ID and data-testid over XPath and CSS selectors
4. **Error Handling**: Implement robust error handling and meaningful error messages
5. **Test Data**: Externalize test data in CSV or JSON files

### Code Quality

1. **PEP 8**: Follow Python style guide
2. **Docstrings**: Document all classes and methods
3. **Type Hints**: Use type annotations for better code clarity
4. **Code Review**: All changes require peer review
5. **Linting**: Run pylint and flake8 before committing

### Maintenance

1. **Regular Updates**: Keep dependencies up-to-date
2. **Refactoring**: Continuously improve code quality
3. **Documentation**: Update README and inline docs
4. **Traceability**: Maintain traceability matrix
5. **Monitoring**: Review logs and reports regularly

## Contributing

### Development Workflow

1. Create a feature branch from `main`
2. Implement changes with tests
3. Run tests locally and ensure all pass
4. Commit with descriptive messages
5. Push and create pull request
6. Address review comments
7. Merge after approval

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Example**:
```
feat(login): Add password visibility toggle test

Implemented test_AUTH_009 to validate password visibility toggle
functionality on web login page.

Closes #123
```

## Support and Contact

For questions, issues, or contributions:

- **GitHub Issues**: https://github.com/bibhuprasad0906-collab/Demo-POM/issues
- **Email**: support@example.com
- **Documentation**: https://github.com/bibhuprasad0906-collab/Demo-POM/wiki

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Selenium WebDriver team
- pytest community
- All contributors and maintainers

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Maintained by**: QA Engineering Team
