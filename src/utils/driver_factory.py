"""
DriverFactory: Instantiates Selenium WebDriver for Chrome/Firefox.
Supports headless mode and implicit waits.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from src.utils.config import Config

def get_driver():
    """
    Returns a Selenium WebDriver instance based on config.
    """
    if Config.BROWSER == "chrome":
        options = ChromeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
    elif Config.BROWSER == "firefox":
        options = FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {Config.BROWSER}")
    driver.implicitly_wait(Config.TIMEOUT)
    return driver