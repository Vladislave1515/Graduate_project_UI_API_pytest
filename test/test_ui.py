import allure
from pages.Search_Page_UI import SearchPage


@allure.feature('Поиск')
@allure.story('Валидный запрос')
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Поиск с валидным запросом")
@allure.description(
    "Тестирование функции поиска с использованием валидного запроса "
    "'Гарри Поттер и кубок огня'"
)
def test_valid_search(browser):
    search_page = SearchPage(browser)
    with allure.step("Ввести и отправить запрос в строку поиска"):
        search_page.enter_search_query("Гарри Поттер и кубок огня")
        search_page.submit_search()
    with allure.step("Проверить успешность выполнения поиска"):
        assert search_page.is_search_success(), (
            "Поиск не выполнен: результаты не загрузились."
        )
    with allure.step("Выбрать категорию 'Книги'"):
        search_page.select_books_category()
    with allure.step("Проверить количество найденных результатов"):
        results_count = search_page.wait_for_results()
        assert int(results_count) > 0, "Результаты поиска отсутствуют!"


@allure.feature('Поиск')
@allure.story('Удаление запроса из истории поиска')
@allure.severity(allure.severity_level.CRITICAL)
class TestSearchHistory:

    @allure.title("Удаление запроса из истории поиска")
    @allure.description(
        "Тестирование удаления запроса 'Книга Гарри Поттер и кубок огня' "
        "из истории поиска"
    )
    def test_delete_search_query(self, browser):
        search_page = SearchPage(browser)
        with allure.step("Ввести и отправить запрос в строку поиска"):
            search_page.enter_search_query('Книга Гарри Поттер и кубок огня')
            search_page.submit_search()
        with allure.step("Очистить строку поиска через крестик"):
            search_page.clear_search_box_with_icon()
        with allure.step("Активировать строку поиска"):
            search_page.click_on_search_box()
        with allure.step("Удалить запрос из истории поиска"):
            search_page.delete_search_query_from_history()
        with allure.step("Проверка заголовка популярных запросов"):
            assert search_page.is_popular_suggestions_title_correct(), (
                "Заголовок популярных запросов неверен или отсутствует"
            )


@allure.feature('Поиск')
@allure.story('Поиск по автору')
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Поиск книг по автору")
@allure.description(
    "Тестирование функции поиска книг по автору "
    "'роулинг джоан кэтлин'"
)
def test_search_by_author(browser):
    search_page = SearchPage(browser)
    with allure.step("Ввести и отправить запрос в строку поиска"):
        search_page.enter_search_query("роулинг джоан кэтлин")
        search_page.submit_search()
    with allure.step("Проверить успешность выполнения поиска"):
        assert search_page.is_search_success(), (
            "Поиск не выполнен: результаты не загрузились."
        )
    with allure.step("Проверить автора первой книги в результатах поиска"):
        author = search_page.get_book_author()
        assert "роулинг" in author.lower(), (
            f"Ожидалось имя автора 'роулинг', но найдено '{author}'."
        )


@allure.feature('Поиск')
@allure.story('Неправильная раскладка клавиатуры')
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Поиск с неправильной раскладкой")
@allure.description(
    "Тестирование обработки запроса, введенного с неправильной раскладкой "
    "клавиатуры ('ufhbb gjnnth')"
)
def test_search_with_wrong_keyboard_layout(browser):
    search_page = SearchPage(browser)
    with allure.step("Ввести и отправить запрос в строку поиска"):
        search_page.enter_search_query("ufhbb gjnnth")
        search_page.submit_search()
    with allure.step("Проверить успешность выполнения поиска"):
        assert search_page.is_search_success(), (
            "Поиск не выполнен: результаты не загрузились."
        )
    with allure.step("Проверить название первой книги в результатах поиска"):
        first_book_title = search_page.get_first_book_title()
        assert 'гарри поттер' in first_book_title.lower(), (
            "Ожидалось название 'гарри поттер', но найдено '\n"
            f"{first_book_title}'"
        )


@allure.feature('Поиск')
@allure.story('Негативный тест: Валидное название товара со спецсимволами')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Поиск с валидным названием и специальными символами")
@allure.description(
    "Тестирование обработки системы при поиске запроса с валидным названием "
    "товара и набором специальных символов. Проверяется, что система выдаёт "
    "релевантные результаты."
)
def test_with_special_char(browser):
    search_page = SearchPage(browser)

    with allure.step("Ввести запрос с валидным названием и спецсимволами"):
        query = "Гарри Поттер ()_+{}|:”>?<Ё!”№;:?*()_+/Ъ,/.,;’[]^$&*"
        search_page.enter_search_query(query)

    with allure.step("Отправить запрос"):
        search_page.submit_search()

    with allure.step("Проверить успешность выполнения поиска"):
        assert search_page.is_search_success(), (
            "Поиск не выполнен: результаты не загрузились."
        )

    with allure.step("Проверить название первой книги в результатах поиска"):
        first_book_title = search_page.get_first_book_title()
        assert 'гарри поттер' in first_book_title.lower(), (
            "Ожидалось название 'гарри поттер' в результатах поиска, \n"
            f"но найдено: '{first_book_title}'."
        )
