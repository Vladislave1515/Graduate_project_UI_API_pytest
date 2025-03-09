import allure
import pytest
from pages.Search_Page_UI import SearchPage


@allure.feature('Поиск')
@allure.story('Валидный запрос')
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Поиск с валидным запросом")
@allure.description(
    "Тестирование функции поиска с использованием валидного запроса "
    "'Гарри Поттер и кубок огня'"
)
@pytest.mark.ui
def test_valid_search(browser):
    search_page = SearchPage(browser)
    with allure.step("Ввести и отправить запрос в строку поиска"):
        search_page.enter_search_query_with_keys("Гарри Поттер и кубок огня")
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
@pytest.mark.ui
class TestSearchHistory:

    @allure.title("Удаление запроса из истории поиска")
    @allure.description(
        "Тестирование удаления запроса 'Книга Гарри Поттер и кубок огня' "
        "из истории поиска"
    )
    def test_delete_query(self, browser):
        search_page = SearchPage(browser)
        with allure.step("Ввести и отправить запрос в строку поиска"):
            search_page.enter_search_query_with_keys(
                'Книга Гарри Поттер и кубок огня'
                )
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
@pytest.mark.ui
def test_by_author(browser):
    search_page = SearchPage(browser)
    with allure.step("Ввести и отправить запрос в строку поиска"):
        search_page.enter_search_query_with_keys("роулинг джоан кэтлин")
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
@pytest.mark.ui
def test_wrong_keyboard_layout(browser):
    search_page = SearchPage(browser)
    with allure.step("Ввести и отправить запрос в строку поиска"):
        search_page.enter_search_query_with_keys("ufhbb gjnnth")
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
@pytest.mark.ui
def test_with_special_char(browser):
    search_page = SearchPage(browser)
    with allure.step("Ввести запрос с валидным названием и спецсимволами"):
        query = "Гарри Поттер ()_+{}|:”>?<Ё!”№;:?*()_+/Ъ,/.,;’[]^$&*"
        search_page.enter_search_query_with_keys(query)
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


@allure.feature('Поиск')
@allure.story('Поиск с использованием только эмодзи')
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Поиск только с использованием эмодзи")
@allure.description(
    "Тестирование поиска с использованием только эмодзи. "
    "Ожидается, что система ничего не найдет и выдаст сообщение "
    "'Похоже, у нас такого нет'."
)
@pytest.mark.ui
def test_with_emojis(browser):
    search_page = SearchPage(browser)

    with allure.step("Ввести эмодзи в строку поиска через JavaScript"):
        emoji_query = "\U0001F600\U0001F600\U0001F600\U0001F600"
        search_page.enter_search_query_with_js(emoji_query)

    with allure.step("Отправить запрос"):
        search_page.submit_search()

    with allure.step("Проверить сообщение об отсутствии результатов"):
        empty_message = search_page.get_empty_result_message()
        assert empty_message == "Похоже, у нас такого нет", (
            f"Ожидалось сообщение 'Похоже, у нас такого нет', "
            f"но получено: '{empty_message}'."
        )


@allure.feature('Поиск')
@allure.story('Ввод более 150 символов')
@allure.severity(allure.severity_level.NORMAL)
@allure.title(
    "Проверка ограничения на длину ввода в строке поиска после отправки")
@allure.description(
    "Тестирование функции строки поиска при вводе более 150 символов. "
    "Ожидается, что система обрежет запрос до 150 символов, при поиске."
)
@pytest.mark.ui
def test_input_150_char(browser):
    search_page = SearchPage(browser)

    with allure.step("Ввести строку длиной более 150 символов вручную"):
        long_query = "a" * 200  # Создаём строку из 200 символов
        search_page.enter_search_query_with_keys(long_query)

    with allure.step("Нажать кнопку поиска"):
        search_page.submit_search()

    with allure.step("Кликнуть на строку поиска для активации истории"):
        search_page.click_on_search_box()

    with allure.step("Получить текст из истории поиска"):
        history_text = search_page.get_search_history_text()

    with allure.step("Проверить, что длина строки из истории \n"
                     "поиска не превышает 150 символов"):
        assert len(history_text) <= 150, (
            f"Превышено ограничение: {len(history_text)} символов"
        )


@allure.feature('Поиск')
@allure.story('Пустой запрос')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Поиск с пустым запросом")
@allure.description(
    "Тестирование поведения системы при поиске с пустым запросом. "
    "Ожидается, что поиск не выполнится, поле поиска станет неактивным, "
    "а локатор для проверки результатов не найдётся."
)
@pytest.mark.ui
def test_empty_search_query(browser):
    search_page = SearchPage(browser)

    with allure.step("Очистить строку поиска и попытаться выполнить поиск"):
        search_page.enter_search_query_with_keys("")
        search_page.submit_search()

    with allure.step("Проверить, что строка поиска становится неактивной"):
        search_box_state = search_page.is_search_box_active()
        assert not search_box_state, "Строка поиска остаётся активной после \n"
        "выполнения пустого запроса!"

    with allure.step("Проверить, что поиск не выполнился"):
        search_success = search_page.is_search_success()
        assert not search_success, "Поиск выполнен, хотя запрос был пустым!"
