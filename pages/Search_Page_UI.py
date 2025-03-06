from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_box = (By.CSS_SELECTOR, 'input.header-search__input')
        self.search_button = (
            By.CSS_SELECTOR, 'button.header-search__button'
        )
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

    def enter_search_query(self, query):
        wait = WebDriverWait(self.driver, 3)
        search_input = wait.until(
            EC.presence_of_element_located(self.search_box)
        )
        search_input.send_keys(query)

    def submit_search(self):
        wait = WebDriverWait(self.driver, 3)
        wait.until(
            EC.element_to_be_clickable(self.search_button)
        ).click()

    def select_books_category(self):
        wait = WebDriverWait(self.driver, 3)
        wait.until(
            EC.element_to_be_clickable(self.category_books)
        ).click()

    def wait_for_results(self):
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located(self.books_count))
        books_count_element = self.driver.find_element(*self.books_count)
        return int(books_count_element.text)

    def delete_search_query_from_history(self):
        wait = WebDriverWait(self.driver, 3)
        delete_button = wait.until(
            EC.element_to_be_clickable(self.delete_query_cross)
        )
        delete_button.click()
        wait.until(EC.staleness_of(delete_button))

    def clear_search_box_with_icon(self):
        wait = WebDriverWait(self.driver, 3)
        clear_button = wait.until(
            EC.element_to_be_clickable(self.clear_icon)
        )
        clear_button.click()

    def click_on_search_box(self):
        wait = WebDriverWait(self.driver, 3)
        search_box = wait.until(
            EC.element_to_be_clickable(self.search_box)
        )
        search_box.click()

    def is_popular_suggestions_title_correct(self):
        wait = WebDriverWait(self.driver, 3)
        title_element = wait.until(
            EC.presence_of_element_located(self.suggestions_title)
        )
        return title_element.text == "Популярные запросы"
