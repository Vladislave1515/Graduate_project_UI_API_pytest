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


def handle_popups(driver):
    """
    Обрабатывает (ждет и закрывает) несколько всплывающих окон.
    """
    logging.info("Обработка всплывающих окон.")
    popup_selectors = [
        ".change-city-container > div",
        ".popmechanic-main",
        ".app-wrapper__content > div.cookie-notice",
        ".app-wrapper__push-notification.push-notification--active > div",
    ]
    close_button_selectors = [
        ".change-city__button--accept.blue",
        ".popmechanic-close",
        ".app-wrapper__content > div.cookie-notice > button",
        ".button.button.push-notification__no-button.white",
    ]

    for popup_selector, close_button_selector in zip(
        popup_selectors, close_button_selectors
    ):
        try:
            # Ждать появления всплывающего окна
            popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, popup_selector))
            )
            logging.info(f"Всплывающее окно найдено: '{popup_selector}'.")

            # Сделать всплывающее окно видимым, если оно скрыто
            driver.execute_script(
                "arguments[0].style.display = 'block';", popup
                )

            # Убедиться, что кнопка закрытия кликабельна
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, close_button_selector))
            )
            logging.info(
                f"Кнопка закрытия '{close_button_selector}' доступна."
                )

            # Нажать на кнопку закрытия
            close_button.click()
            logging.info(
                f"Всплывающее окно '{popup_selector}' успешно закрыто."
                )
        except TimeoutException:
            logging.warning(
                f"Всплывающее окно '{popup_selector}' не появилось вовремя."
                )
        except Exception as e:
            logging.error(
                f"Ошибка при обработке окна '{popup_selector}': {str(e)}"
                )


def wait_for_element(driver, locator, condition, timeout=8):
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
            '.header-search > div > form > input'
        )
        self.search_button = (
            By.CSS_SELECTOR,
            '.header-search > div > form > button > svg'
        )
        self.category_books = (
            By.CSS_SELECTOR,
            '.filter-search-categories > ul > li:nth-child(1) > button'
        )
        self.books_count = (
            By.CSS_SELECTOR,
            '.filter-search-categories > ul > li:nth-child(2) > button > span'
        )
        self.delete_query_cross = (
            By.CSS_SELECTOR,
            '.app-search__suggests > div:nth-child(2) '
            '> ul > li > a > div > button'
        )
        self.clear_icon = (
            By.CSS_SELECTOR,
            '.header__catalog > div > div > div > form > div > button'
        )
        self.suggestions_title = (
            By.CSS_SELECTOR,
            '.suggests-list__item > span'
        )
        self.book_author = (
            By.CSS_SELECTOR,
            '.product-card__caption > span'
        )
        self.empty_result_message = (
            By.CSS_SELECTOR,
            '.catalog-stub__content--row > h4'
        )
        self.search_history_item = (
            By.CSS_SELECTOR,
            "div.header-search-results ul li div div span"
        )
        self.book_title_locator = (
            By.CSS_SELECTOR,
            '.product-card__caption > a > h3'
        )
        self.success_indicator = (
            By.CSS_SELECTOR,
            '.global-container-vertical.search-page > h1'
        )

        logging.info("SearchPage инициализирован.")

    def enter_search_query_with_keys(self, query):
        logging.info(f"Ввод запроса '{query}' с использованием send_keys.")
        search_input = wait_for_element(
            self.driver, self.search_box,
            EC.element_to_be_clickable
        )
        search_input.click()
        search_input.clear()
        search_input.send_keys(query)
        logging.info("Запрос успешно введён.")

        # Обработка всплывающих окон после ввода запроса
        handle_popups(self.driver)
        logging.info("Обработка всплывающих окон завершена.")

    def enter_search_query_with_js(self, query):
        logging.info(f"Ввод запроса '{query}' с использованием JavaScript.")
        search_input = wait_for_element(
            self.driver, self.search_box,
            EC.element_to_be_clickable
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

        # Обработка всплывающих окон после ввода запроса
        handle_popups(self.driver)
        logging.info("Обработка всплывающих окон завершена.")

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
            WebDriverWait(self.driver, 7).until(EC.staleness_of(delete_button))
            logging.info("Запрос успешно удалён из истории.")
        except TimeoutException:
            logging.error("Не удалось удалить запрос из истории.")

    def clear_search_box_with_icon(self):
        logging.info("Очистка строки поиска.")
        try:
            cross = wait_for_element(
                self.driver, self.clear_icon,
                EC.element_to_be_clickable
            )
            cross.click()
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
