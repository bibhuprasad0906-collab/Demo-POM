"""DriverFactory: Instantiates Selenium WebDriver.
Supports Chrome, Firefox, Edge with headless mode and custom options."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from src.utils.config import Config
import logging
import os


class DriverFactory:
    """Factory class for creating WebDriver instances."""

    @staticmethod
    def get_driver():
        """Returns a Selenium WebDriver instance based on configuration.
        
        Returns:
            WebDriver: Configured Selenium WebDriver instance
            
        Raises:
            ValueError: If browser type is not supported
        """
        logger = logging.getLogger("DriverFactory")
        browser = Config.BROWSER.lower()

        logger.info(f"Initializing {browser} driver (headless={Config.HEADLESS})")

        try:
            if browser == "chrome":
                driver = DriverFactory._get_chrome_driver()
            elif browser == "firefox":
                driver = DriverFactory._get_firefox_driver()
            elif browser == "edge":
                driver = DriverFactory._get_edge_driver()
            else:
                raise ValueError(f"Unsupported browser: {browser}. Supported: chrome, firefox, edge")

            # Set timeouts
            driver.implicitly_wait(Config.TIMEOUT)
            driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

            # Set window size
            driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

            logger.info(f"{browser.capitalize()} driver initialized successfully")
            return driver

        except Exception as e:
            logger.error(f"Failed to initialize {browser} driver: {str(e)}")
            raise

    @staticmethod
    def _get_chrome_driver():
        """Create and configure Chrome WebDriver.
        
        Returns:
            WebDriver: Chrome WebDriver instance
        """
        options = ChromeOptions()

        # Headless mode
        if Config.HEADLESS:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

        # Performance and stability options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")

        # Logging
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # User agent
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        # Create driver
        driver = webdriver.Chrome(options=options)
        return driver

    @staticmethod
    def _get_firefox_driver():
        """Create and configure Firefox WebDriver.
        
        Returns:
            WebDriver: Firefox WebDriver instance
        """
        options = FirefoxOptions()

        # Headless mode
        if Config.HEADLESS:
            options.add_argument("--headless")

        # Performance options
        options.add_argument("--disable-gpu")
        options.set_preference("browser.cache.disk.enable", False)
        options.set_preference("browser.cache.memory.enable", False)
        options.set_preference("browser.cache.offline.enable", False)
        options.set_preference("network.http.use-cache", False)

        # Create driver
        driver = webdriver.Firefox(options=options)
        return driver

    @staticmethod
    def _get_edge_driver():
        """Create and configure Edge WebDriver.
        
        Returns:
            WebDriver: Edge WebDriver instance
        """
        options = EdgeOptions()

        # Headless mode
        if Config.HEADLESS:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        # Performance options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")

        # Create driver
        driver = webdriver.Edge(options=options)
        return driver


def get_driver():
    """Convenience function to get WebDriver instance.
    
    Returns:
        WebDriver: Configured Selenium WebDriver instance
    """
    return DriverFactory.get_driver()