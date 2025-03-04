from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_box = (By.CSS_SELECTOR, 'input.header-search__input')
        self.search_button = (By.CSS_SELECTOR, 'button.header-search__button')
        self.category_books = (By.XPATH, '//span[contains(@class, "search-categories-tree-item__text") and contains(text(), "Книги")]')
        self.books_count = (By.XPATH, '//span[contains(@class, "search-categories-tree-item__text") and contains(text(), "Книги")]/span[@class="search-categories-tree-item__count"]')

    def enter_search_query(self, query):
        wait = WebDriverWait(self.driver, 3)
        search_input = wait.until(EC.presence_of_element_located(self.search_box))
        search_input.send_keys(query)

    def submit_search(self):
        wait = WebDriverWait(self.driver, 3)
        search_button = wait.until(EC.element_to_be_clickable(self.search_button))
        search_button.click()

    def select_books_category(self):
        wait = WebDriverWait(self.driver, 3)
        books_category = wait.until(EC.element_to_be_clickable(self.category_books))
        books_category.click()

    def wait_for_results(self):
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located(self.books_count))
        books_count_element = self.driver.find_element(*self.books_count)
        return int(books_count_element.text)
