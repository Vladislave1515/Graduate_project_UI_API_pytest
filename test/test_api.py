import pytest
import allure
import logging
from pages.Cart_Page_API import CartPageAPI
from pages.Search_Page_API import SearchPageAPI


BASE_URL_V1 = "https://web-gate.chitai-gorod.ru/api/v1/"  # Для корзины
BASE_URL_V2 = "https://web-gate.chitai-gorod.ru/api/v2/"  # Для поиска

HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJleHAiOjE3NDI2MjAyNDUsImlhdCI6MTc0MjQ1MjI0NSwiaXNzIjoiL2F"
    "waS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6IjYyNzVmOTJlYWY4YWUwY2U"
    "xYzNhNTRmOGJiZjllNmFhNDdkNGUxMjlhOWVkZTRlMjEyMmFjYWViMzFlZGN"
    "jZWIiLCJ0eXBlIjoxMH0.di7ylDel5uWjV7NzWPP-D2IahXxaXhD6mtyzv8E"
    "0eK4"
    }  # Временный токен
PRODUCT_ID = 3067555  # ID_prod
ID_prod_put_del_post = 194843212
SEARCH_NAME = (
    "search/product?customerCityId=2&phrase=%D0%93%D0%B0%D1%80%D1%80%D0%B8%20"
    "%D0%9F%D0%BE%D1%82%D1%82%D0%B5%D1%80%20%D0%B8%20%D0%BA%D1%83%D0%B1%D0%BE"
    "%D0%BA%20%D0%BE%D0%B3%D0%BD%D1%8F&products%5Bpage%5D=1&products%5Bper-"
    "page%5D=48&sortPreset=relevance"
)
SEARCH_CATEGORY = (
    "search/product?filters%5Bcategories%5D=110090&customerCityId=2&phrase="
    "%D0%B3%D0%B0%D1%80%D1%80%D0%B8%20%D0%BF%D0%BE%D1%82%D1%82%D0%B5%D1%80%20"
    "%D0%B8%20%D0%BA%D1%83%D0%B1%D0%BE%D0%BA%20%D0%BE%D0%B3%D0%BD%D1%8F&"
    "products%5Bpage%5D=1&products%5Bper-page%5D=48&sortPreset=relevance"
)
SEARCH_AVTOR = (
    "search/product?filters%5Bauthors%5D=604355&customerCityId=2&phrase="
    "%D1%80%D0%BE%D1%83%D0%BB%D0%B8%D0%BD%D0%B3%20%D0%B4%D0%B6%D0%BE%D0%B0%D0"
    "%BD%20%D0%BA%D1%8D%D1%82%D0%BB%D0%B8%D0%BD&products%5Bpage%5D=1&products"
    "%5Bper-page%5D=48&sortPreset=relevance"
)
REPEATED_PART = (
    "%D0%B3%D0%B0%D1%80%D1%80%D0%B8%20%D0%BF%D0%BE%D1%82%D1%82%D0%B5%D1%80%20"
    )

SEARCH_150_SYMBOL = (
    "search/product?customerCityId=2&phrase="
    + (REPEATED_PART * 9)  # Повторяем 9 раз
    + "%D0%B8%20%D0%BA%D1%83%D0%B1%D0%BE%D0%BA"  # Добавляем конец строки
)
SEARCH_MORE150_SYMBOL = (
    "search/product?customerCityId=2&phrase="
    + (REPEATED_PART * 10)
    + "%D0%B8%20%D0%BA%D1%83%D0%B1%D0%BE%D0%BA"
)


