"""WebDriver factory module for creating and managing Selenium WebDriver instances.

Provides centralized driver creation with support for multiple browsers,
headless mode, and custom options. Implements robust error handling and
logging for driver lifecycle management.

Supported Browsers:
    - Chrome (default)
    - Firefox

Features:
    - Automatic driver management (no manual driver downloads)
    - Headless mode support
    - Custom window size configuration
    - Implicit wait configuration
    - Page load timeout configuration
    - Comprehensive logging
"""

import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import WebDriverException
from src.utils.config import Config
from src.utils.exceptions import BrowserError, ConfigurationError


class DriverFactory:
    """Factory class for creating WebDriver instances.
    
    This class provides static methods for creating and configuring
    WebDriver instances based on the application configuration.
    
    Example:
        >>> driver = DriverFactory.get_driver()
        >>> driver.get("https://example.com")
        >>> driver.quit()
    """
    
    @staticmethod
    def _get_chrome_options() -> ChromeOptions:
        """Configure Chrome options based on Config settings.
        
        Returns:
            ChromeOptions: Configured Chrome options
        """
        options = ChromeOptions()
        
        # Headless mode
        if Config.HEADLESS:
            options.add_argument("--headless=new")
            logging.info("Chrome headless mode enabled")
        
        # Window size
        width, height = Config.WINDOW_SIZE.split(",")
        options.add_argument(f"--window-size={width},{height}")
        
        # Performance and stability options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        
        # Security and privacy
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Logging
        options.add_argument("--log-level=3")  # Suppress verbose logging
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        logging.debug(f"Chrome options configured: {options.arguments}")
        return options
    
    @staticmethod
    def _get_firefox_options() -> FirefoxOptions:
        """Configure Firefox options based on Config settings.
        
        Returns:
            FirefoxOptions: Configured Firefox options
        """
        options = FirefoxOptions()
        
        # Headless mode
        if Config.HEADLESS:
            options.add_argument("--headless")
            logging.info("Firefox headless mode enabled")
        
        # Window size
        width, height = Config.WINDOW_SIZE.split(",")
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")
        
        # Performance and stability options
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        
        # Security and privacy
        options.set_preference("browser.privatebrowsing.autostart", True)
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        
        # Logging
        options.set_preference("devtools.console.stdout.content", False)
        
        logging.debug(f"Firefox options configured: {options.arguments}")
        return options
    
    @staticmethod
    def _create_chrome_driver() -> webdriver.Chrome:
        """Create and configure Chrome WebDriver instance.
        
        Returns:
            webdriver.Chrome: Configured Chrome driver
        
        Raises:
            BrowserError: If Chrome driver creation fails
        """
        try:
            options = DriverFactory._get_chrome_options()
            driver = webdriver.Chrome(options=options)
            logging.info("Chrome WebDriver created successfully")
            return driver
        except WebDriverException as e:
            error_msg = f"Failed to create Chrome driver: {str(e)}"
            logging.error(error_msg)
            raise BrowserError(
                error_msg,
                context={"browser": "chrome", "error": str(e)}
            )
        except Exception as e:
            error_msg = f"Unexpected error creating Chrome driver: {str(e)}"
            logging.error(error_msg)
            raise BrowserError(
                error_msg,
                context={"browser": "chrome", "error": str(e)}
            )
    
    @staticmethod
    def _create_firefox_driver() -> webdriver.Firefox:
        """Create and configure Firefox WebDriver instance.
        
        Returns:
            webdriver.Firefox: Configured Firefox driver
        
        Raises:
            BrowserError: If Firefox driver creation fails
        """
        try:
            options = DriverFactory._get_firefox_options()
            driver = webdriver.Firefox(options=options)
            logging.info("Firefox WebDriver created successfully")
            return driver
        except WebDriverException as e:
            error_msg = f"Failed to create Firefox driver: {str(e)}"
            logging.error(error_msg)
            raise BrowserError(
                error_msg,
                context={"browser": "firefox", "error": str(e)}
            )
        except Exception as e:
            error_msg = f"Unexpected error creating Firefox driver: {str(e)}"
            logging.error(error_msg)
            raise BrowserError(
                error_msg,
                context={"browser": "firefox", "error": str(e)}
            )
    
    @staticmethod
    def get_driver(browser: Optional[str] = None) -> webdriver.Remote:
        """Create and configure WebDriver instance based on configuration.
        
        Args:
            browser: Browser name (chrome/firefox). If None, uses Config.BROWSER
        
        Returns:
            webdriver.Remote: Configured WebDriver instance
        
        Raises:
            ConfigurationError: If browser is not supported
            BrowserError: If driver creation fails
        
        Example:
            >>> driver = DriverFactory.get_driver()
            >>> driver.get("https://example.com")
            >>> driver.quit()
        """
        browser_name = (browser or Config.BROWSER).lower()
        
        logging.info(f"Creating WebDriver for browser: {browser_name}")
        
        # Create driver based on browser
        if browser_name == "chrome":
            driver = DriverFactory._create_chrome_driver()
        elif browser_name == "firefox":
            driver = DriverFactory._create_firefox_driver()
        else:
            error_msg = f"Unsupported browser: {browser_name}. Supported browsers: chrome, firefox"
            logging.error(error_msg)
            raise ConfigurationError(
                error_msg,
                context={"browser": browser_name, "supported": ["chrome", "firefox"]}
            )
        
        # Configure timeouts
        try:
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            logging.info(f"Timeouts configured - Implicit: {Config.IMPLICIT_WAIT}s, Page Load: {Config.PAGE_LOAD_TIMEOUT}s")
        except Exception as e:
            logging.warning(f"Failed to configure timeouts: {str(e)}")
        
        # Maximize window if not headless
        if not Config.HEADLESS:
            try:
                driver.maximize_window()
                logging.info("Browser window maximized")
            except Exception as e:
                logging.warning(f"Failed to maximize window: {str(e)}")
        
        logging.info(f"WebDriver ready - Browser: {browser_name}, Headless: {Config.HEADLESS}")
        return driver
    
    @staticmethod
    def quit_driver(driver: webdriver.Remote) -> None:
        """Safely quit WebDriver instance.
        
        Args:
            driver: WebDriver instance to quit
        
        Example:
            >>> driver = DriverFactory.get_driver()
            >>> # ... use driver ...
            >>> DriverFactory.quit_driver(driver)
        """
        if driver:
            try:
                driver.quit()
                logging.info("WebDriver quit successfully")
            except Exception as e:
                logging.warning(f"Error quitting driver: {str(e)}")


def get_driver(browser: Optional[str] = None) -> webdriver.Remote:
    """Convenience function to create WebDriver instance.
    
    This is a wrapper around DriverFactory.get_driver() for backward compatibility
    and simplified imports.
    
    Args:
        browser: Browser name (chrome/firefox). If None, uses Config.BROWSER
    
    Returns:
        webdriver.Remote: Configured WebDriver instance
    
    Example:
        >>> from src.utils.driver_factory import get_driver
        >>> driver = get_driver()
        >>> driver.get("https://example.com")
        >>> driver.quit()
    """
    return DriverFactory.get_driver(browser)