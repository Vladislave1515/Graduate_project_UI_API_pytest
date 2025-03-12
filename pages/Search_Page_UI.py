import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s"
)


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
        self.search_box = (
            By.CSS_SELECTOR,
            'input.header-search__input'
        )
        self.search_button = (
            By.CSS_SELECTOR,
            'button.header-search__button'
        )
        self.category_books = (
            By.CSS_SELECTOR,
            '.search-categories__tree > ul > li:nth-child(1) > div > span'
        )
        self.books_count = (
            By.CSS_SELECTOR,
            '.search-categories__tree > ul > li:nth-child'
            '(2) > div > span > span'
        )
        self.delete_query_cross = (
            By.CSS_SELECTOR,
            '.header-search-results__row > ul > li > div > button > svg'
        )
        self.clear_icon = (
            By.CLASS_NAME,
            'header-search__clear-icon'
        )
        self.suggestions_title = (
            By.CLASS_NAME,
            'search-suggestion-wrapper__title'
        )
        self.book_author = (
            By.CSS_SELECTOR,
            'article:nth-child(1) .product-title__author'
        )
        self.empty_result_message = (
            By.CSS_SELECTOR,
            'div.catalog-empty-result__container > div > h4'
        )
        self.search_history_item = (
            By.CSS_SELECTOR,
            "div.header-search-results ul li div div span"
        )
        self.book_title_locator = (
            By.CSS_SELECTOR,
            'article:nth-child(1) .product-title__head'
        )
        self.success_indicator = (
            By.CSS_SELECTOR, 'div.search-page.js-catalog-container > p'
        )
        logging.info("SearchPage инициализирован.")

    def enter_search_query_with_keys(self, query):
        logging.info(f"Ввод запроса '{query}' с использованием send_keys.")
        search_input = wait_for_element(
            self.driver, self.search_box, EC.element_to_be_clickable
        )
        search_input.click()
        search_input.clear()
        search_input.send_keys(query)
        logging.info("Запрос успешно введён.")

    def enter_search_query_with_js(self, query):
        logging.info(f"Ввод запроса '{query}' с использованием JavaScript.")
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
        logging.info("Запрос успешно введён с использованием JavaScript.")

    def click_element(self, locator):
        logging.info(f"Попытка кликнуть по элементу: {locator}.")
        try:
            wait_for_element(
                self.driver, locator,
                EC.element_to_be_clickable
            ).click()
            logging.info("Клик по элементу выполнен.")
        except TimeoutException:
            logging.error(f"Не удалось найти элемент: {locator}.")

    def submit_search(self):
        logging.info("Отправка поискового запроса.")
        self.click_element(self.search_button)

    def select_books_category(self):
        logging.info("Выбор категории 'Книги'.")
        try:
            wait_for_element(
                self.driver, self.category_books,
                EC.element_to_be_clickable
            ).click()
            logging.info("Категория 'Книги' успешно выбрана.")
        except TimeoutException:
            logging.error("Не удалось выбрать категорию 'Книги'.")

    def wait_for_results(self):
        logging.info("Ожидание результатов поиска.")
        try:
            wait_for_element(
                self.driver, self.books_count,
                EC.presence_of_element_located
            )
            results = self.driver.find_element(*self.books_count).text
            logging.info(f"Найдены результаты: {results}.")
            return results
        except TimeoutException:
            logging.error("Результаты поиска не найдены.")
            return None

    def delete_search_query_from_history(self):
        logging.info("Удаление запроса из истории.")
        try:
            delete_button = wait_for_element(
                self.driver, self.delete_query_cross,
                EC.element_to_be_clickable
            )
            delete_button.click()
            WebDriverWait(self.driver, 3).until(EC.staleness_of(delete_button))
            logging.info("Запрос успешно удалён из истории.")
        except TimeoutException:
            logging.error("Не удалось удалить запрос из истории.")

    def clear_search_box_with_icon(self):
        logging.info("Очистка строки поиска.")
        try:
            wait_for_element(
                self.driver, self.clear_icon,
                EC.element_to_be_clickable
            ).click()
            logging.info("Строка поиска успешно очищена.")
        except TimeoutException:
            logging.error("Кнопка очистки не найдена.")

    def click_on_search_box(self):
        logging.info("Клик по строке поиска.")
        self.click_element(self.search_box)

    def is_popular_suggestions_title_correct(self):
        logging.info("Проверка заголовка популярных запросов.")
        try:
            title_element = wait_for_element(
                self.driver, self.suggestions_title,
                EC.presence_of_element_located
            )
            is_correct = title_element.text == "Популярные запросы"
            logging.info(f"Заголовок корректен: {is_correct}.")
            return is_correct
        except TimeoutException:
            logging.error("Заголовок популярных запросов не найден.")
            return False

    def get_book_author(self):
        logging.info("Получение автора книги.")
        try:
            author_element = wait_for_element(
                self.driver, self.book_author,
                EC.presence_of_element_located
            )
            logging.info(f"Автор книги: {author_element.text}.")
            return author_element.text
        except TimeoutException:
            logging.error("Не удалось найти автора книги.")
            return ""

    def get_first_book_title(self):
        logging.info("Получение названия первой книги.")
        try:
            title_element = wait_for_element(
                self.driver, self.book_title_locator,
                EC.presence_of_element_located
            )
            logging.info(f"Название книги: {title_element.text}.")
            return title_element.text
        except TimeoutException:
            logging.error("Не удалось найти название первой книги.")
            return ""

    def is_search_success(self):
        logging.info("Проверка успешности поиска.")
        try:
            wait_for_element(
                self.driver, self.success_indicator,
                EC.presence_of_element_located
            )
            logging.info("Поиск завершён успешно.")
            return True
        except TimeoutException:
            logging.error("Поиск не дал результатов.")
            return False

    def get_empty_result_message(self):
        logging.info("Получение сообщения об отсутствии результатов.")
        try:
            empty_message_element = wait_for_element(
                self.driver, self.empty_result_message,
                EC.presence_of_element_located
            )
            logging.info(f"Сообщение: {empty_message_element.text}.")
            return empty_message_element.text
        except TimeoutException:
            logging.error("Сообщение об отсутствии результатов не найдено.")
            return ""

    def get_search_history_text(self):
        logging.info("Получение текста из истории поиска.")
        try:
            history_element = wait_for_element(
                self.driver, self.search_history_item,
                EC.presence_of_element_located
            )
            logging.info(f"Текст из истории поиска: {history_element.text}.")
            return history_element.text
        except TimeoutException:
            logging.error("История поиска не найдена.")
            return ""

    def is_search_box_active(self):
        logging.info("Проверка активности строки поиска.")
        search_input = self.driver.find_element(*self.search_box)
        is_active = search_input == self.driver.switch_to.active_element
        return is_active
