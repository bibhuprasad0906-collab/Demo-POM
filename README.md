# Selenium Login Test Automation Suite

## Overview

This is a production-ready, enterprise-grade Selenium pytest automation framework for testing authentication and login functionality across Web and Mobile platforms. The suite implements robust error handling, comprehensive traceability, and follows industry best practices for maintainability and scalability.

## Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Data-Driven Testing**: CSV-based test data for flexible parametrization
- **Cross-Browser Support**: Chrome and Firefox with headless mode
- **Robust Error Handling**: Custom exceptions and safe Selenium wrappers
- **Traceability**: Complete mapping from user stories to test cases
- **CI/CD Ready**: GitHub Actions workflow included
- **Comprehensive Logging**: Detailed logging for debugging and audit
- **WCAG 2.1 AA Compliance**: Accessibility testing support

## Test Coverage

This suite covers 12 authentication scenarios:

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

## Project Structure

```
Demo-POM/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI pipeline
├── features/
│   └── login.feature              # Gherkin scenarios
├── src/
│   ├── pages/
│   │   ├── base_page.py          # Base page object with safe wrappers
│   │   └── login_page.py         # Login page object
│   └── utils/
│       ├── config.py              # Configuration management
│       ├── driver_factory.py     # WebDriver instantiation
│       └── exceptions.py         # Custom exceptions
├── tests/
│   ├── data/
│   │   └── login.csv             # Test data
│   ├── conftest.py               # Pytest fixtures and hooks
│   └── test_login.py             # Login test suite
├── .gitignore                     # Git ignore rules
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
├── traceability.json             # Story-to-test mapping
└── README.md                      # This file
```

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
   - **Chrome**: Download ChromeDriver from https://chromedriver.chromium.org/
   - **Firefox**: Download GeckoDriver from https://github.com/mozilla/geckodriver/releases
   - Add the driver to your system PATH

## Configuration

The framework uses environment variables for configuration:

