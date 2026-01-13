# Selenium Pytest Automation Framework - Login Module

## Overview
This is a production-ready, enterprise-grade Selenium pytest automation framework for testing login functionality across Web and Mobile platforms. The framework implements Page Object Model (POM), data-driven testing, robust error handling, and comprehensive traceability.

## Features
- **Page Object Model (POM)**: Clean separation of page logic and test logic
- **Data-Driven Testing**: CSV-based test data for easy maintenance
- **Cross-Browser Support**: Chrome and Firefox with headless mode
- **Robust Error Handling**: Custom exceptions and safe Selenium wrappers
- **Traceability**: Complete mapping between user stories, scenarios, and test cases
- **CI/CD Ready**: GitHub Actions workflow included
- **Accessibility Testing**: WCAG 2.1 AA compliance validation
- **Security**: No plain-text credential storage, secure audit logging

## Project Structure
```
Demo-POM/
├── README.md
├── requirements.txt
├── .gitignore
├── pytest.ini
├── traceability.json
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
└── .github/
    └── workflows/
        └── ci.yml
```

## Prerequisites
- Python 3.8+
- Chrome/Firefox browser
- ChromeDriver/GeckoDriver (automatically managed by Selenium 4.x)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
cd Demo-POM
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Set environment variables for test execution:

```bash
export BASE_URL="http://localhost:8080"  # Application URL
export BROWSER="chrome"                   # chrome or firefox
export HEADLESS="true"                    # true or false
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

### Run with verbose output:
```bash
pytest -v
```

### Run specific test by ID:
```bash
pytest tests/test_login.py::TestLogin::test_AUTH_001_002_valid_login
```

### Run in headless mode:
```bash
HEADLESS=true pytest
```

### Generate HTML report:
```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

## Test Coverage

This framework covers 13 authentication scenarios:

| Story ID | Test Case | Priority | Type |
|----------|-----------|----------|------|
| AUTH-001 | Login with valid credentials on Web | P1 | Positive |
| AUTH-002 | Login with valid credentials on Mobile | P1 | Positive |
| AUTH-003 | Login with invalid credentials on Web | P1 | Negative |
| AUTH-004 | Login with invalid credentials on Mobile | P1 | Negative |
| AUTH-005 | Account lockout after repeated failed attempts on Web | P1 | Negative |
| AUTH-006 | Account lockout after repeated failed attempts on Mobile | P1 | Negative |
| AUTH-007 | Display lockout message for locked user on Web | P1 | Negative |
| AUTH-008 | Display lockout message for locked user on Mobile | P1 | Negative |
| AUTH-009 | Password visibility toggle on Web | P2 | Functional |
| AUTH-010 | Password visibility toggle on Mobile | P2 | Functional |
| AUTH-011 | Audit login attempts for compliance | P1 | Security |
| AUTH-012 | Accessibility compliance for login on Web | P2 | Accessibility |
| AUTH-013 | Accessibility compliance for login on Mobile | P2 | Accessibility |

## Traceability

Complete traceability mapping is maintained in `traceability.json`, linking:
- User Stories → Test Scenarios → Test Cases → Test Methods

View traceability:
```bash
cat traceability.json
```

## CI/CD Integration

GitHub Actions workflow is configured in `.github/workflows/ci.yml`:
- Triggers on push/pull request to main branch
- Runs tests in headless Chrome
- Fails fast on first error
- Python 3.10 on Ubuntu latest

## Troubleshooting

### Driver Issues
**Problem**: WebDriver not found
**Solution**: Selenium 4.x manages drivers automatically. Ensure you have the latest version:
```bash
pip install --upgrade selenium
```

### Element Not Found
**Problem**: ElementNotFoundError raised
**Solution**: 
1. Verify locators in `src/pages/login_page.py` match your application
2. Increase timeout in config: `export TIMEOUT=20`
3. Check if element is in iframe or shadow DOM

### Test Data Issues
**Problem**: CSV data not loading
**Solution**: Verify `tests/data/login.csv` exists and has correct format:
```csv
username,password,expected,platform,story_id
validUserWeb,validPassWeb,success,web,AUTH-001
```

### Headless Mode Failures
**Problem**: Tests pass in headed mode but fail in headless
**Solution**: 
1. Add explicit waits instead of implicit waits
2. Increase window size in driver_factory.py
3. Check for JavaScript-dependent elements

## Maintenance Guidelines

### Adding New Test Cases
1. Add test data row in `tests/data/login.csv`
2. Create test method in `tests/test_login.py`
3. Update `traceability.json` with new mapping
4. Update this README with new test case details

### Updating Page Objects
1. Modify locators in `src/pages/login_page.py`
2. Add new methods for new UI interactions
3. Ensure all methods use BasePage wrappers
4. Add error handling for new operations

### Extending to New Modules
1. Create new feature file in `features/`
2. Create new page object in `src/pages/`
3. Create new test file in `tests/`
4. Add test data in `tests/data/`
5. Update traceability mapping

## Best Practices

1. **Never hardcode credentials**: Use environment variables or secure vaults
2. **Use explicit waits**: Avoid implicit waits for better control
3. **Maintain traceability**: Update traceability.json with every test change
4. **Follow POM**: Keep page logic separate from test logic
5. **Data-driven approach**: Externalize test data for easy maintenance
6. **Robust error handling**: Use custom exceptions for clear error messages
7. **Accessibility first**: Include accessibility checks in all UI tests
8. **Security compliance**: Never log or store plain-text credentials

## Non-Functional Requirements

- **Performance**: Login response time < 2 seconds
- **Security**: No plain-text credential storage in logs or audit trails
- **Accessibility**: WCAG 2.1 AA compliance for all UI elements
- **Availability**: System availability 99.9%
- **Auditability**: All login attempts logged without exposing credentials

## Support and Contribution

For issues, questions, or contributions:
1. Open an issue on GitHub
2. Submit a pull request with detailed description
3. Follow existing code style and conventions
4. Include tests for new features
5. Update documentation accordingly

## License

This project is licensed under the MIT License.

## Contact

Maintainer: Senior Automation and Quality Engineering Team
Repository: https://github.com/bibhuprasad0906-collab/Demo-POM

---

**Last Updated**: 2024
**Framework Version**: 1.0.0
**Selenium Version**: 4.x
**Pytest Version**: 7.x