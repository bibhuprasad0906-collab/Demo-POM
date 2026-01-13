"""
DriverFactory: Instantiates Selenium WebDriver for Chrome/Firefox.
Supports headless mode, custom options, and implicit waits.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from src.utils.config import Config
import logging
import os

def get_driver():
    """
    Create and configure a Selenium WebDriver instance.
    
    Returns:
        Configured WebDriver instance (Chrome or Firefox)
        
    Raises:
        ValueError: If browser type is not supported
        Exception: If driver initialization fails
    """
    try:
        if Config.BROWSER == "chrome":
            driver = _get_chrome_driver()
        elif Config.BROWSER == "firefox":
            driver = _get_firefox_driver()
        else:
            raise ValueError(f"Unsupported browser: {Config.BROWSER}")
        
        # Configure timeouts
        driver.implicitly_wait(Config.TIMEOUT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        driver.set_script_timeout(Config.SCRIPT_TIMEOUT)
        
        # Configure window size
        if Config.MAXIMIZE_WINDOW:
            driver.maximize_window()
        else:
            driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        
        logging.info(f"WebDriver initialized successfully: {Config.BROWSER}")
        return driver
        
    except Exception as e:
        logging.error(f"Failed to initialize WebDriver: {str(e)}")
        raise

def _get_chrome_driver():
    """
    Create and configure Chrome WebDriver.
    
    Returns:
        Configured Chrome WebDriver instance
    """
    options = ChromeOptions()
    
    # Add headless mode if configured
    if Config.HEADLESS:
        options.add_argument("--headless=new")
        logging.info("Chrome running in headless mode")
    
    # Add standard Chrome options
    for option in Config.CHROME_OPTIONS:
        options.add_argument(option)
    
    # Additional Chrome preferences
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Disable W3C mode for better compatibility (if needed)
    # options.add_experimental_option("w3c", False)
    
    try:
        # Try to use ChromeService if chromedriver path is specified
        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
        if chromedriver_path:
            service = ChromeService(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
        else:
            driver = webdriver.Chrome(options=options)
        
        logging.info("Chrome WebDriver created successfully")
        return driver
        
    except Exception as e:
        logging.error(f"Failed to create Chrome WebDriver: {str(e)}")
        raise

def _get_firefox_driver():
    """
    Create and configure Firefox WebDriver.
    
    Returns:
        Configured Firefox WebDriver instance
    """
    options = FirefoxOptions()
    
    # Add headless mode if configured
    if Config.HEADLESS:
        options.add_argument("--headless")
        logging.info("Firefox running in headless mode")
    
    # Add standard Firefox options
    for option in Config.FIREFOX_OPTIONS:
        options.add_argument(option)
    
    # Additional Firefox preferences
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("geo.enabled", False)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    
    try:
        # Try to use FirefoxService if geckodriver path is specified
        geckodriver_path = os.environ.get("GECKODRIVER_PATH")
        if geckodriver_path:
            service = FirefoxService(executable_path=geckodriver_path)
            driver = webdriver.Firefox(service=service, options=options)
        else:
            driver = webdriver.Firefox(options=options)
        
        logging.info("Firefox WebDriver created successfully")
        return driver
        
    except Exception as e:
        logging.error(f"Failed to create Firefox WebDriver: {str(e)}")
        raise

def quit_driver(driver):
    """
    Safely quit the WebDriver.
    
    Args:
        driver: WebDriver instance to quit
    """
    try:
        if driver:
            driver.quit()
            logging.info("WebDriver quit successfully")
    except Exception as e:
        logging.error(f"Error quitting WebDriver: {str(e)}")