- **BASE_URL**: Application base URL (default: https://example.com)
- **BROWSER**: Browser to use - chrome or firefox (default: chrome)
- **HEADLESS**: Run in headless mode - true or false (default: true)
- **TIMEOUT**: Default timeout in seconds (default: 10)

### Setting Environment Variables

**Linux/Mac:**
```bash
export BASE_URL=https://your-app.com
export BROWSER=chrome
export HEADLESS=true
export TIMEOUT=10
```

**Windows:**
```cmd
set BASE_URL=https://your-app.com
set BROWSER=chrome
set HEADLESS=true
set TIMEOUT=10
```

## Usage

### Running All Tests

```bash
pytest
```

### Running Specific Tests

```bash
# Run a specific test file
pytest tests/test_login.py

# Run a specific test method
pytest tests/test_login.py::TestLogin::test_AUTH_001_login_valid_web

# Run tests by marker
pytest -m "web"
```

### Running with Different Browsers

```bash
# Chrome (default)
BROWSER=chrome pytest

# Firefox
BROWSER=firefox pytest

# Headless mode
HEADLESS=true pytest
```

### Generating Reports

```bash
# HTML report
pytest --html=report.html --self-contained-html

# JUnit XML report
pytest --junitxml=report.xml
```

## Test Data Management

Test data is stored in `tests/data/login.csv`. The CSV file contains:

- **username**: Test username
- **password**: Test password
- **expected**: Expected result (success, fail, lockout, locked)
- **platform**: Platform (web, mobile)
- **story**: Story ID (AUTH-001, etc.)

To add new test data:
1. Open `tests/data/login.csv`
2. Add a new row with the required fields
3. The test will automatically pick up the new data

## Page Object Model

### BasePage (src/pages/base_page.py)

Provides safe Selenium wrappers:
- `find_element(locator)`: Find element with explicit wait
- `click_element(locator)`: Safely click element
- `enter_text(locator, text)`: Enter text with clear
- `is_element_visible(locator)`: Check visibility
- `get_element_text(locator)`: Get element text

### LoginPage (src/pages/login_page.py)

Login-specific operations:
- `login(username, password)`: Perform login
- `is_dashboard_displayed()`: Check dashboard visibility
- `get_error_message()`: Get error message
- `get_lockout_message()`: Get lockout message
- `toggle_password_visibility()`: Toggle password visibility
- `is_password_visible()`: Check password visibility

## Traceability

The `traceability.json` file maps user stories to test cases:

```json
{
  "AUTH-001": ["test_AUTH_001_login_valid_web"],
  "AUTH-002": ["test_AUTH_002_login_valid_mobile"],
  ...
}
```

This ensures complete coverage and facilitates impact analysis when requirements change.

## CI/CD Integration

The suite includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. Runs on push and pull requests to main branch
2. Sets up Python 3.10
3. Installs dependencies
4. Runs tests in headless Chrome
5. Fails fast on first error

### Customizing CI/CD

Edit `.github/workflows/ci.yml` to:
- Change Python version
- Add different browsers
- Configure test reports
- Add deployment steps

## Troubleshooting

### Common Issues

**1. WebDriver not found**
- **Solution**: Ensure ChromeDriver/GeckoDriver is installed and in PATH
- **Verify**: Run `chromedriver --version` or `geckodriver --version`

**2. Element not found errors**
- **Solution**: Update locators in `src/pages/login_page.py` to match your application
- **Check**: Inspect your application's HTML and update locator IDs/classes

**3. Timeout errors**
- **Solution**: Increase TIMEOUT environment variable
- **Example**: `export TIMEOUT=20`

**4. Tests fail in headless mode**
- **Solution**: Run in headed mode for debugging
- **Example**: `HEADLESS=false pytest`

**5. CSV data not loading**
- **Solution**: Verify CSV file path and format
- **Check**: Ensure `tests/data/login.csv` exists and has correct headers

### Debug Mode

Run tests with verbose output:
```bash
pytest -v -s
```

Enable detailed logging:
```bash
pytest --log-cli-level=DEBUG
```

## Maintenance

### Updating Locators

1. Open `src/pages/login_page.py`
2. Update the locator tuples (e.g., `USERNAME_INPUT`, `PASSWORD_INPUT`)
3. Run tests to verify

### Adding New Test Cases

1. Add scenario to `features/login.feature`
2. Add test data to `tests/data/login.csv`
3. Add test method to `tests/test_login.py`
4. Update `traceability.json`
5. Run tests to verify

### Extending Page Objects

1. Create new page class in `src/pages/`
2. Inherit from `BasePage`
3. Define locators and methods
4. Use in test files

## Best Practices

1. **Never commit credentials**: Use environment variables or secure vaults
2. **Keep locators updated**: Review and update locators regularly
3. **Use explicit waits**: Avoid implicit waits and sleep statements
4. **Maintain traceability**: Update `traceability.json` with every change
5. **Run tests locally**: Before pushing to CI/CD
6. **Review test data**: Keep CSV data clean and relevant
7. **Document changes**: Update README and inline comments

## Security Considerations

- **No plain-text credentials**: Never store passwords in code or CSV
- **Token management**: Use GitHub secrets for CI/CD tokens
- **Audit compliance**: Ensure audit logs don't store plain-text credentials
- **Access control**: Restrict repository access to authorized personnel

## Accessibility Testing

The suite includes basic accessibility checks (AUTH-012). For comprehensive WCAG 2.1 AA compliance:

1. Integrate axe-core or pa11y
2. Add accessibility assertions
3. Run accessibility audits in CI/CD

## Performance Testing

The suite includes response time checks (AUTH-001, AUTH-002). For comprehensive performance testing:

1. Integrate Locust or JMeter
2. Add performance benchmarks
3. Monitor response times in CI/CD

## Support and Contribution

For issues, questions, or contributions:

1. Open an issue on GitHub
2. Submit a pull request with tests
3. Follow coding standards and conventions
4. Update documentation

## License

This project is licensed under the MIT License.

## Contact

For questions or support, contact the QA Engineering team.

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Maintained By**: Senior Automation and Quality Engineering Team