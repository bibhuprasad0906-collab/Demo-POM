"""Utilities package for test automation framework.

Provides configuration management, driver factory, custom exceptions,
and other utility functions for test automation.
"""

from src.utils.config import Config
from src.utils.driver_factory import DriverFactory, get_driver
from src.utils.exceptions import (
    AutomationFrameworkException,
    ElementNotFoundError,
    ElementNotInteractableError,
    LoginFailedError,
    AccountLockedError,
    PageLoadTimeoutError,
    ConfigurationError,
    DataValidationError,
    ScreenshotError,
    BrowserError,
    TestDataNotFoundError,
    PerformanceThresholdExceededError,
    sanitize_error_message
)

__all__ = [
    "Config",
    "DriverFactory",
    "get_driver",
    "AutomationFrameworkException",
    "ElementNotFoundError",
    "ElementNotInteractableError",
    "LoginFailedError",
    "AccountLockedError",
    "PageLoadTimeoutError",
    "ConfigurationError",
    "DataValidationError",
    "ScreenshotError",
    "BrowserError",
    "TestDataNotFoundError",
    "PerformanceThresholdExceededError",
    "sanitize_error_message"
]