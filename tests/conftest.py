"""
Pytest fixtures for driver and data.
Includes CSV loader and pytest hooks for screenshots and logging.
"""

import pytest
import csv
import os
import logging
from datetime import datetime
from src.utils.driver_factory import get_driver, quit_driver
from src.utils.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(Config.LOG_DIR, 'test_execution.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def config():
    """Provide Config object to tests."""
    logger.info("Test session started")
    logger.info(f"Configuration: {Config.get_config_summary()}")
    return Config

@pytest.fixture(scope="function")
def driver(config):
    """Provide WebDriver instance for each test function."""
    logger.info("Initializing WebDriver for test")
    driver_instance = get_driver()
    yield driver_instance
    logger.info("Tearing down WebDriver")
    quit_driver(driver_instance)

@pytest.fixture(scope="session", autouse=True)
def setup_test_directories():
    """Create necessary directories for screenshots and logs."""
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    logger.info(f"Test directories created: {Config.SCREENSHOT_DIR}, {Config.LOG_DIR}")

def pytest_configure(config):
    """Pytest configuration hook."""
    # Add custom markers
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "p1: mark test as priority 1")
    config.addinivalue_line("markers", "p2: mark test as priority 2")
    config.addinivalue_line("markers", "web: mark test as web platform test")
    config.addinivalue_line("markers", "mobile: mark test as mobile platform test")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and take screenshots on failure."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        if Config.SCREENSHOT_ON_FAILURE:
            # Get driver from test fixture
            driver = item.funcargs.get('driver')
            if driver:
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_name = f"{item.name}_{timestamp}.png"
                    screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_name)
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"Screenshot saved: {screenshot_path}")
                    
                    # Attach screenshot to report (for HTML reports)
                    if hasattr(report, 'extra'):
                        report.extra = getattr(report, 'extra', [])
                        report.extra.append(pytest.html.extras.image(screenshot_path))
                except Exception as e:
                    logger.error(f"Failed to capture screenshot: {str(e)}")

def pytest_generate_tests(metafunc):
    """Generate parametrized tests from CSV data."""
    if "login_data" in metafunc.fixturenames:
        csv_path = "tests/data/login.csv"
        if os.path.exists(csv_path):
            with open(csv_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                data = [row for row in reader]
            
            # Filter data based on test function name if needed
            test_name = metafunc.function.__name__
            if "AUTH" in test_name:
                # Extract story ID from test name (e.g., test_AUTH_001_login_valid_web -> AUTH-001)
                story_id = test_name.split('_')[1] + '-' + test_name.split('_')[2]
                filtered_data = [row for row in data if row.get('story') == story_id]
                if filtered_data:
                    metafunc.parametrize("login_data", filtered_data)
                else:
                    metafunc.parametrize("login_data", data)
            else:
                metafunc.parametrize("login_data", data)
        else:
            logger.warning(f"CSV file not found: {csv_path}")

@pytest.fixture(scope="session")
def test_data():
    """Load all test data from CSV."""
    csv_path = "tests/data/login.csv"
    if os.path.exists(csv_path):
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    return []

def pytest_sessionfinish(session, exitstatus):
    """Hook called after test session finishes."""
    logger.info(f"Test session finished with exit status: {exitstatus}")
    logger.info("=" * 80)