"""Page objects package for test automation framework.

Contains all page object classes implementing the Page Object Model (POM)
pattern for clean separation of test logic and UI interactions.
"""

from src.pages.base_page import BasePage
from src.pages.login_page import LoginPage

__all__ = ["BasePage", "LoginPage"]