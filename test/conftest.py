import allure
import pytest
from selenium import webdriver
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
    with allure.step(f"Открыть и настроить браузер: {browser_name}"):
        if browser_name == "chrome":
            driver = webdriver.Chrome()
        elif browser_name == "firefox":
            driver = webdriver.Firefox()
        else:
            raise ValueError(f"Браузер {browser_name} не поддерживается.")

        # Настройки браузера
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.maximize_window()
        driver.get(BASE_URL)
        yield driver

    with allure.step("Закрыть браузер"):
        driver.quit()
