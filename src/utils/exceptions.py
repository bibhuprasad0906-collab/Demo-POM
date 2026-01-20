"""
Custom exceptions for UI operations.
"""

class ElementNotFoundError(Exception):
    """Raised when a UI element is not found."""
    pass

class LoginFailedError(Exception):
    """Raised when login fails."""
    pass
