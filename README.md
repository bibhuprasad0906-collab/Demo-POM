# Selenium Pytest Automation Framework

## Overview
Production-ready Selenium pytest automation framework for authentication testing with comprehensive Page Object Model (POM) architecture, data-driven testing, and CI/CD integration.

## Features
- **Page Object Model**: Maintainable, scalable page object architecture
- **Data-Driven Testing**: CSV-based test data management
- **Cross-Browser Support**: Chrome and Firefox with headless mode
- **Robust Error Handling**: Custom exceptions and comprehensive logging
- **CI/CD Integration**: GitHub Actions workflow for automated testing
- **Traceability**: Complete mapping between user stories and test cases
- **Security**: No plain-text credentials in logs, secure credential handling
- **Accessibility**: WCAG 2.1 AA compliance validation

## Project Structure
```
.
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── features/
│   └── login.feature           # Gherkin scenarios for traceability
├── src/
│   ├── pages/
│   │   ├── base_page.py        # Abstract base page with safe wrappers
│   │   └── login_page.py       # Login page object implementation
│   └── utils/
│       ├── config.py            # Environment-based configuration
│       ├── driver_factory.py   # WebDriver instantiation
│       └── exceptions.py       # Custom exceptions
├── tests/
│   ├── data/
│   │   └── login.csv           # Test data for parametrization
│   ├── conftest.py             # Pytest fixtures and configuration
│   └── test_login.py           # Login test suite
├── traceability.json           # Story-to-test mapping
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
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
export BASE_URL="http://localhost:8080"  # Application base URL
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

### Run specific test story:
```bash
pytest -m story="AUTH-001"
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

## Traceability

Complete traceability mapping is maintained in `traceability.json`, ensuring:
- User story to test case mapping
- Scenario to test function mapping
- Coverage analysis and gap identification

## CI/CD Integration

GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:
- Runs on every push and pull request
- Executes all tests in headless Chrome
- Fails fast on first error
- Provides test execution feedback

## Maintenance

### Adding New Test Cases:
1. Update `features/login.feature` with new Gherkin scenarios
2. Add test data to `tests/data/login.csv`
3. Implement test methods in `tests/test_login.py`
4. Update `traceability.json` with new mappings

### Updating Page Objects:
1. Modify locators in `src/pages/login_page.py` as per UI changes
2. Add new page objects in `src/pages/` for new features
3. Extend `base_page.py` for common functionality

### Updating Configuration:
1. Modify `src/utils/config.py` for new environment variables
2. Update `src/utils/driver_factory.py` for new browser support

## Troubleshooting

### Driver Errors:
- Ensure browser drivers are installed and in PATH
- Selenium 4.x automatically manages drivers via Selenium Manager
- For manual driver management, download from official sources

### Element Not Found:
- Verify locators in page objects match actual UI
- Increase timeout in config if page load is slow
- Check for dynamic content and add explicit waits

### Data Mismatches:
- Validate `tests/data/login.csv` for correct scenario mapping
- Ensure CSV headers match expected parameters
- Check for encoding issues in CSV file

### CI Failures:
- Verify environment variables in workflow file
- Check browser compatibility in CI environment
- Review test logs for specific failure reasons

## Best Practices

1. **Never commit credentials**: Use environment variables or secure vaults
2. **Keep locators updated**: Regular maintenance as UI evolves
3. **Use explicit waits**: Avoid implicit waits for better control
4. **Maintain traceability**: Update mapping with every test change
5. **Review logs**: Regular audit of test execution logs
6. **Code reviews**: Peer review for all test code changes
7. **Accessibility**: Validate WCAG 2.1 AA compliance
8. **Security**: Ensure no PII in logs or screenshots

## Recommendations

- **Reporting**: Integrate pytest-html or Allure for enhanced reporting
- **Accessibility**: Add axe-selenium-python for automated accessibility checks
- **Audit Logs**: Integrate with actual audit log API for AUTH-011 validation
- **Parallel Execution**: Use pytest-xdist for faster test execution
- **Coverage**: Track code coverage with pytest-cov
- **Monitoring**: Set up nightly test runs and alerting

## Support

For issues, questions, or contributions:
- Create an issue in the GitHub repository
- Follow contribution guidelines
- Maintain code quality and test coverage

## License

This project is licensed under the MIT License.

## Authors

Senior Automation and Quality Engineering Team

## Version History

- **1.0.0** (2024-06-01): Initial production release
  - Complete authentication test suite
  - Page Object Model architecture
  - CI/CD integration
  - Comprehensive documentation
