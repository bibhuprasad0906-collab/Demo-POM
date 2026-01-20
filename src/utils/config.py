"""Configuration module for test automation framework.

Loads configuration from environment variables with secure defaults.
Provides centralized access to all runtime configuration parameters.

Security Note:
    - Never hardcode credentials in this file
    - Use environment variables or secure vaults for sensitive data
    - All credential access should be in-memory only
"""

import os
import logging
from typing import Optional


class Config:
    """Central configuration class for test automation framework.
    
    All configuration parameters are loaded from environment variables
    with sensible defaults for local development.
    
    Attributes:
        BASE_URL: Application base URL for testing
        BROWSER: Browser to use (chrome/firefox)
        HEADLESS: Run browser in headless mode
        TIMEOUT: Default timeout for element waits (seconds)
        IMPLICIT_WAIT: Implicit wait timeout (seconds)
        PAGE_LOAD_TIMEOUT: Page load timeout (seconds)
        SCREENSHOT_ON_FAILURE: Capture screenshot on test failure
        LOG_LEVEL: Logging level (DEBUG/INFO/WARNING/ERROR)
        MAX_LOGIN_ATTEMPTS: Maximum failed login attempts before lockout
        LOGIN_RESPONSE_TIME_THRESHOLD: Maximum acceptable login response time (seconds)
    """
    
    # Application Configuration
    BASE_URL: str = os.environ.get("BASE_URL", "http://localhost:8080")
    
    # Browser Configuration
    BROWSER: str = os.environ.get("BROWSER", "chrome").lower()
    HEADLESS: bool = os.environ.get("HEADLESS", "true").lower() == "true"
    WINDOW_SIZE: str = os.environ.get("WINDOW_SIZE", "1920,1080")
    
    # Timeout Configuration
    TIMEOUT: int = int(os.environ.get("TIMEOUT", "10"))
    IMPLICIT_WAIT: int = int(os.environ.get("IMPLICIT_WAIT", "5"))
    PAGE_LOAD_TIMEOUT: int = int(os.environ.get("PAGE_LOAD_TIMEOUT", "30"))
    
    # Test Execution Configuration
    SCREENSHOT_ON_FAILURE: bool = os.environ.get("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO").upper()
    
    # Application-Specific Configuration
    MAX_LOGIN_ATTEMPTS: int = int(os.environ.get("MAX_LOGIN_ATTEMPTS", "5"))
    LOGIN_RESPONSE_TIME_THRESHOLD: float = float(os.environ.get("LOGIN_RESPONSE_TIME_THRESHOLD", "2.0"))
    
    # Directory Configuration
    SCREENSHOTS_DIR: str = os.environ.get("SCREENSHOTS_DIR", "screenshots")
    LOGS_DIR: str = os.environ.get("LOGS_DIR", "logs")
    REPORTS_DIR: str = os.environ.get("REPORTS_DIR", "reports")
    TEST_DATA_DIR: str = os.environ.get("TEST_DATA_DIR", "tests/data")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration parameters.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        errors = []
        
        # Validate BASE_URL
        if not cls.BASE_URL:
            errors.append("BASE_URL is not set")
        
        # Validate BROWSER
        if cls.BROWSER not in ["chrome", "firefox"]:
            errors.append(f"Unsupported browser: {cls.BROWSER}. Use 'chrome' or 'firefox'")
        
        # Validate timeouts
        if cls.TIMEOUT <= 0:
            errors.append(f"TIMEOUT must be positive, got: {cls.TIMEOUT}")
        
        if cls.IMPLICIT_WAIT < 0:
            errors.append(f"IMPLICIT_WAIT must be non-negative, got: {cls.IMPLICIT_WAIT}")
        
        if cls.PAGE_LOAD_TIMEOUT <= 0:
            errors.append(f"PAGE_LOAD_TIMEOUT must be positive, got: {cls.PAGE_LOAD_TIMEOUT}")
        
        # Validate MAX_LOGIN_ATTEMPTS
        if cls.MAX_LOGIN_ATTEMPTS <= 0:
            errors.append(f"MAX_LOGIN_ATTEMPTS must be positive, got: {cls.MAX_LOGIN_ATTEMPTS}")
        
        # Validate LOGIN_RESPONSE_TIME_THRESHOLD
        if cls.LOGIN_RESPONSE_TIME_THRESHOLD <= 0:
            errors.append(f"LOGIN_RESPONSE_TIME_THRESHOLD must be positive, got: {cls.LOGIN_RESPONSE_TIME_THRESHOLD}")
        
        if errors:
            for error in errors:
                logging.error(f"Configuration validation error: {error}")
            return False
        
        logging.info("Configuration validation successful")
        return True
    
    @classmethod
    def get_config_summary(cls) -> dict:
        """Get a summary of current configuration (sanitized).
        
        Returns:
            dict: Configuration summary without sensitive data
        """
        return {
            "base_url": cls.BASE_URL,
            "browser": cls.BROWSER,
            "headless": cls.HEADLESS,
            "timeout": cls.TIMEOUT,
            "implicit_wait": cls.IMPLICIT_WAIT,
            "page_load_timeout": cls.PAGE_LOAD_TIMEOUT,
            "screenshot_on_failure": cls.SCREENSHOT_ON_FAILURE,
            "log_level": cls.LOG_LEVEL,
            "max_login_attempts": cls.MAX_LOGIN_ATTEMPTS,
            "login_response_time_threshold": cls.LOGIN_RESPONSE_TIME_THRESHOLD
        }
    
    @classmethod
    def log_config(cls) -> None:
        """Log current configuration (sanitized)."""
        config_summary = cls.get_config_summary()
        logging.info("=" * 50)
        logging.info("Test Configuration:")
        for key, value in config_summary.items():
            logging.info(f"  {key}: {value}")
        logging.info("=" * 50)


# Validate configuration on module import
if not Config.validate():
    logging.warning("Configuration validation failed. Please check environment variables.")