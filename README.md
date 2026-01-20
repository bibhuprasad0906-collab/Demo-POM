# Selenium Pytest Automation Framework - Login Module

## Overview

This is a production-ready, enterprise-grade Selenium pytest automation framework for testing login functionality across web and mobile platforms. The framework implements robust error handling, secure credential management, comprehensive logging, and full traceability between test cases and user stories.

## Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Data-Driven Testing**: CSV-based test data management
- **Cross-Browser Support**: Chrome and Firefox with headless mode
- **Robust Error Handling**: Custom exceptions and comprehensive logging
- **Security**: No plain-text credential storage, secure token handling
- **Traceability**: Complete mapping between stories, scenarios, and test cases
- **CI/CD Ready**: GitHub Actions workflow included
- **Accessibility**: WCAG 2.1 AA compliance considerations
- **Performance Monitoring**: Response time tracking and validation

## Project Structure

```
Demo-POM/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD pipeline
├── features/
│   └── login.feature              # Gherkin feature file for documentation
├── src/
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py           # Abstract base page with safe Selenium wrappers
│   │   └── login_page.py          # Login page object with all login operations
│   └── utils/
│       ├── __init__.py
│       ├── config.py               # Configuration management
│       ├── driver_factory.py      # WebDriver factory
│       └── exceptions.py          # Custom exceptions
├── tests/
│   ├── data/
│   │   └── login.csv              # Test data for login scenarios
│   ├── conftest.py                # Pytest fixtures and hooks
│   └── test_login.py              # Login test cases
├── logs/                          # Test execution logs (git-ignored)
├── screenshots/                   # Failure screenshots (git-ignored)
├── .gitignore                     # Git ignore rules
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
├── traceability.json              # Story-to-test mapping
└── README.md                      # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Chrome/Firefox browser
- ChromeDriver/GeckoDriver (automatically managed by selenium 4.x)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
   cd Demo-POM
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The framework uses environment variables for configuration. Set the following variables before running tests:

| Variable | Description | Default |
|----------|-------------|----------|
| `BASE_URL` | Application base URL | `http://localhost:8080` |
| `BROWSER` | Browser to use (chrome/firefox) | `chrome` |
| `HEADLESS` | Run in headless mode (true/false) | `true` |
| `TIMEOUT` | Default timeout in seconds | `10` |

**Example:**
```bash
export BASE_URL="https://your-app.com"
export BROWSER="chrome"
export HEADLESS="false"
export TIMEOUT="15"
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

### Run specific test case:
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

### Run in parallel (requires pytest-xdist):
```bash
pytest -n auto
```

## Test Coverage

This framework covers the following authentication scenarios:

### Web Platform:
- **AUTH-001**: Login with valid credentials
- **AUTH-003**: Login with invalid credentials
- **AUTH-005**: Account lockout after repeated failed attempts
- **AUTH-007**: Locked user login attempt
- **AUTH-009**: Password visibility toggle

### Mobile Platform:
- **AUTH-002**: Login with valid credentials
- **AUTH-004**: Login with invalid credentials
- **AUTH-006**: Account lockout after repeated failed attempts
- **AUTH-008**: Locked user login attempt
- **AUTH-010**: Password visibility toggle

### Security & Compliance:
- **AUTH-011**: Audit login attempts (no plain-text credentials)

## Test Data Management

Test data is stored in `tests/data/login.csv` with the following structure:

```csv
username,password,expected,story
valid_user_web,valid_pass,success,AUTH-001
invalid_user,invalid_pass,fail,AUTH-003
```

**Important:** Never commit real credentials to version control. Use placeholder values and configure actual credentials via environment variables or secure vaults in production.

## Traceability

The `traceability.json` file maintains a complete mapping between user stories and test cases:

```json
{
  "AUTH-001": ["test_AUTH_001_login_valid_web"],
  "AUTH-002": ["test_AUTH_002_login_valid_mobile"]
}
```

This ensures full traceability for compliance and audit purposes.

## CI/CD Integration

The framework includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. Runs on every push and pull request to main branch
2. Sets up Python environment
3. Installs dependencies
4. Executes tests in headless Chrome
5. Reports results

## Extending the Framework

### Adding New Page Objects:

1. Create a new file in `src/pages/`
2. Inherit from `BasePage`
3. Define locators as class variables
4. Implement page-specific methods

```python
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class DashboardPage(BasePage):
    WELCOME_MESSAGE = (By.ID, "welcome")
    
    def get_welcome_message(self):
        return self.find_element(self.WELCOME_MESSAGE).text
```

### Adding New Test Cases:

1. Add test data to appropriate CSV file
2. Create test method in relevant test class
3. Use `@pytest.mark.parametrize` for data-driven tests
4. Update `traceability.json`

```python
@pytest.mark.parametrize("login_data", [
    {"username": "user", "password": "pass", "expected": "success", "story": "AUTH-012"},
])
def test_AUTH_012_new_scenario(self, driver, login_data):
    """Test AUTH-012: New login scenario."""
    # Test implementation
    pass
```

## Troubleshooting

### Common Issues:

1. **WebDriver not found:**
   - Selenium 4.x manages drivers automatically
   - Ensure you have the latest selenium version
   - Check internet connectivity for driver download

2. **Element not found errors:**
   - Verify locators match your application's DOM
   - Update locators in page objects as needed
   - Increase timeout if elements load slowly

3. **Login failures:**
   - Check `BASE_URL` is correct and accessible
   - Verify test data in `login.csv`
   - Review application logs for backend issues

4. **CI/CD failures:**
   - Ensure `BASE_URL` is reachable from CI environment
   - Check for environment-specific issues
   - Review GitHub Actions logs for details

## Security Considerations

- **Never commit credentials:** Use environment variables or secret management
- **Token handling:** Tokens are used in-memory only, never persisted
- **Audit logs:** Framework ensures no plain-text credentials in logs
- **Access control:** Limit repository access to authorized personnel

## Performance Monitoring

- Login response times are tracked and validated (< 2 seconds)
- Warnings logged for slow operations
- Performance metrics can be extended via custom fixtures

## Compliance

- **WCAG 2.1 AA**: Accessibility considerations in test design
- **OWASP**: Authentication security best practices
- **Audit trails**: Complete traceability for regulatory compliance

## Maintenance

### Regular Tasks:

1. **Update dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Review and update locators** as application UI changes

3. **Update test data** to reflect current test scenarios

4. **Review traceability** and update mappings for new stories

5. **Monitor CI/CD** pipeline health and address failures promptly

## Support and Contact

For issues, questions, or contributions:

- **Repository:** https://github.com/bibhuprasad0906-collab/Demo-POM
- **Issues:** https://github.com/bibhuprasad0906-collab/Demo-POM/issues

## License

This framework is provided as-is for internal use. All rights reserved.

## Version History

- **v1.0.0** (2024): Initial release with complete login module coverage

---

**Note:** This framework is designed for enterprise-grade quality assurance with emphasis on security, traceability, and maintainability. Always follow your organization's security policies and compliance requirements when using this framework.