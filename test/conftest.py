import allure
import pytest
import json
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
    Фикстура для настройки браузера с добавлением и удалением куки.
    """
    browser_name = request.config.getoption("--browser")  # Получаем аргумент
    with allure.step(f"Открыть и настроить браузер: {browser_name}"):
        # Инициализация браузера
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

        # Удаление куки
        cookies_to_remove = [
            {"name": "_ym_uid", "domain": ".chitai-gorod.ru"},
            {"name": "_pk_id.1.f5fe", "domain": "www.chitai-gorod.ru"}
        ]
        for cookie in cookies_to_remove:
            try:
                driver.delete_cookie(cookie["name"])  # Удаляем куки по имени
                print(f"Кука '{cookie['name']}' удалена.")
            except Exception as e:
                print(f"Не удалось удалить куку '{cookie['name']}': {e}")

        # Добавление куки из файла
        try:
            with open("cookie.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                new_cookies = data.get("new_values", [])
                for cookie in new_cookies:
                    # Удаляем неподдерживаемые поля
                    cookie.pop("sameSite", None)
                    driver.add_cookie(cookie)
                print("Куки добавлены в браузер.")
        except FileNotFoundError:
            print("Файл merged_results.json не найден. Пропускаем загрузку.")
        except json.JSONDecodeError:
            print("Ошибка чтения JSON из файла merged_results.json.")

        # Обновление страницы для применения куки
        driver.refresh()
        yield driver

    with allure.step("Закрыть браузер"):
        driver.quit()
