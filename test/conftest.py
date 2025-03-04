import allure
import pytest
from selenium import webdriver


@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):
        browser = webdriver.Chrome()
        browser.implicitly_wait(4)
        browser.maximize_window()
        browser.get("https://www.chitai-gorod.ru")
        yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()
