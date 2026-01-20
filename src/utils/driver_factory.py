"""
DriverFactory: Instantiates Selenium WebDriver for Chrome/Firefox.
Supports headless mode and implicit waits.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from src.utils.config import Config
import logging

logger = logging.getLogger(__name__)

def get_driver():
    """
    Factory method to create and configure WebDriver instance.
    Returns configured WebDriver based on Config settings.
    """
    browser = Config.BROWSER
    logger.info(f"Initializing {browser} driver (headless={Config.HEADLESS})")
    
    try:
        if browser == "chrome":
            options = ChromeOptions()
            
            if Config.HEADLESS:
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
            
            # Additional Chrome options for stability
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--window-size=1920,1080")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # Use webdriver-manager for automatic driver management
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
        elif browser == "firefox":
            options = FirefoxOptions()
            
            if Config.HEADLESS:
                options.add_argument("--headless")
            
            # Additional Firefox options
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            
            # Use webdriver-manager for automatic driver management
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
        else:
            raise ValueError(f"Unsupported browser: {browser}. Supported browsers: chrome, firefox")
        
        # Set timeouts
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
        # Maximize window if not headless
        if not Config.HEADLESS:
            driver.maximize_window()
        
        logger.info(f"{browser.capitalize()} driver initialized successfully")
        return driver
        
    except Exception as e:
        logger.error(f"Failed to initialize {browser} driver: {str(e)}")
        raise

def quit_driver(driver):
    """
    Safely quit the WebDriver instance.
    """
    try:
        if driver:
            driver.quit()
            logger.info("Driver quit successfully")
    except Exception as e:
        logger.error(f"Error quitting driver: {str(e)}")