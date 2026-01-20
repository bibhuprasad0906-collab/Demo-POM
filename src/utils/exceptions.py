"""
Custom exceptions for UI operations.
Provides specific exception types for better error handling and debugging.
"""

class ElementNotFoundError(Exception):
    """Raised when a UI element is not found within the specified timeout."""
    pass

class LoginFailedError(Exception):
    """Raised when login operation fails."""
    pass

class PageLoadError(Exception):
    """Raised when a page fails to load properly."""
    pass

class ConfigurationError(Exception):
    """Raised when there is a configuration issue."""
    pass

class DataValidationError(Exception):
    """Raised when test data validation fails."""
    pass