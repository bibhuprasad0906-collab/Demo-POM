"""Pytest fixtures and configuration.
Provides session-scoped fixtures for WebDriver, base URL, and test data loading."""

import pytest
import csv
import os
import logging
from datetime import datetime
from src.utils.driver_factory import get_driver
from src.utils.config import Config


# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    """Session-level setup: validate config and create directories."""
    logger.info("=" * 70)
    logger.info("Starting Test Session")
    logger.info("=" * 70)
    
    # Validate configuration
    try:
        Config.validate()
        Config.log_config()
    except Exception as e:
        logger.error(f"Configuration validation failed: {str(e)}")
        pytest.exit("Configuration validation failed")
    
    # Create directories
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    
    yield
    
    logger.info("=" * 70)
    logger.info("Test Session Completed")
    logger.info("=" * 70)


@pytest.fixture(scope="function")
def driver(request):
    """Function-scoped Selenium WebDriver fixture.
    
    Creates a new WebDriver instance for each test function.
    Automatically quits the driver after test completion.
    Takes screenshot on test failure if configured.
    """
    logger.info(f"Initializing driver for test: {request.node.name}")
    
    drv = get_driver()
    
    yield drv
    
    # Screenshot on failure
    if Config.SCREENSHOT_ON_FAILURE and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{request.node.name}_{timestamp}.png"
        screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_name)
        drv.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
    
    logger.info(f"Closing driver for test: {request.node.name}")
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for screenshot on failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def base_url():
    """Returns base URL from configuration.
    
    Returns:
        str: Base URL for the application under test
    """
    return Config.BASE_URL


@pytest.fixture(scope="session")
def login_data():
    """Loads login test data from CSV file.
    
    Returns:
        list: List of dictionaries containing test data
        
    Raises:
        FileNotFoundError: If CSV file not found
    """
    csv_path = os.path.join(Config.TEST_DATA_DIR, "login.csv")
    
    if not os.path.exists(csv_path):
        logger.error(f"Test data file not found: {csv_path}")
        pytest.exit(f"Test data file not found: {csv_path}")
    
    data = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        logger.info(f"Loaded {len(data)} test data records from {csv_path}")
        return data
    except Exception as e:
        logger.error(f"Failed to load test data: {str(e)}")
        pytest.exit(f"Failed to load test data: {str(e)}")


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")
    config.addinivalue_line("markers", "p1: Priority 1 tests")
    config.addinivalue_line("markers", "p2: Priority 2 tests")
    config.addinivalue_line("markers", "web: Web platform tests")
    config.addinivalue_line("markers", "mobile: Mobile platform tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add platform markers
        if "_web" in item.name.lower():
            item.add_marker(pytest.mark.web)
        if "_mobile" in item.name.lower():
            item.add_marker(pytest.mark.mobile)
        
        # Add priority markers based on test case ID
        if "AUTH-001" in item.name or "AUTH-002" in item.name or "AUTH-003" in item.name:
            item.add_marker(pytest.mark.p1)
            item.add_marker(pytest.mark.smoke)