"""
Pytest fixtures for driver and data.
Includes CSV loader and pytest_generate_tests for data-driven tests.
"""

import pytest
import csv
import os
from src.utils.driver_factory import get_driver
from src.utils.config import Config

@pytest.fixture(scope="function")
def driver():
    """
    Provides a Selenium WebDriver instance for tests.
    """
    drv = get_driver()
    yield drv
    drv.quit()

@pytest.fixture(scope="session")
def base_url():
    """
    Provides the base URL for tests.
    """
    return Config.BASE_URL

@pytest.fixture(scope="session")
def login_data():
    """
    Loads login test data from CSV.
    """
    data = []
    csv_path = os.path.join(os.path.dirname(__file__), "data", "login.csv")
    if os.path.exists(csv_path):
        with open(csv_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    return data

def pytest_generate_tests(metafunc):
    """
    Parametrize tests using login_data fixture.
    """
    if "login_row" in metafunc.fixturenames:
        data = []
        csv_path = os.path.join(os.path.dirname(metafunc.module.__file__), "data", "login.csv")
        if os.path.exists(csv_path):
            with open(csv_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
        if data:
            metafunc.parametrize("login_row", data)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")