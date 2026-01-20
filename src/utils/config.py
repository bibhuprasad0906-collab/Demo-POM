"""
Config: Loads configuration from environment variables.
Supports baseUrl, browser, headless, and timeouts.
"""

import os

class Config:
    """Configuration class for test execution parameters."""
    
    BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
    BROWSER = os.environ.get("BROWSER", "chrome").lower()
    HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.environ.get("TIMEOUT", "10"))
    IMPLICIT_WAIT = int(os.environ.get("IMPLICIT_WAIT", "5"))
    PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "30"))
    
    # Screenshot settings
    SCREENSHOT_ON_FAILURE = os.environ.get("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOT_DIR = os.environ.get("SCREENSHOT_DIR", "screenshots")
    
    # Logging settings
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    LOG_DIR = os.environ.get("LOG_DIR", "logs")
    
    @classmethod
    def get_config_summary(cls):
        """Return a summary of current configuration (sanitized)."""
        return {
            "BASE_URL": cls.BASE_URL,
            "BROWSER": cls.BROWSER,
            "HEADLESS": cls.HEADLESS,
            "TIMEOUT": cls.TIMEOUT,
            "IMPLICIT_WAIT": cls.IMPLICIT_WAIT,
            "PAGE_LOAD_TIMEOUT": cls.PAGE_LOAD_TIMEOUT,
            "SCREENSHOT_ON_FAILURE": cls.SCREENSHOT_ON_FAILURE,
            "LOG_LEVEL": cls.LOG_LEVEL
        }