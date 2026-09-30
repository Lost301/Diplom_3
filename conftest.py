"""Фикстуры: параметризованный драйвер (Chrome/Firefox) и тестовый пользователь."""
import glob
import os

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from data import Urls
from helpers import generate_user

DEFAULT_BROWSER = "chrome"
# Путь к бинарю Firefox можно переопределить переменной окружения FIREFOX_BINARY
FIREFOX_STORE_ALIAS = r"C:\Users\dkpol\AppData\Local\Microsoft\WindowsApps\firefox.exe"


def _firefox_binary():
    """Бинарь Firefox: свежий из кэша Selenium Manager, иначе алиас Microsoft Store."""
    cache_dir = os.path.expanduser(r"~\.cache\selenium\firefox\win64")
    candidates = sorted(glob.glob(os.path.join(cache_dir, "*", "firefox.exe")))
    if candidates:
        return candidates[-1]
    return FIREFOX_STORE_ALIAS


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=DEFAULT_BROWSER,
        choices=["chrome", "firefox"],
        help="Браузер для прогона тестов: chrome или firefox",
    )


def _build_driver(browser):
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1600,900")
        return webdriver.Chrome(options=options)
    options = FirefoxOptions()
    options.add_argument("-headless")
    options.add_argument("--width=1600")
    options.add_argument("--height=900")
    # Store-версия Firefox: бинарь не находится автоматически, задаём явно
    # (кэш Selenium Manager стабильнее алиаса WindowsApps)
    options.binary_location = os.environ.get("FIREFOX_BINARY", _firefox_binary())
    return webdriver.Firefox(options=options)


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    browser_driver = _build_driver(browser)
    browser_driver.implicitly_wait(5)
    yield browser_driver
    browser_driver.quit()


@pytest.fixture
def user(driver):
    """Создаёт пользователя через API, инъектирует токены в localStorage, удаляет после теста."""
    payload = generate_user()
    response = requests.post(Urls.REGISTER_USER, json=payload, timeout=15)
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"
    tokens = response.json()
    user_data = {
        "email": payload["email"],
        "password": payload["password"],
        "name": payload["name"],
        "accessToken": tokens["accessToken"],
        "refreshToken": tokens["refreshToken"],
    }

    driver.get(Urls.MAIN_PAGE)
    driver.execute_script(
        "window.localStorage.setItem('accessToken', arguments[0]);"
        "window.localStorage.setItem('refreshToken', arguments[1]);",
        user_data["accessToken"],
        user_data["refreshToken"],
    )
    driver.refresh()

    yield user_data

    requests.delete(
        Urls.DELETE_USER,
        headers={"Authorization": user_data["accessToken"]},
        timeout=15,
    )
