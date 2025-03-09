from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def wait_for_element(driver, locator, condition, timeout=3):
    """
    Универсальный метод ожидания элемента.

    :param driver: WebDriver - экземпляр драйвера.
    :param locator: tuple - локатор элемента.
    :param condition: Callable - условие ожидания.
    :param timeout: int - время ожидания в секундах (по умолчанию 3 секунды).
    :return: WebElement - найденный элемент.
    """
    return WebDriverWait(driver, timeout).until(condition(locator))


class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_box = (By.CSS_SELECTOR, 'input.header-search__input')
        self.search_button = (By.CSS_SELECTOR, 'button.header-search__button')
        self.category_books = (
            By.XPATH,
            '//span[contains(@class, "search-categories-tree-item__text") '
            'and contains(text(), "Книги")]'
        )
        self.books_count = (
            By.XPATH,
            '//span[contains(@class, "search-categories-tree-item__text") '
            'and contains(text(), "Книги")]/span[@class="'
            'search-categories-tree-item__count"]'
        )
        self.delete_query_cross = (
            By.XPATH, '//button[contains(@class, "result-item__button")]'
        )
        self.clear_icon = (By.CLASS_NAME, 'header-search__clear-icon')
        self.suggestions_title = (
            By.CLASS_NAME, 'search-suggestion-wrapper__title'
        )
        self.book_author = (
            By.CSS_SELECTOR, 'article:nth-child(1) .product-title__author'
        )
        self.empty_result_message = (
            By.CSS_SELECTOR, 'div.catalog-empty-result__container > div > h4'
        )
        self.search_history_item = (
            By.CSS_SELECTOR,
            "div.header-search-results ul li div div span"
        )  # Локатор для текста из истории поиска

    def enter_search_query_with_keys(self, query):
        """
        Вводит запрос в строку поиска вручную с помощью send_keys.
        """
        search_input = wait_for_element(
            self.driver, self.search_box, EC.element_to_be_clickable
        )
        search_input.click()
        search_input.clear()
        search_input.send_keys(query)

    def enter_search_query_with_js(self, query):
        """
        Вводит запрос в строку поиска с помощью JavaScript.
        """
        search_input = wait_for_element(
            self.driver, self.search_box, EC.element_to_be_clickable
        )
        search_input.click()
        search_input.clear()

        js_set_value = """
        var elm = arguments[0], txt = arguments[1];
        elm.value = txt;
        elm.dispatchEvent(new Event('input'));  // Эмулируем ввод данных
        """
        self.driver.execute_script(js_set_value, search_input, query)

    def click_element(self, locator):
        """
        Ожидание элемента и клик.
        """
        element = wait_for_element(
            self.driver, locator, EC.element_to_be_clickable
            )
        element.click()

    def submit_search(self):
        self.click_element(self.search_button)

    def select_books_category(self):
        wait_for_element(
            self.driver, self.category_books, EC.element_to_be_clickable
        ).click()

    def wait_for_results(self):
        wait_for_element(
            self.driver, self.books_count, EC.presence_of_element_located
        )
        return self.driver.find_element(*self.books_count).text

    def delete_search_query_from_history(self):
        delete_button = wait_for_element(
            self.driver, self.delete_query_cross, EC.element_to_be_clickable
        )
        delete_button.click()
        WebDriverWait(self.driver, 3).until(EC.staleness_of(delete_button))

    def clear_search_box_with_icon(self):
        wait_for_element(
            self.driver, self.clear_icon, EC.element_to_be_clickable
        ).click()

    def click_on_search_box(self):
        self.click_element(self.search_box)

    def is_popular_suggestions_title_correct(self):
        title_element = wait_for_element(
            self.driver, self.suggestions_title, EC.presence_of_element_located
        )
        return title_element.text == "Популярные запросы"

    def get_book_author(self):
        author_element = wait_for_element(
            self.driver, self.book_author, EC.presence_of_element_located
        )
        return author_element.text

    def get_first_book_title(self):
        book_title_locator = (
            By.CSS_SELECTOR, 'article:nth-child(1) .product-title__head'
        )
        title_element = wait_for_element(
            self.driver, book_title_locator, EC.presence_of_element_located
        )
        return title_element.text

    def is_search_success(self):
        success_indicator = (
            By.CSS_SELECTOR, 'div.search-page.js-catalog-container > p'
        )
        try:
            wait_for_element(
                self.driver, success_indicator, EC.presence_of_element_located,
                timeout=10
            )
            return True
        except TimeoutException:
            return False

    def get_empty_result_message(self):
        empty_message_element = wait_for_element(
            self.driver, self.empty_result_message,
            EC.presence_of_element_located, timeout=10
        )
        return empty_message_element.text

    def get_search_history_text(self):
        """
        Получает текст из истории поиска.
        Возвращает пустую строку, если элемента нет.
        """
        try:
            history_element = wait_for_element(
                self.driver, self.search_history_item,
                EC.presence_of_element_located, timeout=5
            )
            return history_element.text
        except TimeoutException:
            return ""

    def is_search_box_active(self):
        """
        Проверяет, активна ли строка поиска.
        Возвращает True, если строка активна; иначе False.
        """
        search_input = self.driver.find_element(*self.search_box)
        return search_input == self.driver.switch_to.active_element
