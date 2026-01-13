"""
Custom exceptions for UI test automation.
Provides specific exception types for better error handling and debugging.
"""

class ElementNotFoundError(Exception):
    """
    Raised when a UI element is not found within the specified timeout.
    
    This exception indicates that the element locator may be incorrect,
    the page may not have loaded properly, or the element may not exist.
    """
    pass

class LoginFailedError(Exception):
    """
    Raised when a login operation fails unexpectedly.
    
    This exception indicates that the login process did not complete
    as expected, either due to incorrect credentials, system errors,
    or unexpected UI behavior.
    """
    pass

class PageLoadError(Exception):
    """
    Raised when a page fails to load within the expected timeout.
    
    This exception indicates network issues, server errors, or
    incorrect URL configuration.
    """
    pass

class ConfigurationError(Exception):
    """
    Raised when there is an error in test configuration.
    
    This exception indicates missing or invalid configuration values,
    such as environment variables or test data.
    """
    pass

class TestDataError(Exception):
    """
    Raised when there is an error loading or parsing test data.
    
    This exception indicates issues with test data files, such as
    missing CSV files, invalid JSON, or incorrect data format.
    """
    pass

class DriverInitializationError(Exception):
    """
    Raised when WebDriver fails to initialize.
    
    This exception indicates issues with browser driver setup,
    such as missing driver executable or incompatible versions.
    """
    pass

class NavigationError(Exception):
    """
    Raised when navigation to a page fails.
    
    This exception indicates issues with page navigation,
    such as invalid URLs or network connectivity problems.
    """
    pass

class AssertionError(Exception):
    """
    Raised when a test assertion fails.
    
    This exception indicates that the actual result does not match
    the expected result in a test case.
    """
    pass