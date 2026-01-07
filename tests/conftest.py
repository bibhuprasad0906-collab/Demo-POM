"""
Pytest fixtures for driver and data.
Includes CSV loader and pytest_generate_tests for parametrization.
"""

import pytest
import csv
from src.utils.driver_factory import get_driver
from src.utils.config import Config

@pytest.fixture(scope="session")
def driver():
    """
    Fixture to initialize and quit WebDriver.
    """
    drv = get_driver()
    yield drv
    drv.quit()

@pytest.fixture(scope="session")
def base_url():
    """
    Fixture to provide base URL.
    """
    return Config.BASE_URL

@pytest.fixture(scope="session")
def login_data():
    """
    Loads login test data from CSV.
    """
    data = []
    with open("tests/data/login.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def pytest_generate_tests(metafunc):
    """
    Parametrize tests using login_data fixture.
    """
    if "login_record" in metafunc.fixturenames:
        data = []
        with open("tests/data/login.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        metafunc.parametrize("login_record", data)