class TestCart:
    @allure.feature('Корзина')
    @allure.story('Добавление товара в корзину')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Позитивный тест: добавление товара в корзину")
    @allure.description(
        "Тест проверяет, что POST запрос на добавление "
        "товара в корзину выполняется успешно."
    )
    @pytest.mark.api
    def test_add_product_to_cart(self):
        api = CartPageAPI(BASE_URL_V1, HEADERS)

        with allure.step("Отправить POST запрос для добавления товара"):
            response = api.add_product_to_cart(PRODUCT_ID)

        with allure.step("Проверить, что статус ответа равен 200"):
            assert response["status"] == 200, (
                f"Ожидался статус 200, но получен {response['status']}."
            )

        with allure.step("Проверить, что тело ответа пустое"):
            if "id" not in response:
                logging.info(
                    "Ответ сервера пустой, проверка завершена успешно."
                    )

    @allure.feature('Корзина')
    @allure.story('Просмотр списка добавленных товаров в корзину')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Просмотр содержимого корзины")
    @allure.description(
        "Тест проверяет, что GET запрос на получение содержимого корзины "
        "выполняется успешно и возвращает корректные данные."
    )
    @pytest.mark.api
    def test_view_cart_contents(self):
        api = CartPageAPI(BASE_URL_V1, HEADERS)

        with allure.step("Отправить GET запрос для получения списка товаров"):
            response_body = api.get_cart_contents()

        with allure.step("Проверить, что тело ответа содержит список товаров"):
            assert response_body is not None, "Ответ сервера пустой."
            assert "products" in response_body, "'products' отсутствует."
            assert isinstance(response_body["products"], list), (
                "Ожидался список товаров, но получено: "
                f"{type(response_body['products'])}."
            )

    @allure.feature('Корзина')
    @allure.story('Увеличение добавленного товара в корзине')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Изменение количества товара в корзине")
    @allure.description(
        "Тест проверяет, что PUT запрос для увеличения количества товара "
        "выполняется успешно и данные корзины обновляются."
    )
    @pytest.mark.api
    def test_update_product_quantity(self):
        api = CartPageAPI(BASE_URL_V1, HEADERS)

        with allure.step(
            "Отправить PUT запрос для увеличения количества товара"
                ):
            response = api.update_product_quantity(ID_prod_put_del_post, 2)

        with allure.step("Проверить, что количество товара обновлено"):
            try:
                # Логирование тела ответа для отладки
                logging.info(f"Тело ответа сервера: {response.text}")

                # Преобразуем тело ответа в JSON
                response_body = response.json()

                # Проверяем, что ответ не пустой
                assert response_body is not None, "Ответ сервера пустой."

                # Проверяем наличие ключа 'products'
                assert "products" in response_body, "'products' отсутствует."

                # Проверяем, что товар с нужным ID обновлён
                products = response_body["products"]
                assert any(
                    product["id"] == ID_prod_put_del_post and product[
                        "quantity"
                        ] == 2
                    for product in products
                ), "Товар с id "
                f"{ID_prod_put_del_post} не найден или не обновлено."
            except ValueError as e:
                assert False, (
                    f"Ошибка обработки JSON из ответа сервера: {e}. "
                    f"Тело ответа: {response.text}"
                )

    @allure.feature('Корзина')
    @allure.story('Удаление товара из корзины')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление товара из корзины")
    @allure.description(
        "Тест проверяет, что DELETE запрос успешно удаляет товар из корзины."
    )
    @pytest.mark.api
    def test_delete_product_from_cart(self):
        api = CartPageAPI(BASE_URL_V1, HEADERS)

        with allure.step("Отправить DELETE запрос для удаления товара"):
            response = api.delete_product_from_cart(ID_prod_put_del_post)

        with allure.step("Проверить, что статус ответа равен 204"):
            # Проверяем статус ответа напрямую у объекта Response
            assert response.status_code == 204, (
                f"Ожидался статус 204, но получен {response.status_code}."
            )

        # Дополнительно проверим, что товар больше не в корзине
        with allure.step("Проверить, что товар был удалён из корзины"):
            get_response = api.get_cart_contents()
            assert "products" in get_response, "'products' отсутствует."
            products = get_response["products"]
            assert all(
                product["id"] != ID_prod_put_del_post for product in products
            ), f"Товар с ID {ID_prod_put_del_post} все еще "
            "находится в корзине."

    @allure.feature('Корзина')
    @allure.story('Возврат удалённого товара в корзину')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Возврат удалённого товара в корзину")
    @allure.description(
        "Тест проверяет, что POST запрос успешно "
        "возвращает удалённый товар в корзину."
    )
    @pytest.mark.api
    def test_restore_product_to_cart(self):
        api = CartPageAPI(BASE_URL_V1, HEADERS)

        with allure.step("Отправить POST запрос для восстановления товара"):
            response = api.restore_product_to_cart(ID_prod_put_del_post)

        with allure.step("Проверить, что статус ответа равен 200"):
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}."
            )

        with allure.step("Проверить, что товар был успешно восстановлен"):
            response_body = response.json()
            assert "products" in response_body, "'products' отсутствует."
            products = response_body["products"]
            assert any(
                product["id"] == ID_prod_put_del_post for product in products
            ), f"Товар с ID {ID_prod_put_del_post} не был "
            "восстановлен в корзину."

    @allure.feature('Корзина')
    @allure.story('Увеличение количества товара выше допустимого')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title(
        "Негативный тест: Увеличение количества товара выше допустимого"
        )
    @allure.description(
        "Тест проверяет, что система не позволяет увеличить количество товара "
        "выше допустимого значения и возвращает статус код 422."
    )
    @pytest.mark.api
    def test_increase_product_quantity_above_limit(self):
        api = CartPageAPI(BASE_URL_V1, HEADERS)

        with allure.step(
            "Отправить PUT запрос для увеличения количества товара"
                ):
            response = api.update_product_quantity(ID_prod_put_del_post, 2000)

        with allure.step("Проверить, что статус ответа равен 422"):
            assert response.status_code == 422, (
                f"Ожидался статус 422, но получен {response.status_code}."
            )

        with allure.step(
            "Проверить, что тело ответа содержит сообщение об ошибке"
                ):
            try:
                response_body = response.json()
                assert "message" in response_body, "'message' отсутствует."
                assert response_body["message"] == "422 - error", (
                    "Ожидалось сообщение '422 - error', но получено "
                    f"{response_body.get('message')}."
                )
            except ValueError:
                assert False, (
                    f"Не удалось декодировать JSON из ответа сервера. "
                    f"Тело: {response.text}"
                )

    @allure.feature('Корзина')
    @allure.story('Изменение количества товара на отрицательное значение')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title(
        "Негативный тест: Изменение количества "
        "товара на отрицательное значение"
        )
    @allure.description(
        "Тест проверяет, что система не позволяет установить отрицательное "
        "количество товара в корзине и возвращает статус код 422."
    )
    @pytest.mark.api
    def test_set_negative_quantity_in_cart(self):
        api = CartPageAPI(BASE_URL_V1, HEADERS)

        with allure.step(
            "Отправить PUT запрос для установки "
            "отрицательного количества товара"
                ):
            response = api.update_product_quantity(ID_prod_put_del_post, -1)

        with allure.step("Проверить, что статус ответа равен 422"):
            assert response.status_code == 422, (
                f"Ожидался статус 422, но получен {response.status_code}."
            )

        with allure.step(
            "Проверить, что тело ответа содержит сообщение об ошибке"
                ):
            try:
                response_body = response.json()
                assert "message" in response_body, "'message' отсутствует."
                assert response_body["message"] == "422 - error", (
                    "Ожидалось сообщение '422 - error', но получено "
                    f"{response_body.get('message')}."
                )
            except ValueError:
                assert False, (
                    f"Ошибка обработки JSON из ответа сервера. "
                    f"Тело ответа: {response.text}"
                )

    @allure.feature('Корзина')
    @allure.story('Запрос без тела')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Негативный тест: Запрос без тела")
    @allure.description(
        "Тест проверяет, что API не позволяет выполнить POST запрос без тела "
        "и возвращает статус код 404 с сообщением об ошибке."
    )
    @pytest.mark.api
    def test_post_request_without_body(self):
        api = CartPageAPI(BASE_URL_V1, HEADERS)

        with allure.step("Отправить POST запрос без тела"):
            response = api.post_request_without_body("cart/product-restore")

        with allure.step("Проверить, что статус ответа равен 404"):
            assert response.status_code == 404, (
                f"Ожидался статус 404, но получен {response.status_code}."
            )

        with allure.step(
            "Проверить, что тело ответа содержит сообщение об ошибке"
                ):
            try:
                response_body = response.json()
                assert "message" in response_body, "'message' отсутствует."
                assert response_body["message"] == "404 - error", (
                    "Ожидалось сообщение '404 - error', но получено "
                    f"{response_body.get('message')}."
                )
            except ValueError:
                assert False, (
                    f"Ошибка обработки JSON из ответа сервера. "
                    f"Тело ответа: {response.text}"
                )


