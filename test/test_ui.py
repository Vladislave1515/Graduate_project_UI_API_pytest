import allure
from pages.Search_Page_UI import SearchPage


@allure.feature('Поиск')
@allure.story('Валидный поиск')
@allure.severity(allure.severity_level.CRITICAL)
class TestSearch:

    @allure.title("Тест валидного поиска")
    @allure.description(
        "Тестирование валидного поиска с запросом 'Гарри Поттер и кубок огня'"
    )
    def test_valid_search(self, browser):
        search_page = SearchPage(browser)

        with allure.step("Ввести запрос в строку поиска"):
            search_page.enter_search_query('Гарри Поттер и кубок огня')

        with allure.step("Отправить запрос поиска"):
            search_page.submit_search()

        with allure.step("Выбрать категорию 'Книги'"):
            search_page.select_books_category()

        with allure.step("Ожидание появления результатов поиска"):
            results_count = int(search_page.wait_for_results())

        with allure.step("Проверка отображения результатов поиска"):
            assert results_count > 0, "Результаты поиска не найдены"


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
@allure.severity(allure.severity_level.CRITICAL)
class TestSearchByAuthor:

    @allure.title("Поиск по автору книги")
    @allure.description(
        "Проверка, что поиск по автору 'роулинг джоан кэтлин' выдаёт "
        "корректные книги"
    )
    def test_search_by_author(self, browser):
        search_page = SearchPage(browser)

        with allure.step("Ввести имя автора в строку поиска"):
            search_page.enter_search_query('роулинг джоан кэтлин')

        with allure.step("Отправить запрос поиска"):
            search_page.submit_search()

        with allure.step("Ожидать загрузку результатов поиска"):
            search_page.wait_for_results()  # Добавлен метод ожидания загрузки

        with allure.step("Получить имя автора из первой карточки книги"):
            first_book_author = search_page.get_book_author()

        with allure.step("Проверить, что автор совпадает"):
            assert 'роулинг' in first_book_author.lower(), (
                f"Ожидался автор 'роулинг', но найден '{first_book_author}'"
            )
