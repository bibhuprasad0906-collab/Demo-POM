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
    drv = get_driver()
    yield drv
    drv.quit()

def pytest_generate_tests(metafunc):
    if "login_data" in metafunc.fixturenames:
        with open("tests/data/login.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
        metafunc.parametrize("login_data", data)