class TestSearch:
    @allure.feature('Поиск')
    @allure.story('Валидный поиск товара по названию')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест валидного поиска товара")
    @allure.description(
        "Тест проверяет, что API возвращает валидный и релевантный результат "
        "при поиске товара по названию."
    )
    @pytest.mark.api
    def test_valid_product_search_by_name(self):
        api = SearchPageAPI(BASE_URL_V2, HEADERS)

        with allure.step("Отправить GET запрос для поиска товара"):
            response = api.search_by_name(SEARCH_NAME)

        with allure.step("Проверить, что статус ответа равен 200"):
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}."
            )

        with allure.step("Проверить, что ответ содержит валидные данные"):
            try:
                response_body = response.json()
                assert "data" in response_body, "'data' отсутствует."
                assert "attributes" in response_body["data"], (
                    "Ключ 'attributes' отсутствует в разделе 'data'."
                )
                assert response_body[
                    "data"]["attributes"]["transformedPhrase"] == (
                        "гарри поттер и кубок огня"
                        ), "Фраза поиска не совпадает с ожидаемой."
                assert "relationships" in response_body["data"], (
                    "Ключ 'relationships' отсутствует в разделе 'data'."
                )
                products = response_body[
                    "data"]["relationships"]["products"]["data"]
                assert any(
                    product["id"] == "2441276" for product in products
                ), "Искомый продукт не найден в результатах поиска."
            except ValueError as e:
                assert False, (
                    f"Ошибка обработки JSON из ответа сервера: {e}. "
                    f"Тело ответа: {response.text}"
                )

    @allure.feature('Поиск')
    @allure.story('Валидный поиск товара по категории')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест валидного поиска по категории")
    @allure.description(
        "Тест проверяет, что API возвращает валидный и релевантный результат "
        "при поиске товара по категории."
    )
    @pytest.mark.api
    def test_valid_product_search_by_category(self):
        api = SearchPageAPI(BASE_URL_V2, HEADERS)  # Используем URL_v2

        with allure.step(
            "Отправить GET-запрос для поиска товара по категории"
                ):
            response = api.search_by_category(SEARCH_CATEGORY)

        with allure.step("Проверить, что статус ответа равен 200"):
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}."
            )

        with allure.step("Проверить, что ответ содержит валидные данные"):
            try:
                response_body = response.json()
                assert "data" in response_body, "'data' отсутствует."
                assert "attributes" in response_body["data"], (
                    "Ключ 'attributes' отсутствует в разделе 'data'."
                )
                assert response_body[
                    "data"]["attributes"]["transformedPhrase"] == (
                    "гарри поттер и кубок огня"
                ), "Фраза поиска не совпадает с ожидаемой."
                assert "relationships" in response_body["data"], (
                    "Ключ 'relationships' отсутствует в разделе 'data'."
                )
                products = response_body[
                    "data"]["relationships"]["products"]["data"]
                assert any(
                    product["id"] == "2441276" for product in products
                ), "Искомый продукт не найден в результатах поиска."
            except ValueError as e:
                assert False, (
                    f"Ошибка обработки JSON из ответа сервера: {e}. "
                    f"Тело ответа: {response.text}"
                )

    @allure.feature('Поиск')
    @allure.story('Валидный поиск товара по автору книги')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест валидного поиска по автору")
    @allure.description(
        "Тест проверяет, что API возвращает валидный и релевантный результат "
        "при поиске товара по автору книги."
    )
    @pytest.mark.api
    def test_api_search_by_author(self):
        api = SearchPageAPI(BASE_URL_V2, HEADERS)  # Используем URL_v2

        with allure.step("Отправить GET-запрос для поиска товара по автору"):
            response = api.search_by_author(SEARCH_AVTOR)

        with allure.step("Проверить, что статус ответа равен 200"):
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}."
            )

        with allure.step("Проверить, что ответ содержит валидные данные"):
            try:
                response_body = response.json()
                assert "data" in response_body, "'data' отсутствует."
                assert "attributes" in response_body["data"], (
                    "Ключ 'attributes' отсутствует в разделе 'data'."
                )
                assert response_body[
                    "data"]["attributes"]["transformedPhrase"] == (
                        "роулинг джоан кэтлин"
                        ), "Фраза поиска не совпадает с ожидаемой."
                assert "relationships" in response_body["data"], (
                    "Ключ 'relationships' отсутствует в разделе 'data'."
                )
                products = response_body[
                    "data"]["relationships"]["products"]["data"]
                assert any(
                    product["id"] == "2405917" for product in products
                ), "Искомый продукт не найден в результатах поиска."
            except ValueError as e:
                assert False, (
                    f"Ошибка обработки JSON из ответа сервера: {e}. "
                    f"Тело ответа: {response.text}"
                )

    @allure.feature('Поиск')
    @allure.story('Поиск по строке длиной 150 символов')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест поиска по строке длиной 150 символов")
    @allure.description(
        "Тест проверяет, что API корректно обрабатывает "
        "запрос длиной 150 символов и возвращает валидные результаты."
    )
    @pytest.mark.api
    def test_search_by_150_symbols(self):
        api = SearchPageAPI(BASE_URL_V2, HEADERS)  # Используем URL_v2

        with allure.step(
            "Отправить GET-запрос для поиска товара по длинной строке"
                ):
            response = api.search_by_150_symbols(SEARCH_150_SYMBOL)

        with allure.step("Проверить, что статус ответа равен 200"):
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}."
            )

        with allure.step("Проверить, что ответ содержит валидные данные"):
            try:
                response_body = response.json()
                assert "data" in response_body, "'data' отсутствует."
                assert "attributes" in response_body["data"], (
                    "Ключ 'attributes' отсутствует в разделе 'data'."
                )
                assert response_body[
                    "data"]["attributes"]["transformedPhrase"] == (
                        "гарри поттер гарри поттер гарри поттер гарри "
                        "поттер гарри поттер гарри поттер гарри поттер "
                        "гарри поттер гарри поттер и кубок"
                        ), "Фраза поиска не совпадает с ожидаемой."
                assert "relationships" in response_body["data"], (
                    "Ключ 'relationships' отсутствует в разделе 'data'."
                )
                products = response_body[
                    "data"]["relationships"]["products"]["data"]
                assert any(
                    product["id"] == "2441276" for product in products
                ), "Искомый продукт не найден в результатах поиска."
            except ValueError as e:
                assert False, (
                    f"Ошибка обработки JSON из ответа сервера: {e}. "
                    f"Тело ответа: {response.text}"
                )

    @allure.feature('Поиск')
    @allure.story('Вывод результатов поиска')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест вывода результатов поиска")
    @allure.description(
        "Тест проверяет, что POST запрос для вывода результатов поиска "
        "возвращает корректный статус 204."
    )
    @pytest.mark.api
    def test_search_results_output(self):
        api = SearchPageAPI(BASE_URL_V2, HEADERS)  # Используем URL_v2

        with allure.step(
            "Отправить POST-запрос для вывода результатов поиска"
                ):
            response = api.post_search_results("гарри поттер", 21)

        with allure.step("Проверить, что статус ответа равен 204"):
            assert response.status_code == 204, (
                f"Ожидался статус 204, но получен {response.status_code}."
            )

    @allure.feature('Поиск')
    @allure.story('Поиск с длиной строки больше 150 символов')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест поиска с длиной строки больше 150 символов")
    @allure.description(
        "Тест проверяет, что система не принимает "
        "строку длиной больше 150 символов и возвращает "
        "соответствующую ошибку 422."
    )
    @pytest.mark.api
    def test_search_long_query(self):
        api = SearchPageAPI(BASE_URL_V2, HEADERS)  # Используем URL_v2

        with allure.step(
            "Отправить GET-запрос для поиска с длиной строки > 150 символов"
                ):
            response = api.search_with_long_query(SEARCH_MORE150_SYMBOL)

        with allure.step("Проверить, что статус ответа равен 422"):
            assert response.status_code == 422, (
                f"Ожидался статус 422, но получен {response.status_code}."
            )

        with allure.step("Проверить, что ответ содержит сообщение об ошибке"):
            try:
                response_body = response.json()
                assert "errors" in response_body, "'errors' отсутствует."
                error = response_body["errors"][0]
                assert error["status"] == "422", "Статус ошибки не равен 422."
                assert error["title"] == (
                    "Значение слишком длинное. "
                    "Должно быть равно 125 символам или меньше."
                ), "Сообщение ошибки не соответствует ожидаемому."
            except ValueError as e:
                assert False, (
                    f"Ошибка обработки JSON из ответа сервера: {e}. "
                    f"Тело ответа: {response.text}"
                )
