"""
Config: Loads configuration from environment variables.
Supports baseUrl, browser, headless, timeouts, and other runtime settings.
"""

import os
import logging

class Config:
    """
    Configuration class for test execution settings.
    All settings can be overridden via environment variables.
    """
    
    # Application settings
    BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080")
    
    # Browser settings
    BROWSER = os.environ.get("BROWSER", "chrome").lower()
    HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"
    
    # Timeout settings (in seconds)
    TIMEOUT = int(os.environ.get("TIMEOUT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "30"))
    SCRIPT_TIMEOUT = int(os.environ.get("SCRIPT_TIMEOUT", "30"))
    
    # Window settings
    WINDOW_WIDTH = int(os.environ.get("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.environ.get("WINDOW_HEIGHT", "1080"))
    MAXIMIZE_WINDOW = os.environ.get("MAXIMIZE_WINDOW", "true").lower() == "true"
    
    # Screenshot settings
    SCREENSHOT_ON_FAILURE = os.environ.get("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOT_DIR = os.environ.get("SCREENSHOT_DIR", "screenshots")
    
    # Logging settings
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    LOG_DIR = os.environ.get("LOG_DIR", "logs")
    LOG_FILE = os.environ.get("LOG_FILE", "test_execution.log")
    
    # Test data settings
    TEST_DATA_DIR = os.environ.get("TEST_DATA_DIR", "tests/data")
    
    # Retry settings
    MAX_RETRY_ATTEMPTS = int(os.environ.get("MAX_RETRY_ATTEMPTS", "3"))
    RETRY_DELAY = int(os.environ.get("RETRY_DELAY", "1"))
    
    # Browser-specific options
    CHROME_OPTIONS = [
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-infobars",
        "--disable-notifications",
        "--disable-popup-blocking"
    ]
    
    FIREFOX_OPTIONS = [
        "--disable-gpu",
        "--no-sandbox"
    ]
    
    @classmethod
    def validate(cls):
        """
        Validate configuration settings.
        
        Raises:
            ValueError: If configuration is invalid
        """
        # Validate browser
        valid_browsers = ["chrome", "firefox"]
        if cls.BROWSER not in valid_browsers:
            raise ValueError(f"Invalid browser: {cls.BROWSER}. Must be one of {valid_browsers}")
        
        # Validate timeouts
        if cls.TIMEOUT <= 0:
            raise ValueError(f"Invalid timeout: {cls.TIMEOUT}. Must be positive")
        
        if cls.PAGE_LOAD_TIMEOUT <= 0:
            raise ValueError(f"Invalid page load timeout: {cls.PAGE_LOAD_TIMEOUT}. Must be positive")
        
        # Validate window dimensions
        if cls.WINDOW_WIDTH <= 0 or cls.WINDOW_HEIGHT <= 0:
            raise ValueError(f"Invalid window dimensions: {cls.WINDOW_WIDTH}x{cls.WINDOW_HEIGHT}")
        
        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if cls.LOG_LEVEL not in valid_log_levels:
            raise ValueError(f"Invalid log level: {cls.LOG_LEVEL}. Must be one of {valid_log_levels}")
        
        logging.info("Configuration validated successfully")
    
    @classmethod
    def print_config(cls):
        """
        Print current configuration (for debugging).
        Sensitive information is redacted.
        """
        config_info = f"""
        ========================================
        Test Configuration
        ========================================
        BASE_URL: {cls.BASE_URL}
        BROWSER: {cls.BROWSER}
        HEADLESS: {cls.HEADLESS}
        TIMEOUT: {cls.TIMEOUT}s
        PAGE_LOAD_TIMEOUT: {cls.PAGE_LOAD_TIMEOUT}s
        SCRIPT_TIMEOUT: {cls.SCRIPT_TIMEOUT}s
        WINDOW_SIZE: {cls.WINDOW_WIDTH}x{cls.WINDOW_HEIGHT}
        MAXIMIZE_WINDOW: {cls.MAXIMIZE_WINDOW}
        SCREENSHOT_ON_FAILURE: {cls.SCREENSHOT_ON_FAILURE}
        SCREENSHOT_DIR: {cls.SCREENSHOT_DIR}
        LOG_LEVEL: {cls.LOG_LEVEL}
        LOG_DIR: {cls.LOG_DIR}
        LOG_FILE: {cls.LOG_FILE}
        TEST_DATA_DIR: {cls.TEST_DATA_DIR}
        MAX_RETRY_ATTEMPTS: {cls.MAX_RETRY_ATTEMPTS}
        RETRY_DELAY: {cls.RETRY_DELAY}s
        ========================================
        """
        logging.info(config_info)
        print(config_info)

# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    logging.error(f"Configuration validation failed: {str(e)}")
    raise