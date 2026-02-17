# Testing Guide

## Overview
This guide provides comprehensive instructions for running, maintaining, and extending the Login Test Automation Suite.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Test Execution](#test-execution)
3. [Test Data Management](#test-data-management)
4. [Debugging](#debugging)
5. [Extending Tests](#extending-tests)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Chrome or Firefox browser
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
cd Demo-POM

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### First Test Run
```bash
# Set environment variables
export BASE_URL="https://example.com/login"
export BROWSER="chrome"
export HEADLESS="false"

# Run smoke tests
pytest -v -m smoke
```

## Test Execution

### Run All Tests
```bash
pytest
```

### Run by Priority
```bash
# Priority 1 tests only
pytest -v -m p1

# Priority 2 tests only
pytest -v -m p2
```

### Run by Platform
```bash
# Web tests only
pytest -v -m web

# Mobile tests only
pytest -v -m mobile
```

### Run by Test Type
```bash
# Smoke tests
pytest -v -m smoke

# Regression tests
pytest -v -m regression
```

### Run Specific Test
```bash
# By test name
pytest -v tests/test_login.py::TestLogin::test_AUTH_001_002_valid_login

# By story ID (using -k)
pytest -v -k "AUTH-001"
```

### Parallel Execution
```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel (4 workers)
pytest -v -n 4
```

### Generate HTML Report
```bash
pytest --html=report.html --self-contained-html
```

### Run with Coverage
```bash
pip install pytest-cov
pytest --cov=src --cov-report=html
```

## Test Data Management

### CSV Structure
Test data is stored in `tests/data/login.csv`:

```csv
username,password,expected,platform,story_id
valid_user_web,valid_pass,success,web,AUTH-001
```

### Adding New Test Data
1. Open `tests/data/login.csv`
2. Add new row with required fields
3. Update test parametrization if needed

### Data-Driven Testing
Tests automatically load data from CSV using the `login_data` fixture:

```python
@pytest.mark.parametrize("username,password,platform,story_id", [
    ("valid_user_web", "valid_pass", "web", "AUTH-001"),
])
def test_example(self, driver, base_url, username, password, platform, story_id):
    # Test implementation
    pass
```

## Debugging

### Run in Non-Headless Mode
```bash
export HEADLESS="false"
pytest -v -s
```

### Enable Verbose Logging
```bash
export LOG_LEVEL="DEBUG"
pytest -v -s --log-cli-level=DEBUG
```

### Capture Screenshots
Screenshots are automatically captured on test failure when `SCREENSHOT_ON_FAILURE=true`.

Manual screenshot:
```python
driver.save_screenshot("debug_screenshot.png")
```

### Use Debugger
```python
import pdb; pdb.set_trace()  # Add breakpoint
```

Run with debugger:
```bash
pytest -v -s --pdb
```

### Inspect Elements
```python
element = login_page.find_element(LoginPage.USERNAME_INPUT)
print(f"Element: {element.tag_name}")
print(f"Visible: {element.is_displayed()}")
print(f"Enabled: {element.is_enabled()}")
```

## Extending Tests

### Adding New Test Case

1. **Add to Gherkin feature file** (`features/login.feature`):
```gherkin
Scenario: AUTH-012_New_scenario
  Given precondition
  When action
  Then expected result
```

2. **Add test data** (`tests/data/login.csv`):
```csv
new_user,new_pass,expected,platform,AUTH-012
```

3. **Implement test** (`tests/test_login.py`):
```python
@pytest.mark.p1
def test_AUTH_012_new_scenario(self, driver, base_url):
    """Test new scenario (AUTH-012)."""
    login_page = LoginPage(driver)
    login_page.open(base_url)
    # Test implementation
    assert True
```

4. **Update traceability** (`traceability.json`):
```json
"AUTH-012": {
  "title": "New scenario",
  "test_functions": ["test_AUTH_012_new_scenario"],
  "test_file": "tests/test_login.py",
  "priority": "P1",
  "status": "automated"
}
```

### Adding New Page Object

1. **Create page class** (`src/pages/new_page.py`):
```python
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class NewPage(BasePage):
    # Locators
    ELEMENT = (By.ID, "element_id")
    
    def perform_action(self):
        self.click_element(self.ELEMENT)
```

2. **Update package** (`src/pages/__init__.py`):
```python
from src.pages.new_page import NewPage
__all__ = ["BasePage", "LoginPage", "NewPage"]
```

3. **Use in tests**:
```python
from src.pages.new_page import NewPage

def test_new_page(driver, base_url):
    new_page = NewPage(driver)
    new_page.perform_action()
```

### Adding New Locator

1. **Inspect element** in browser DevTools
2. **Choose stable locator strategy**:
   - Prefer: ID > Name > CSS > XPath
   - Avoid: text content, index-based

3. **Add to page object**:
```python
NEW_ELEMENT = (By.ID, "new_element_id")
# or
NEW_ELEMENT = (By.CSS_SELECTOR, ".class-name")
# or
NEW_ELEMENT = (By.XPATH, "//button[@data-testid='submit']")
```

## Best Practices

### Test Design
- ✅ One assertion per test (when possible)
- ✅ Clear, descriptive test names
- ✅ Comprehensive docstrings
- ✅ Proper test isolation
- ✅ Use fixtures for setup/teardown

### Page Objects
- ✅ One page object per page
- ✅ Encapsulate page interactions
- ✅ Use explicit waits
- ✅ Return page objects for chaining
- ✅ Avoid assertions in page objects

### Locators
- ✅ Use stable, unique locators
- ✅ Prefer data-testid attributes
- ✅ Avoid brittle XPath
- ✅ Document locator strategy
- ✅ Keep locators in page objects

### Data Management
- ✅ Externalize test data
- ✅ Use CSV for tabular data
- ✅ Use JSON for complex data
- ✅ Never hardcode credentials
- ✅ Use environment variables

### Error Handling
- ✅ Use custom exceptions
- ✅ Log errors with context
- ✅ Capture screenshots on failure
- ✅ Provide clear error messages
- ✅ Handle timeouts gracefully

### Code Quality
- ✅ Follow PEP 8 style guide
- ✅ Use type hints
- ✅ Write comprehensive docstrings
- ✅ Keep functions small and focused
- ✅ Use meaningful variable names

## Troubleshooting

### Common Issues

#### WebDriver Not Found
**Error**: `WebDriver not found` or `Driver executable not in PATH`

**Solution**: Selenium 4.x auto-manages drivers. Ensure:
- Internet connectivity
- Latest Selenium version: `pip install --upgrade selenium`

#### Element Not Found
**Error**: `ElementNotFoundError: Element not found: (By.ID, 'element_id')`

**Solutions**:
1. Verify element exists on page
2. Check locator is correct
3. Increase timeout: `find_element(locator, timeout=20)`
4. Use explicit wait:
   ```python
   wait = WebDriverWait(driver, 10)
   element = wait.until(EC.presence_of_element_located(locator))
   ```

#### Stale Element Reference
**Error**: `StaleElementReferenceException`

**Solution**: Re-locate element:
```python
try:
    element.click()
except StaleElementReferenceException:
    element = self.find_element(locator)
    element.click()
```

#### Timeout Errors
**Error**: `TimeoutException`

**Solutions**:
1. Increase timeout in config
2. Check page load performance
3. Verify network connectivity
4. Use explicit waits for dynamic content

#### Test Data Not Found
**Error**: `FileNotFoundError: tests/data/login.csv`

**Solution**: Ensure CSV file exists and path is correct:
```bash
ls -la tests/data/login.csv
```

#### Import Errors
**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running from project root:
```bash
pwd  # Should show project root
pytest  # Run from root
```

#### Browser Crashes
**Error**: Browser crashes or hangs

**Solutions**:
1. Update browser to latest version
2. Clear browser cache
3. Disable browser extensions
4. Increase system resources
5. Use headless mode

### Getting Help

1. **Check logs**: Review pytest output and log files
2. **Enable debug logging**: `export LOG_LEVEL=DEBUG`
3. **Run in non-headless mode**: `export HEADLESS=false`
4. **Capture screenshots**: Check `screenshots/` directory
5. **Review documentation**: README.md, docstrings
6. **Check GitHub Issues**: Search for similar problems
7. **Contact team**: Reach out to QA team or maintainers

## Performance Tips

### Speed Up Tests
1. **Use headless mode**: 20-30% faster
2. **Parallel execution**: `pytest -n 4`
3. **Optimize waits**: Use explicit waits, avoid sleep()
4. **Reuse browser session**: Use session-scoped fixtures
5. **Disable unnecessary features**: Images, CSS, JavaScript (when possible)

### Reduce Flakiness
1. **Use explicit waits**: Never use implicit waits + explicit waits together
2. **Stable locators**: Prefer data-testid over CSS/XPath
3. **Proper synchronization**: Wait for elements, not fixed delays
4. **Isolate tests**: No dependencies between tests
5. **Clean state**: Reset application state between tests

## Maintenance

### Regular Tasks
- **Weekly**: Review test results, update test data
- **Monthly**: Update dependencies, review coverage
- **Quarterly**: Refactor tests, update documentation
- **Annually**: Review test strategy, plan improvements

### Updating Dependencies
```bash
# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade selenium

# Update all packages
pip install --upgrade -r requirements.txt

# Freeze updated versions
pip freeze > requirements.txt
```

### Code Reviews
Before merging:
- ✅ All tests pass
- ✅ Code follows style guide
- ✅ Documentation updated
- ✅ Traceability updated
- ✅ No hardcoded credentials
- ✅ Screenshots reviewed (if any)

## Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

**Last Updated**: 2024-01-01
**Maintainer**: QA Automation Team