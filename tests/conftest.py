"""Pytest configuration and fixtures for test automation framework.

Provides fixtures for:
    - WebDriver management
    - Test data loading
    - Screenshot capture on failure
    - Logging configuration
    - Performance monitoring

Hooks:
    - pytest_configure: Configure logging and directories
    - pytest_runtest_makereport: Capture screenshots on failure
    - pytest_generate_tests: Data-driven test parametrization
"""

import os
import csv
import logging
import pytest
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from src.utils.driver_factory import DriverFactory
from src.utils.config import Config


# Configure logging
def pytest_configure(config):
    """Configure pytest and create necessary directories.
    
    Args:
        config: Pytest config object
    """
    # Create directories
    for directory in [Config.LOGS_DIR, Config.SCREENSHOTS_DIR, Config.REPORTS_DIR]:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    log_file = os.path.join(Config.LOGS_DIR, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logging.info("=" * 80)
    logging.info("Test Execution Started")
    logging.info("=" * 80)
    Config.log_config()


def pytest_unconfigure(config):
    """Cleanup after test execution.
    
    Args:
        config: Pytest config object
    """
    logging.info("=" * 80)
    logging.info("Test Execution Completed")
    logging.info("=" * 80)


@pytest.fixture(scope="session")
def base_url() -> str:
    """Provide base URL for tests.
    
    Returns:
        str: Application base URL from config
    """
    return Config.BASE_URL


@pytest.fixture(scope="function")
def driver(request) -> WebDriver:
    """Provide WebDriver instance for each test.
    
    Yields:
        WebDriver: Configured WebDriver instance
    
    Note:
        Driver is automatically quit after test completion.
    """
    logging.info(f"Creating WebDriver for test: {request.node.name}")
    driver = DriverFactory.get_driver()
    driver.get(Config.BASE_URL)
    
    yield driver
    
    # Cleanup
    logging.info(f"Quitting WebDriver for test: {request.node.name}")
    DriverFactory.quit_driver(driver)


@pytest.fixture(scope="session")
def driver_session() -> WebDriver:
    """Provide WebDriver instance for entire test session.
    
    Yields:
        WebDriver: Configured WebDriver instance
    
    Note:
        Use this fixture for tests that can share a driver instance.
        Driver is automatically quit after session completion.
    """
    logging.info("Creating session-scoped WebDriver")
    driver = DriverFactory.get_driver()
    driver.get(Config.BASE_URL)
    
    yield driver
    
    # Cleanup
    logging.info("Quitting session-scoped WebDriver")
    DriverFactory.quit_driver(driver)


def load_csv_data(filename: str) -> List[Dict[str, str]]:
    """Load test data from CSV file.
    
    Args:
        filename: Name of CSV file in TEST_DATA_DIR
    
    Returns:
        List[Dict[str, str]]: List of test data dictionaries
    
    Raises:
        FileNotFoundError: If CSV file is not found
    """
    filepath = os.path.join(Config.TEST_DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        logging.error(f"Test data file not found: {filepath}")
        raise FileNotFoundError(f"Test data file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    
    logging.info(f"Loaded {len(data)} test data rows from {filename}")
    return data


def pytest_generate_tests(metafunc):
    """Generate parametrized tests from CSV data.
    
    Args:
        metafunc: Pytest metafunc object
    
    Note:
        Tests requesting 'login_data' fixture will be parametrized
        with data from tests/data/login.csv
    """
    if "login_data" in metafunc.fixturenames:
        try:
            data = load_csv_data("login.csv")
            metafunc.parametrize("login_data", data)
        except FileNotFoundError:
            logging.warning("login.csv not found, skipping parametrization")
            metafunc.parametrize("login_data", [])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure.
    
    Args:
        item: Pytest test item
        call: Pytest call object
    
    Note:
        Screenshots are saved to SCREENSHOTS_DIR with timestamp and test name.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        if Config.SCREENSHOT_ON_FAILURE:
            # Get driver from test fixtures
            driver = None
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
            elif "driver_session" in item.funcargs:
                driver = item.funcargs["driver_session"]
            
            if driver:
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    test_name = item.name.replace(" ", "_").replace("[", "_").replace("]", "")
                    screenshot_name = f"{test_name}_{timestamp}.png"
                    screenshot_path = os.path.join(Config.SCREENSHOTS_DIR, screenshot_name)
                    
                    driver.save_screenshot(screenshot_path)
                    logging.info(f"Screenshot captured: {screenshot_path}")
                    
                    # Attach screenshot to report (for HTML reports)
                    if hasattr(report, "extra"):
                        report.extra = getattr(report, "extra", [])
                        report.extra.append(pytest.html.extras.image(screenshot_path))
                
                except Exception as e:
                    logging.error(f"Failed to capture screenshot: {str(e)}")


@pytest.fixture
def test_data_login() -> List[Dict[str, str]]:
    """Provide login test data.
    
    Returns:
        List[Dict[str, str]]: Login test data from CSV
    """
    return load_csv_data("login.csv")


@pytest.fixture
def performance_monitor():
    """Monitor test performance.
    
    Yields:
        Dict: Performance metrics including start time and duration
    
    Example:
        >>> def test_example(performance_monitor):
        ...     # Test code
        ...     assert performance_monitor["duration"] < 5.0
    """
    import time
    metrics = {"start_time": time.time()}
    
    yield metrics
    
    metrics["end_time"] = time.time()
    metrics["duration"] = metrics["end_time"] - metrics["start_time"]
    logging.info(f"Test duration: {metrics['duration']:.2f}s")


# Pytest markers
def pytest_configure(config):
    """Register custom markers.
    
    Args:
        config: Pytest config object
    """
    config.addinivalue_line("markers", "smoke: Smoke tests for critical functionality")
    config.addinivalue_line("markers", "regression: Full regression test suite")
    config.addinivalue_line("markers", "auth: Authentication related tests")
    config.addinivalue_line("markers", "login: Login functionality tests")
    config.addinivalue_line("markers", "positive: Positive test scenarios")
    config.addinivalue_line("markers", "negative: Negative test scenarios")
    config.addinivalue_line("markers", "p1: Priority 1 - Critical tests")
    config.addinivalue_line("markers", "p2: Priority 2 - High priority tests")
    config.addinivalue_line("markers", "p3: Priority 3 - Medium priority tests")
    config.addinivalue_line("markers", "web: Web platform tests")
    config.addinivalue_line("markers", "mobile: Mobile platform tests")
    config.addinivalue_line("markers", "security: Security and compliance tests")