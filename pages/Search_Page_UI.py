from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
        self.clear_icon = (
            By.CLASS_NAME, 'header-search__clear-icon'
            )
        self.suggestions_title = (
            By.CLASS_NAME, 'search-suggestion-wrapper__title'
            )
        self.book_author = (
            By.CSS_SELECTOR, 'article:nth-child(1) .product-title__author'
            )
        self.empty_result_message = (
            By.CSS_SELECTOR, 'div.catalog-empty-result__container > div > h4'
        )

    def enter_search_query(self, query):
        """
        Вводит запрос в строку поиска. Использует JavaScript для добавления
        сложных символов.
        """
        search_input = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.search_box)
        )
        search_input.click()

        js_add_text_to_input = """
        var elm = arguments[0], txt = arguments[1];
        elm.value += txt;
        elm.dispatchEvent(new Event('change'));
        """
        self.driver.execute_script(js_add_text_to_input, search_input, query)

        try:
            search_input.send_keys(query)
        except Exception:
            self.driver.execute_script(
                "arguments[0].value = arguments[1];", search_input, query
            )

    def submit_search(self):
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(self.search_button)
        ).click()

    def select_books_category(self):
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(self.category_books)
        ).click()

    def wait_for_results(self):
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(self.books_count)
        )
        return self.driver.find_element(*self.books_count).text

    def delete_search_query_from_history(self):
        delete_button = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(self.delete_query_cross)
        )
        delete_button.click()
        WebDriverWait(self.driver, 3).until(EC.staleness_of(delete_button))

    def clear_search_box_with_icon(self):
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(self.clear_icon)
        ).click()

    def click_on_search_box(self):
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(self.search_box)
        ).click()

    def is_popular_suggestions_title_correct(self):
        title_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(self.suggestions_title)
        )
        return title_element.text == "Популярные запросы"

    def get_book_author(self):
        author_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(self.book_author)
        )
        return author_element.text

    def get_first_book_title(self):
        book_title_locator = (
            By.CSS_SELECTOR, 'article:nth-child(1) .product-title__head'
            )
        wait = WebDriverWait(self.driver, 3)
        title_element = wait.until(
            EC.presence_of_element_located(book_title_locator)
            )
        return title_element.text

    def is_search_success(self):
        """
        Проверяет, завершен ли поиск и загрузились ли элементы результатов.
        Возвращает True, если элемент найден, иначе False.
        """
        success_indicator = (
            By.CSS_SELECTOR, 'div.search-page.js-catalog-container > p'
            )
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(success_indicator)
            )
            return True
        except TimeoutException:
            return False

    def get_empty_result_message(self):
        """
        Возвращает текст сообщения об отсутствии результатов,
        если оно существует.
        """
        empty_message_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.empty_result_message)
        )
        return empty_message_element.text
