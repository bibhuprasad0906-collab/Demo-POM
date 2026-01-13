"""
Config: Loads configuration from environment variables.
Supports baseUrl, browser, headless, timeouts.
"""

import os

class Config:
    BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080/login")
    BROWSER = os.environ.get("BROWSER", "chrome")
    HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.environ.get("TIMEOUT", "10"))