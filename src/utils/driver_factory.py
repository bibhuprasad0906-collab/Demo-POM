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

def get_driver():
    """
    Returns a configured WebDriver instance.
    """
    if Config.BROWSER == "chrome":
        options = ChromeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif Config.BROWSER == "firefox":
        options = FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {Config.BROWSER}")
    driver.implicitly_wait(Config.TIMEOUT)
    return driver