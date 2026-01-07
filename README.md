# Selenium Pytest Automation Suite

## Overview
This repository contains a production-ready, standards-compliant Selenium pytest automation codebase for testing login functionality across Web and Mobile platforms. The suite is designed for regulated and high-stakes industries, ensuring quality, compliance, and rapid release cycles.

## Features
- **Robust Page Object Model (POM)**: Modular, maintainable page objects with safe Selenium wrappers.
- **Parametrized Tests**: Data-driven tests using CSV files for comprehensive coverage.
- **Explicit Waits**: Stable locators and explicit waits for reliable test execution.
- **Cross-Browser Support**: Chrome and Firefox, with headless mode support.
- **Environment-Based Configuration**: Configurable via environment variables.
- **Screenshot-on-Failure**: Automatic screenshot capture on test failures.
- **Comprehensive Logging**: Detailed logs for debugging and audit trails.
- **Traceability**: Mapping between test cases and user stories.
- **CI/CD Integration**: GitHub Actions workflow for automated testing.

## Directory Structure
```
.
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
├── .github/
│   └── workflows/
│       └── ci.yml
├── traceability.json
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Chrome or Firefox browser
- ChromeDriver or GeckoDriver (ensure they are in your PATH)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/bibhuprasad0906-collab/Demo-POM.git
   cd Demo-POM
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
Set the following environment variables:
- `BASE_URL`: Base URL of the application (default: `http://localhost:8080`)
- `BROWSER`: Browser to use (`chrome` or `firefox`, default: `chrome`)
- `HEADLESS`: Run in headless mode (`true` or `false`, default: `true`)
- `TIMEOUT`: Implicit wait timeout in seconds (default: `10`)

Example:
```bash
export BASE_URL=http://localhost:8080
export BROWSER=chrome
export HEADLESS=true
export TIMEOUT=10
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test
```bash
pytest tests/test_login.py::TestLogin::test_AUTH_001_login_valid_web
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with HTML Report
```bash
pytest --html=report.html --self-contained-html
```

## Test Cases
The suite covers the following test cases:
- **AUTH-001**: Login with valid credentials on Web
- **AUTH-002**: Login with valid credentials on Mobile
- **AUTH-003**: Login with invalid credentials on Web
- **AUTH-004**: Login with invalid credentials on Mobile
- **AUTH-005**: Account lockout after repeated failed attempts on Web
- **AUTH-006**: Account lockout after repeated failed attempts on Mobile
- **AUTH-007**: Notification of locked account on Web
- **AUTH-008**: Notification of locked account on Mobile
- **AUTH-009**: Password visibility toggle on Web
- **AUTH-010**: Password visibility toggle on Mobile
- **AUTH-011**: Audit login attempts

## Traceability
The `traceability.json` file maps user stories to test cases for full traceability.

## CI/CD
The repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs tests on every push and pull request.

## Troubleshooting
- **ElementNotFoundError**: Check locator values and page load timing.
- **LoginFailedError**: Ensure test data matches backend state (e.g., locked users).
- **Driver errors**: Ensure browser drivers are installed and PATH is set.
- **Data mismatches**: Validate CSV data and story mapping.

## Maintenance
- Update locators in `src/pages/login_page.py` as per actual application.
- Add new scenarios by extending `tests/data/login.csv` and test methods.
- Ensure environment variables are set for `BASE_URL`, `BROWSER`, `HEADLESS`, `TIMEOUT`.

## Recommendations
- Integrate reporting (e.g., pytest-html).
- Extend audit log test with backend/API checks.
- Add accessibility checks (e.g., axe-selenium).
- Schedule nightly test runs and code reviews.
- Track coverage via pytest-cov and update traceability.json as stories evolve.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, please contact the QA team.
