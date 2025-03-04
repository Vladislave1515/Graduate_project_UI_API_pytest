import allure
from pages.Search_Page_UI import SearchPage


@allure.feature('Поиск')
@allure.story('Валидный поиск')
@allure.severity(allure.severity_level.CRITICAL)
class TestSearch:

    @allure.title("Тест валидного поиска")
    @allure.description("Тестирование валидного поиска с запросом 'Гарри Поттер и кубок огня'")
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
