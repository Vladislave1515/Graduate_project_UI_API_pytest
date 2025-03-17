import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config import BASE_URL, IMPLICIT_WAIT


def pytest_addoption(parser):
    """
    Добавление пользовательского аргумента для выбора браузера.
    """
    parser.addoption(
        "--browser",
        action="store",
        default="firefox",
        help="Выбор браузера: chrome или firefox"
    )


@pytest.fixture
def browser(request):
    """
    Фикстура для настройки браузера.
    """
    browser_name = request.config.getoption("--browser")  # Получаем аргумент
    if browser_name == "chrome":
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
    elif browser_name == "firefox":
        firefox_options = FirefoxOptions()
        driver = webdriver.Firefox(options=firefox_options)
    else:
        raise ValueError(f"Браузер {browser_name} не поддерживается.")

    # Настройки браузера
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.maximize_window()
    driver.get(BASE_URL)

    yield driver

    driver.quit()
