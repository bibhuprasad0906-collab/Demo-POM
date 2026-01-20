"""Custom exceptions for UI test automation framework.

Provides specific exception types for different failure scenarios,
enabling precise error handling and reporting.

All exceptions include detailed error messages and optional context
for debugging and troubleshooting.
"""

import logging
from typing import Optional, Any


class AutomationFrameworkException(Exception):
    """Base exception for all automation framework errors.
    
    All custom exceptions should inherit from this base class
    to enable unified exception handling.
    """
    
    def __init__(self, message: str, context: Optional[dict] = None):
        """Initialize exception with message and optional context.
        
        Args:
            message: Human-readable error message
            context: Optional dictionary with additional error context
        """
        self.message = message
        self.context = context or {}
        super().__init__(self.message)
        logging.error(f"{self.__class__.__name__}: {message}")
        if context:
            logging.debug(f"Error context: {context}")


class ElementNotFoundError(AutomationFrameworkException):
    """Raised when a UI element cannot be located.
    
    This exception indicates that a web element could not be found
    using the specified locator within the configured timeout period.
    
    Common causes:
    - Incorrect locator strategy or value
    - Element not yet rendered (timing issue)
    - Element removed from DOM
    - Page not fully loaded
    
    Example:
        >>> raise ElementNotFoundError(
        ...     "Login button not found",
        ...     context={"locator": (By.ID, "loginBtn"), "timeout": 10}
        ... )
    """
    pass


class ElementNotInteractableError(AutomationFrameworkException):
    """Raised when an element exists but cannot be interacted with.
    
    This exception indicates that an element was found but could not
    be clicked, typed into, or otherwise interacted with.
    
    Common causes:
    - Element is hidden or obscured
    - Element is disabled
    - Element is outside viewport
    - Overlay or modal blocking interaction
    
    Example:
        >>> raise ElementNotInteractableError(
        ...     "Submit button is disabled",
        ...     context={"element_id": "submitBtn", "state": "disabled"}
        ... )
    """
    pass


class LoginFailedError(AutomationFrameworkException):
    """Raised when login operation fails.
    
    This exception indicates that a login attempt was unsuccessful,
    either due to invalid credentials, account lockout, or system error.
    
    Security Note:
        Never include actual credentials in error messages or context.
        Use sanitized identifiers only.
    
    Common causes:
    - Invalid username or password
    - Account locked due to failed attempts
    - Account disabled or expired
    - Authentication service unavailable
    
    Example:
        >>> raise LoginFailedError(
        ...     "Login failed: Invalid credentials",
        ...     context={"username": "user***", "attempt": 3}
        ... )
    """
    pass


class AccountLockedError(LoginFailedError):
    """Raised when login fails due to account lockout.
    
    This is a specialized login error indicating that the account
    has been locked, typically after multiple failed login attempts.
    
    Example:
        >>> raise AccountLockedError(
        ...     "Account locked after 5 failed attempts",
        ...     context={"username": "user***", "lockout_duration": "30 minutes"}
        ... )
    """
    pass


class PageLoadTimeoutError(AutomationFrameworkException):
    """Raised when a page fails to load within the timeout period.
    
    This exception indicates that a page navigation or load operation
    did not complete within the configured timeout.
    
    Common causes:
    - Slow network connection
    - Server performance issues
    - Large page size or resources
    - JavaScript errors preventing page load
    
    Example:
        >>> raise PageLoadTimeoutError(
        ...     "Dashboard page failed to load",
        ...     context={"url": "https://app.com/dashboard", "timeout": 30}
        ... )
    """
    pass


class ConfigurationError(AutomationFrameworkException):
    """Raised when configuration is invalid or missing.
    
    This exception indicates that required configuration parameters
    are missing, invalid, or inconsistent.
    
    Common causes:
    - Missing environment variables
    - Invalid configuration values
    - Unsupported browser or platform
    - Missing required files or resources
    
    Example:
        >>> raise ConfigurationError(
        ...     "BASE_URL not configured",
        ...     context={"env_var": "BASE_URL", "current_value": None}
        ... )
    """
    pass


class DataValidationError(AutomationFrameworkException):
    """Raised when test data validation fails.
    
    This exception indicates that test data is missing, malformed,
    or does not meet validation requirements.
    
    Common causes:
    - Missing required fields in test data
    - Invalid data format or type
    - Data constraint violations
    - Corrupted test data files
    
    Example:
        >>> raise DataValidationError(
        ...     "Invalid username format in test data",
        ...     context={"field": "username", "value": "123", "expected": "string"}
        ... )
    """
    pass


class ScreenshotError(AutomationFrameworkException):
    """Raised when screenshot capture fails.
    
    This exception indicates that a screenshot could not be captured,
    typically during failure handling or reporting.
    
    Common causes:
    - Insufficient disk space
    - Permission issues
    - Driver session closed
    - Invalid screenshot directory
    
    Example:
        >>> raise ScreenshotError(
        ...     "Failed to save screenshot",
        ...     context={"path": "/screenshots/test.png", "error": "Permission denied"}
        ... )
    """
    pass


class BrowserError(AutomationFrameworkException):
    """Raised when browser operation fails.
    
    This exception indicates that a browser-level operation failed,
    such as driver initialization, navigation, or window management.
    
    Common causes:
    - WebDriver not found or incompatible
    - Browser not installed
    - Browser crash or hang
    - Invalid browser options
    
    Example:
        >>> raise BrowserError(
        ...     "Failed to initialize Chrome driver",
        ...     context={"browser": "chrome", "version": "120.0"}
        ... )
    """
    pass


class TestDataNotFoundError(AutomationFrameworkException):
    """Raised when required test data file or resource is not found.
    
    This exception indicates that a test data file, fixture, or
    resource required for test execution could not be located.
    
    Common causes:
    - Missing test data file
    - Incorrect file path
    - File moved or deleted
    - Permission issues
    
    Example:
        >>> raise TestDataNotFoundError(
        ...     "Login test data file not found",
        ...     context={"file": "tests/data/login.csv", "cwd": "/app"}
        ... )
    """
    pass


class PerformanceThresholdExceededError(AutomationFrameworkException):
    """Raised when a performance threshold is exceeded.
    
    This exception indicates that an operation took longer than
    the configured performance threshold, violating NFRs.
    
    Example:
        >>> raise PerformanceThresholdExceededError(
        ...     "Login response time exceeded threshold",
        ...     context={"actual": 3.5, "threshold": 2.0, "unit": "seconds"}
        ... )
    """
    pass


def sanitize_error_message(message: str, sensitive_patterns: Optional[list] = None) -> str:
    """Sanitize error message by removing sensitive information.
    
    Args:
        message: Original error message
        sensitive_patterns: List of regex patterns to redact
    
    Returns:
        Sanitized error message with sensitive data redacted
    
    Example:
        >>> sanitize_error_message("Login failed for user@example.com with password abc123")
        'Login failed for user*** with password ***'
    """
    import re
    
    if sensitive_patterns is None:
        sensitive_patterns = [
            r'password[=:\s]+\S+',
            r'token[=:\s]+\S+',
            r'api[_-]?key[=:\s]+\S+',
            r'secret[=:\s]+\S+',
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        ]
    
    sanitized = message
    for pattern in sensitive_patterns:
        sanitized = re.sub(pattern, '***', sanitized, flags=re.IGNORECASE)
    
    return sanitized