"""Custom exceptions for UI test automation.
Provides specific exception types for better error handling and reporting."""


class ElementNotFoundError(Exception):
    """Raised when a UI element is not found within the specified timeout.
    
    This exception indicates that the element locator is either incorrect,
    the element is not present on the page, or the page has not loaded properly.
    """
    pass


class LoginFailedError(Exception):
    """Raised when login fails due to invalid credentials or account lockout.
    
    This exception is used to distinguish login failures from other types of errors,
    allowing for specific handling of authentication issues.
    """
    pass


class PageLoadError(Exception):
    """Raised when a page fails to load within the expected timeout.
    
    This exception indicates network issues, server errors, or incorrect URLs.
    """
    pass


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing required parameters.
    
    This exception is used during initialization to catch configuration issues early.
    """
    pass


class TestDataError(Exception):
    """Raised when test data is invalid, missing, or cannot be loaded.
    
    This exception indicates issues with CSV files, JSON data, or other test data sources.
    """
    pass