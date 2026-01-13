"""
Pytest fixtures and configuration.
Provides shared fixtures for driver management, test data loading, and hooks.
"""

import pytest
import csv
import os
import logging
from datetime import datetime
from src.utils.driver_factory import get_driver, quit_driver
from src.utils.config import Config

# Configure logging
log_dir = Config.LOG_DIR
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, Config.LOG_FILE)
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Create screenshot directory if it doesn't exist
if not os.path.exists(Config.SCREENSHOT_DIR):
    os.makedirs(Config.SCREENSHOT_DIR)

@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture for WebDriver.
    Creates a new driver instance for each test function.
    Automatically quits the driver after the test completes.
    
    Yields:
        WebDriver instance
    """
    logging.info("Initializing WebDriver for test")
    driver_instance = get_driver()
    
    yield driver_instance
    
    logging.info("Quitting WebDriver after test")
    quit_driver(driver_instance)

@pytest.fixture(scope="session")
def driver_session():
    """
    Pytest fixture for WebDriver with session scope.
    Creates a single driver instance for the entire test session.
    Use this for tests that don't modify browser state.
    
    Yields:
        WebDriver instance
    """
    logging.info("Initializing WebDriver for session")
    driver_instance = get_driver()
    
    yield driver_instance
    
    logging.info("Quitting WebDriver after session")
    quit_driver(driver_instance)

@pytest.fixture(scope="session")
def base_url():
    """
    Pytest fixture for base URL.
    
    Returns:
        Base URL from configuration
    """
    return Config.BASE_URL

@pytest.fixture(scope="session")
def test_data_dir():
    """
    Pytest fixture for test data directory.
    
    Returns:
        Test data directory path
    """
    return Config.TEST_DATA_DIR

def pytest_generate_tests(metafunc):
    """
    Pytest hook for dynamic test parametrization.
    Loads test data from CSV files and parametrizes tests.
    
    Args:
        metafunc: Pytest metafunc object
    """
    if "login_data" in metafunc.fixturenames:
        # Load login test data from CSV
        csv_path = os.path.join(Config.TEST_DATA_DIR, "login.csv")
        
        if not os.path.exists(csv_path):
            logging.warning(f"Test data file not found: {csv_path}")
            return
        
        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = [row for row in reader]
            
            if data:
                metafunc.parametrize("login_data", data)
                logging.info(f"Loaded {len(data)} test data rows from {csv_path}")
            else:
                logging.warning(f"No test data found in {csv_path}")
                
        except Exception as e:
            logging.error(f"Failed to load test data from {csv_path}: {str(e)}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture test results and take screenshots on failure.
    
    Args:
        item: Pytest test item
        call: Pytest call object
    """
    outcome = yield
    report = outcome.get_result()
    
    # Take screenshot on test failure
    if report.when == "call" and report.failed:
        if Config.SCREENSHOT_ON_FAILURE:
            try:
                # Get the driver fixture from the test
                driver_fixture = item.funcargs.get('driver') or item.funcargs.get('driver_session')
                
                if driver_fixture:
                    # Generate screenshot filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    test_name = item.name.replace(" ", "_").replace("[", "_").replace("]", "")
                    screenshot_name = f"{test_name}_{timestamp}.png"
                    screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_name)
                    
                    # Take screenshot
                    driver_fixture.save_screenshot(screenshot_path)
                    logging.info(f"Screenshot saved: {screenshot_path}")
                    
                    # Attach screenshot to report (for HTML reports)
                    if hasattr(report, 'extra'):
                        report.extra = getattr(report, 'extra', [])
                        report.extra.append(pytest_html.extras.image(screenshot_path))
                        
            except Exception as e:
                logging.error(f"Failed to take screenshot: {str(e)}")

def pytest_configure(config):
    """
    Pytest hook called before test collection.
    Prints configuration and sets up test environment.
    
    Args:
        config: Pytest config object
    """
    logging.info("="*80)
    logging.info("Starting test execution")
    logging.info("="*80)
    Config.print_config()

def pytest_sessionstart(session):
    """
    Pytest hook called at the start of the test session.
    
    Args:
        session: Pytest session object
    """
    logging.info("Test session started")

def pytest_sessionfinish(session, exitstatus):
    """
    Pytest hook called at the end of the test session.
    
    Args:
        session: Pytest session object
        exitstatus: Exit status code
    """
    logging.info("="*80)
    logging.info(f"Test session finished with exit status: {exitstatus}")
    logging.info("="*80)

def pytest_collection_modifyitems(config, items):
    """
    Pytest hook to modify collected test items.
    Can be used to add markers, skip tests, or reorder tests.
    
    Args:
        config: Pytest config object
        items: List of collected test items
    """
    logging.info(f"Collected {len(items)} test items")

# Optional: Add custom markers
def pytest_configure(config):
    """
    Register custom markers.
    """
    config.addinivalue_line("markers", "smoke: Mark test as smoke test")
    config.addinivalue_line("markers", "regression: Mark test as regression test")
    config.addinivalue_line("markers", "positive: Mark test as positive test case")
    config.addinivalue_line("markers", "negative: Mark test as negative test case")
    config.addinivalue_line("markers", "p1: Mark test as priority 1")
    config.addinivalue_line("markers", "p2: Mark test as priority 2")