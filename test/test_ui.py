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
            results_count = search_page.wait_for_results()

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
