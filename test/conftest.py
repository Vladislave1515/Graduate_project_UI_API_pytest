import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config import BASE_URL, IMPLICIT_WAIT
from pages.Cart_Page_API import CartPageAPI
from pages.Search_Page_API import SearchPageAPI
from config import BASE_URLS, HEADERS


def pytest_addoption(parser):
    """
    Добавление пользовательского аргумента для выбора браузера.
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
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


@pytest.fixture(scope="function")
def cart_api():
    """
    Фикстура для API клиента корзины.
    Возвращает объект CartPageAPI.
    """
    return CartPageAPI(BASE_URLS["cart"], HEADERS)


@pytest.fixture(scope="function")
def search_api():
    """
    Фикстура для API клиента поиска.
    Возвращает объект SearchPageAPI.
    """
    return SearchPageAPI(BASE_URLS["search"], HEADERS)


@pytest.fixture(scope="function")
def search_api_no_auth():
    """
    Фикстура для API клиента корзины без авторизации.
    """
    headers_without_auth = {}  # Пустые заголовки
    return SearchPageAPI(BASE_URLS["search"], headers_without_auth)
