import logging
import allure
import pytest
from pages.Search_Page_UI import SearchPage
from pages.Cart_Page_UI import CartPage


class TestSearch:
    @allure.feature('Поиск')
    @allure.story('Валидный запрос')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Поиск с валидным запросом")
    @allure.description(
        "Тестирование функции поиска с использованием валидного запроса "
        "'Гарри Поттер и кубок огня'"
    )
    @pytest.mark.ui
    def test_valid_search(self, browser):
        search_page = SearchPage(browser)
        with allure.step("Ввести и отправить запрос в строку поиска"):
            search_page.enter_search_query_with_keys(
                "Гарри Поттер и кубок огня"
                )
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
    @allure.title("Удаление запроса из истории поиска")
    @allure.description(
            "Тестирование удаления запроса 'Книга Гарри Поттер и кубок огня' "
            "из истории поиска"
        )
    @pytest.mark.ui
    def test_search_delete_query(self, browser):
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
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Поиск книг по автору")
    @allure.description(
        "Тестирование функции поиска книг по автору "
        "'роулинг джоан кэтлин'"
    )
    @pytest.mark.ui
    def test_search_by_author(self, browser):
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
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Поиск с неправильной раскладкой")
    @allure.description(
        "Тестирование обработки запроса, введенного с неправильной раскладкой "
        "клавиатуры ('ufhbb gjnnth')"
    )
    @pytest.mark.ui
    def test_search_wrong_keyboard_layout(self, browser):
        search_page = SearchPage(browser)
        with allure.step("Ввести и отправить запрос в строку поиска"):
            search_page.enter_search_query_with_keys("ufhbb gjnnth")
            search_page.submit_search()
        with allure.step("Проверить успешность выполнения поиска"):
            assert search_page.is_search_success(), (
                "Поиск не выполнен: результаты не загрузились."
            )
        with allure.step("Проверить название первой книги в результатах"):
            first_book_title = search_page.get_first_book_title()
            assert 'гарри поттер' in first_book_title.lower(), (
                "Ожидалось название 'гарри поттер', но найдено '\n"
                f"{first_book_title}'"
            )

    @allure.feature('Поиск')
    @allure.story('Негативный тест: Валидное название товара с спецсимволами')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Поиск с валидным названием и специальными символами")
    @allure.description(
        "Тестирование обработки системы при поиске запроса"
        " с валидным названием товара и набором специальных символов."
        "Проверяется, что система выдаёт релевантные результаты."
    )
    @pytest.mark.ui
    def test_search_with_special_char(self, browser):
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
        with allure.step("Проверить название первой книги в результатах"):
            first_book_title = search_page.get_first_book_title()
            assert 'гарри поттер' in first_book_title.lower(), (
                "Ожидалось название 'гарри поттер' в результатах поиска, \n"
                f"но найдено: '{first_book_title}'."
            )

    @allure.feature('Поиск')
    @allure.story('Негативный тест: Поиск с использованием только эмодзи')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Поиск только с использованием эмодзи")
    @allure.description(
        "Тестирование поиска с использованием только эмодзи. "
        "Ожидается, что система ничего не найдет и выдаст сообщение "
        "'Похоже, у нас такого нет'."
    )
    @pytest.mark.ui
    def test_search_with_emojis(self, browser):
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
    @allure.story('Негативный тест: Ввод более 150 символов')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title(
        "Проверка ограничения на длину ввода в строке поиска после отправки")
    @allure.description(
        "Тестирование функции строки поиска при вводе более 150 символов. "
        "Ожидается, что система обрежет запрос до 150 символов, при поиске."
    )
    @pytest.mark.ui
    def test_search_input_150_char(self, browser):
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
    @allure.story('Негативный тест: Пустой запрос')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Поиск с пустым запросом")
    @allure.description(
        "Тестирование поведения системы при поиске с пустым запросом. "
        "Ожидается, что поиск не выполнится, поле поиска станет неактивным, "
        "а локатор для проверки результатов не найдётся."
    )
    @pytest.mark.ui
    def test_empty_search_query(self, browser):
        search_page = SearchPage(browser)

        with allure.step("Очистить строку поиска и выполнить поиск"):
            search_page.enter_search_query_with_keys("")
            search_page.submit_search()

        with allure.step("Проверить, что строка поиска становится неактивной"):
            search_box_state = search_page.is_search_box_active()
            assert not search_box_state, "Строка поиска остаётся \n"
            "активной после выполнения пустого запроса!"

        with allure.step("Проверить, что поиск не выполнился"):
            search_success = search_page.is_search_success()
            assert not search_success, "Поиск выполнен, хотя запрос был пуст!"

    @allure.feature('Поиск')
    @allure.story('Негативный тест: Невалидный запрос')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Поиск с невалидным запросом")
    @allure.description(
        "Тестирование поиска с использованием невалидного запроса. "
        "Ожидается, что система не найдёт ничего и покажет сообщение "
        "'Похоже, у нас такого нет'."
    )
    @pytest.mark.ui
    def test_invalid_search(self, browser):
        search_page = SearchPage(browser)

        with allure.step("Ввести невалидный запрос в строку поиска"):
            invalid_query = "aslkdjaslkdjaslkdja"  # Пример невалидного запроса
            search_page.enter_search_query_with_keys(invalid_query)

        with allure.step("Отправить запрос"):
            search_page.submit_search()

        with allure.step("Проверить сообщение об отсутствии результатов"):
            empty_message = search_page.get_empty_result_message()
            assert empty_message == "Похоже, у нас такого нет", (
                f"Ожидалось сообщение 'Похоже, у нас такого нет', "
                f"но получено: '{empty_message}'."
            )


