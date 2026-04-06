"""Behave environment hooks for Selenium UI tests."""

from os import getenv
from shutil import which

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


WAIT_SECONDS = int(getenv("WAIT_SECONDS", "30"))
BASE_URL = getenv("BASE_URL", "http://localhost:8080")
DRIVER = getenv("DRIVER", "chrome").lower()


def before_all(context):
    """Executed once before all tests."""
    context.base_url = BASE_URL
    context.wait_seconds = WAIT_SECONDS

    if "firefox" in DRIVER:
        context.driver = get_firefox()
    else:
        context.driver = get_chrome()

    context.driver.implicitly_wait(context.wait_seconds)
    context.driver.set_window_size(1280, 1300)
    context.config.setup_logging()


def after_all(context):
    """Executed once after all tests."""
    if hasattr(context, "driver"):
        context.driver.quit()


def get_chrome():
    """Create a headless Chrome web driver."""
    print("Running Behave using the Chrome driver...\n")

    chrome_bin = which("chromium") or which("google-chrome")
    chromedriver_bin = which("chromedriver")

    if not chrome_bin:
        raise RuntimeError("Chrome/Chromium binary not found on PATH")
    if not chromedriver_bin:
        raise RuntimeError("chromedriver not found on PATH")

    options = webdriver.ChromeOptions()
    options.binary_location = chrome_bin
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    return webdriver.Chrome(service=ChromeService(chromedriver_bin), options=options)


def get_firefox():
    """Create a headless Firefox web driver."""
    print("Running Behave using the Firefox driver...\n")
    options = webdriver.FirefoxOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)
