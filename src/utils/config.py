"""Config: Loads configuration from environment variables.
Provides centralized configuration management for test execution."""

import os
import logging


class Config:
    """Configuration class for test execution parameters."""

    # Application URL
    BASE_URL = os.environ.get("BASE_URL", "https://example.com/login")

    # Browser configuration
    BROWSER = os.environ.get("BROWSER", "chrome").lower()

    # Headless mode
    HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"

    # Timeouts
    TIMEOUT = int(os.environ.get("TIMEOUT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "30"))

    # Window size
    WINDOW_WIDTH = int(os.environ.get("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.environ.get("WINDOW_HEIGHT", "1080"))

    # Screenshot configuration
    SCREENSHOT_ON_FAILURE = os.environ.get("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOT_DIR = os.environ.get("SCREENSHOT_DIR", "screenshots")

    # Logging configuration
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    LOG_DIR = os.environ.get("LOG_DIR", "logs")

    # Test data
    TEST_DATA_DIR = os.environ.get("TEST_DATA_DIR", "tests/data")

    # Account lockout configuration
    LOCKOUT_THRESHOLD = int(os.environ.get("LOCKOUT_THRESHOLD", "3"))

    @classmethod
    def validate(cls):
        """Validate configuration parameters.
        
        Raises:
            ValueError: If configuration is invalid
        """
        logger = logging.getLogger(cls.__name__)

        # Validate browser
        valid_browsers = ["chrome", "firefox", "edge", "safari"]
        if cls.BROWSER not in valid_browsers:
            raise ValueError(f"Invalid browser: {cls.BROWSER}. Must be one of {valid_browsers}")

        # Validate timeouts
        if cls.TIMEOUT <= 0:
            raise ValueError(f"Invalid timeout: {cls.TIMEOUT}. Must be positive integer")

        if cls.PAGE_LOAD_TIMEOUT <= 0:
            raise ValueError(f"Invalid page load timeout: {cls.PAGE_LOAD_TIMEOUT}. Must be positive integer")

        # Validate window size
        if cls.WINDOW_WIDTH <= 0 or cls.WINDOW_HEIGHT <= 0:
            raise ValueError(f"Invalid window size: {cls.WINDOW_WIDTH}x{cls.WINDOW_HEIGHT}")

        # Validate lockout threshold
        if cls.LOCKOUT_THRESHOLD <= 0:
            raise ValueError(f"Invalid lockout threshold: {cls.LOCKOUT_THRESHOLD}. Must be positive integer")

        logger.info("Configuration validated successfully")

    @classmethod
    def log_config(cls):
        """Log current configuration (sanitized)."""
        logger = logging.getLogger(cls.__name__)
        logger.info("=" * 50)
        logger.info("Test Configuration:")
        logger.info(f"  BASE_URL: {cls.BASE_URL}")
        logger.info(f"  BROWSER: {cls.BROWSER}")
        logger.info(f"  HEADLESS: {cls.HEADLESS}")
        logger.info(f"  TIMEOUT: {cls.TIMEOUT}s")
        logger.info(f"  PAGE_LOAD_TIMEOUT: {cls.PAGE_LOAD_TIMEOUT}s")
        logger.info(f"  WINDOW_SIZE: {cls.WINDOW_WIDTH}x{cls.WINDOW_HEIGHT}")
        logger.info(f"  SCREENSHOT_ON_FAILURE: {cls.SCREENSHOT_ON_FAILURE}")
        logger.info(f"  LOG_LEVEL: {cls.LOG_LEVEL}")
        logger.info(f"  LOCKOUT_THRESHOLD: {cls.LOCKOUT_THRESHOLD}")
        logger.info("=" * 50)