class TestCart:
    @allure.feature('Корзина')
    @allure.story('Добавление товара')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Добавление товара в корзину через кнопку 'КУПИТЬ'")
    @allure.description(
        "Тестирование функциональности добавления товара"
        "в корзину через кнопку 'КУПИТЬ'. "
        "Ожидается, что товар будет добавлен в корзину."
    )
    @pytest.mark.ui
    def test_add_to_cart(self, browser):
        search_page = SearchPage(browser)
        cart_page = CartPage(browser)

        with allure.step("Выполнить валидный поисковой запрос 'Гарри Поттер'"):
            search_page.enter_search_query_with_keys("Гарри Поттер")
            search_page.submit_search()

        with allure.step("Нажать кнопку 'КУПИТЬ' для добавления \n"
                         "товара в корзину"):
            cart_page.click_buy_button()

        with allure.step("Проверить, что товар добавлен в корзину"):
            cart_count = cart_page.get_cart_item_count()
            assert cart_count > 0, "Товар не был добавлен в корзину!"

    @allure.feature('Корзина')
    @allure.story('Удаление товара')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление товара из корзины")
    @allure.description(
        "Тестирование удаления товара из корзины."
        "Ожидается, что после нажатия кнопки удаления товар будет удалён,"
        " и появится сообщение об удалении."
    )
    @pytest.mark.ui
    def test_remove_item_from_cart(self, browser):
        search_page = SearchPage(browser)
        cart_page = CartPage(browser)

        with allure.step("Добавить товар в корзину"):
            search_page.enter_search_query_with_keys("гарри поттер")
            search_page.submit_search()
            cart_page.click_buy_button()

        with allure.step("Перейти в корзину"):
            cart_page.open_cart()

        with allure.step("Удалить товар из корзины"):
            cart_page.remove_item_from_cart()

        with allure.step("Проверить, что товар удалён из корзины"):
            notification_text = cart_page.get_notification_message()
            print(f"Полученное сообщение: '{notification_text}'")
            assert notification_text.strip() == "Удалили товар из корзины.", (
                f"Ожидалось сообщение 'Удалили товар из корзины.', "
                f"но получено: '{notification_text.strip()}'."
            )

    @allure.feature('Корзина')
    @allure.story('Возврат удалённого товара в корзину')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Возврат удалённого товара через кнопку 'ВЕРНУТЬ В КОРЗИНУ'")
    @allure.description(
        "Тестирование функциональности возврата удалённого товара"
        " в корзину через кнопку 'ВЕРНУТЬ В КОРЗИНУ'. "
        "Ожидается, что товар будет возвращён в корзину."
    )
    @pytest.mark.ui
    def test_return_to_cart(self, browser):
        search_page = SearchPage(browser)
        cart_page = CartPage(browser)

        with allure.step("Добавить товар в корзину"):
            search_page.enter_search_query_with_keys("Гарри Поттер")
            search_page.submit_search()
            cart_page.click_buy_button()

        with allure.step("Удалить товар из корзины"):
            cart_page.open_cart()
            cart_page.remove_item_from_cart()

        with allure.step("Подождать обновления корзины после удаления товара"):
            cart_page.cart_update()

        with allure.step("Вернуть удалённый товар обратно в корзину"):
            cart_page.click_return_to_cart_button()

        with allure.step("Проверить, что товар снова добавлен в корзину"):
            cart_count = cart_page.get_cart_item_count()
            assert cart_count > 0, "Товар не был возвращён в корзину!"

    @allure.feature('Корзина')
    @allure.story('Изменение количества товара в корзине')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Изменение количества товара в корзине через ручной ввод")
    @allure.description(
        "Тестирование изменения количества товара"
        " в корзине через ручной ввод. "
        "Ожидается, что количество товара и итоговая цена изменятся"
        " в соответствии с вводимым числом."
    )
    @pytest.mark.ui
    def test_change_item_quantity_in_cart(self, browser):
        search_page = SearchPage(browser)
        cart_page = CartPage(browser)

        with allure.step("Добавить товар в корзину"):
            search_page.enter_search_query_with_keys("Гарри Поттер")
            search_page.submit_search()
            cart_page.click_buy_button()

        with allure.step("Перейти в корзину"):
            cart_page.open_cart()

        with allure.step("Изменить количество товара в корзине на 3"):
            cart_page.set_item_quantity(3)
        with allure.step("Подождать обновления цены товара"):
            cart_page.wait_price_update()

        with allure.step("Проверить, что количество товара обновилось"):
            quantity = cart_page.get_item_quantity()
            assert quantity == 3, "Ожидалось количество 3,"
            f" но получено {quantity}"

        with allure.step("Проверить, что итоговая цена обновилась"):
            total_price = cart_page.get_total_price()
            expected_price = cart_page.calculate_expected_price(quantity=3)
            assert total_price == expected_price, (
                f"Ожидалась итоговая цена {expected_price},"
                f" но получено {total_price}"
            )

    @allure.feature('Корзина')
    @allure.story('Изменение количества товара в корзине')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Изменение количества товара через кнопку '+'")
    @allure.description(
        "Тест проверяет, что после нажатия кнопки '+' количество товара "
        "увеличивается, а итоговая цена пересчитывается корректно."
    )
    @pytest.mark.ui
    def test_increase_item_quantity(self, browser):
        search_page = SearchPage(browser)
        cart_page = CartPage(browser)

        with allure.step("Добавить товар в корзину"):
            search_page.enter_search_query_with_keys("Гарри Поттер")
            search_page.submit_search()
            cart_page.click_buy_button()

        with allure.step("Перейти в корзину"):
            cart_page.open_cart()

        with allure.step("Получить текущее количество и цену товара"):
            initial_quantity = cart_page.get_cart_item_count()
            initial_price = cart_page.get_total_price()
            logging.info(
                "Изначальное количество: "
                f"{initial_quantity}, цена: {initial_price}."
                )

        with allure.step("Нажать на кнопку '+' для увеличения количества"):
            cart_page.click_increase_quantity_button()

        with allure.step("Подождать обновления количества и цены"):
            cart_page.wait_price_update()

        with allure.step("Проверить, что количество увеличилось на 1"):
            updated_quantity = cart_page.get_item_quantity()
            assert updated_quantity == initial_quantity + 1, (
                "Ожидалось количество "
                f"{initial_quantity + 1}, но получено {updated_quantity}."
            )

        with allure.step("Проверить, что итоговая цена изменилась корректно"):
            updated_price = cart_page.get_total_price()
            expected_price = cart_page.calculate_expected_price(
                updated_quantity
                )
            assert updated_price == expected_price, (
                "Ожидалась итоговая цена "
                f"{expected_price}, но получено {updated_price}."
            )

    @allure.feature('Корзина')
    @allure.story('Изменение количества товара в корзине')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Изменение количества товара через кнопку '-'")
    @allure.description(
        "Тест проверяет, что после нажатия кнопки '-' количество товара "
        "уменьшается, а итоговая цена пересчитывается корректно."
    )
    @pytest.mark.ui
    def test_decrease_item_quantity(self, browser):
        search_page = SearchPage(browser)
        cart_page = CartPage(browser)

        with allure.step("Добавить товар в корзину"):
            search_page.enter_search_query_with_keys("Гарри Поттер")
            search_page.submit_search()
            cart_page.click_buy_button()

        with allure.step("Перейти в корзину"):
            cart_page.open_cart()

        with allure.step("Установить количество товара равным 3 вручную"):
            cart_page.set_item_quantity(3)
            cart_page.wait_price_update()

        with allure.step("Нажать на кнопку '-' для уменьшения количества"):
            cart_page.click_decrease_quantity_button()

        with allure.step("Подождать обновления количества и цены"):
            cart_page.wait_price_update()

        with allure.step("Проверить, что количество уменьшилось на 1"):
            updated_quantity = cart_page.get_item_quantity()
            assert updated_quantity == 2, (
                "Ожидалось количество 2, но получено "
                f"{updated_quantity}."
            )

    @allure.feature('Корзина')
    @allure.story(
        'Негативный тест: Изменение количества товара '
        'на значение больше допустимого'
        )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Ввод количества товара больше допустимого")
    @allure.description(
        "Тест проверяет, что при вводе количества товара,"
        "превышающего максимально допустимое, значение изменяется "
        "на максимально допустимое для данного товара."
    )
    @pytest.mark.ui
    def test_set_quantity_above_max(self, browser):
        search_page = SearchPage(browser)
        cart_page = CartPage(browser)

        with allure.step(
            "Выполнить валидный поисковой запрос для поиска товара"
                ):
            search_page.enter_search_query_with_keys("Гарри Поттер")
            search_page.submit_search()

        with allure.step("Добавить товар в корзину"):
            cart_page.click_buy_button()

        with allure.step("Перейти в корзину"):
            cart_page.open_cart()

        with allure.step(
            "Попробовать ввести количество, превышающее максимально допустимое"
                ):
            cart_page.set_item_quantity(2000)

        with allure.step("Подождать обновления количества и цены"):
            cart_page.wait_price_update()

        with allure.step(
            "Получить максимально допустимое количество из 'max'"
                ):
            max_quantity = cart_page.get_max_allowed_quantity()

        with allure.step(
            "Проверить, что количество товара изменилось на максимальное"
                ):
            actual_quantity = cart_page.get_item_quantity()
            assert actual_quantity == max_quantity, (
                f"Ожидалось количество {max_quantity}, \n"
                f"но получено {actual_quantity}."
            )

    @allure.feature('Корзина')
    @allure.story(
        'Негативный тест: Изменение количества товара на нулевое значение'
        )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Ввод количества товара равным нулю")
    @allure.description(
        "Тест проверяет, что при вводе количества товара, равного нулю, "
        "значение изменяется на минимально допустимое (1)."
    )
    @pytest.mark.ui
    def test_set_quantity_to_zero(self, browser):
        search_page = SearchPage(browser)
        cart_page = CartPage(browser)

        with allure.step("Выполнить валидный поисковой запроc"):
            search_page.enter_search_query_with_keys("Гарри Поттер")
            search_page.submit_search()

        with allure.step("Добавить товар в корзину"):
            cart_page.click_buy_button()

        with allure.step("Перейти в корзину"):
            cart_page.open_cart()

        with allure.step("Попробовать ввести количество, равное нулю"):
            cart_page.set_item_quantity(0)

        with allure.step(
            "Кликнуть на другой элемент для обновления количества"
                ):
            search_page.click_element(search_page.search_button)

        with allure.step("Проверить, что количество товара изменилось на 1"):
            actual_quantity = cart_page.get_item_quantity()
            assert actual_quantity == 1, (
                f"Ожидалось количество 1, но получено {actual_quantity}."
            )

    @allure.feature('Корзина')
    @allure.story(
        'Негативный тест: Изменение количества товара '
        'на отрицательное значение'
        )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Ввод количества товара отрицательным значением")
    @allure.description(
        "Тест проверяет, что при вводе отрицательного количества товара, "
        "значение изменяется на минимально допустимое (1)."
    )
    @pytest.mark.ui
    def test_set_quantity_to_negative(self, browser):
        search_page = SearchPage(browser)
        cart_page = CartPage(browser)

        with allure.step("Выполнить валидный поисковой запрос"):
            search_page.enter_search_query_with_keys("Гарри Поттер")
            search_page.submit_search()

        with allure.step("Добавить товар в корзину"):
            cart_page.click_buy_button()

        with allure.step("Перейти в корзину"):
            cart_page.open_cart()

        with allure.step("Попробовать ввести отрицательное количество товара"):
            cart_page.set_item_quantity(-10)

        with allure.step("Ожидание обновления количества товара"):
            current_quantity = cart_page.get_item_quantity()
            if current_quantity == -10:
                cart_page.wait_for_quantity_update(initial_quantity=-10)
            else:
                logging.info(f"Количество уже обновилось: {current_quantity}")

        with allure.step(
            "Кликнуть на другой элемент для обновления количества"
                ):
            search_page.click_element(search_page.search_button)

        with allure.step("Проверить, что количество товара изменилось на 1"):
            actual_quantity = cart_page.get_item_quantity()
            assert actual_quantity == 1, (
                f"Ожидалось количество 1, но получено {actual_quantity}."
            )
