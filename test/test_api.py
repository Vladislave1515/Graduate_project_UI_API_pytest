import pytest
import allure
import logging
from config import BASE_URLS, HEADERS, PRODUCT_IDS, SEARCH_QUERIES


BASE_URL_V1 = BASE_URLS["cart"]
BASE_URL_V2 = BASE_URLS["search"]
HEADERS = HEADERS
PRODUCT_ID = PRODUCT_IDS["default_product"]
ID_prod_put_del_post = PRODUCT_IDS["cart_product"]
SEARCH_NAME = SEARCH_QUERIES["name"]
SEARCH_CATEGORY = SEARCH_QUERIES["category"]
SEARCH_AVTOR = SEARCH_QUERIES["author"]
SEARCH_MORE150_SYMBOL = SEARCH_QUERIES["query_more_150"]
SEARCH_150_SYMBOL = SEARCH_QUERIES["query_150"]


class TestCart:
    @allure.feature('Корзина')
    @allure.story('Добавление товара в корзину')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Добавление товара в корзину")
    @allure.description(
        "Тест проверяет, что POST запрос на добавление "
        "товара в корзину выполняется успешно."
    )
    @pytest.mark.api
    def test_add_product_to_cart(self, cart_api):

        with allure.step("Отправить POST запрос для добавления товара"):
            response = cart_api.add_product_to_cart(PRODUCT_ID)

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
    def test_view_cart_contents(self, cart_api):

        with allure.step("Отправить GET запрос для получения списка товаров"):
            response_body = cart_api.get_cart_contents()

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
    def test_update_product_quantity(self, cart_api):

        with allure.step(
            "Отправить PUT запрос для увеличения количества товара"
                ):
            response = cart_api.update_product_quantity(
                ID_prod_put_del_post, 2
                )

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
    def test_delete_product_from_cart(self, cart_api):

        with allure.step("Отправить DELETE запрос для удаления товара"):
            response = cart_api.delete_product_from_cart(ID_prod_put_del_post)

        with allure.step("Проверить, что статус ответа равен 204"):
            # Проверяем статус ответа напрямую у объекта Response
            assert response.status_code == 204, (
                f"Ожидался статус 204, но получен {response.status_code}."
            )

        # Дополнительно проверим, что товар больше не в корзине
        with allure.step("Проверить, что товар был удалён из корзины"):
            get_response = cart_api.get_cart_contents()
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
    def test_restore_product_to_cart(self, cart_api):

        with allure.step("Отправить POST запрос для восстановления товара"):
            response = cart_api.restore_product_to_cart(ID_prod_put_del_post)

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
    @allure.story(
        'Негативный тест: Увеличение количества товара выше допустимого'
        )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Увеличение количества товара выше допустимого")
    @allure.description(
        "Тест проверяет, что система не позволяет увеличить количество товара "
        "выше допустимого значения и возвращает статус код 422."
    )
    @pytest.mark.api
    def test_increase_product_quantity_above_limit(self, cart_api):

        with allure.step(
            "Отправить PUT запрос для увеличения количества товара"
                ):
            response = cart_api.update_product_quantity(
                ID_prod_put_del_post, 2000
                )

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
    @allure.story(
        'Негативный тест: Изменение количества товара '
        'на отрицательное значение'
        )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Изменение количества товара на отрицательное значение")
    @allure.description(
        "Тест проверяет, что система не позволяет установить отрицательное "
        "количество товара в корзине и возвращает статус код 422."
    )
    @pytest.mark.api
    def test_set_negative_quantity_in_cart(self, cart_api):

        with allure.step(
            "Отправить PUT запрос для установки "
            "отрицательного количества товара"
                ):
            response = cart_api.update_product_quantity(
                ID_prod_put_del_post, -1
                )

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
    @allure.story('Негативный тест: Запрос без тела')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Запрос без тела")
    @allure.description(
        "Тест проверяет, что API не позволяет выполнить POST запрос без тела "
        "и возвращает статус код 404 с сообщением об ошибке."
    )
    @pytest.mark.api
    def test_post_request_without_body(self, cart_api):

        with allure.step("Отправить POST запрос без тела"):
            response = cart_api.post_request_without_body(
                "cart/product-restore"
                )

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
    @pytest.mark.parametrize(
        "query_type, search_query, expected_phrase, expected_product_id",
        [
            ("Название", SEARCH_QUERIES["name"],
             "гарри поттер и кубок огня", "2441276"),
            ("Категория", SEARCH_QUERIES["category"],
             "гарри поттер и кубок огня", "2441276"),
            ("Автор", SEARCH_QUERIES["author"],
             "роулинг джоан кэтлин", "2405917"),
        ]
    )
    @allure.title("Тест валидного поиска товара по {query_type}")
    @allure.description(
        "Тест проверяет, что API возвращает валидный и релевантный результат "
        "при выполнении различных запросов поиска."
    )
    @pytest.mark.api
    def test_valid_search_api(
        self, query_type, search_query,
        expected_phrase, expected_product_id, search_api
            ):

        with allure.step(
            f"Отправить GET-запрос для поиска товара ({query_type})"
                ):
            response = search_api.search_with_query(search_query)

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
                    "data"]["attributes"][
                        "transformedPhrase"] == expected_phrase, (
                            "Фраза поиска не совпадает с ожидаемой: "
                            f"{expected_phrase}."
                            )
                assert "relationships" in response_body["data"], (
                    "Ключ 'relationships' отсутствует в разделе 'data'."
                )
                products = response_body[
                    "data"]["relationships"]["products"]["data"]
                assert any(
                    product[
                        "id"] == expected_product_id for product in products
                ), f"Искомый продукт с ID {expected_product_id} не найден."
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
    def test_search_by_150_symbols(self, search_api):

        with allure.step(
            "Отправить GET-запрос для поиска товара по длинной строке"
                ):
            response = search_api.search_by_150_symbols(SEARCH_150_SYMBOL)

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
    def test_search_results_output(self, search_api):

        with allure.step(
            "Отправить POST-запрос для вывода результатов поиска"
                ):
            response = search_api.post_search_results("гарри поттер", 21)

        with allure.step("Проверить, что статус ответа равен 204"):
            assert response.status_code == 204, (
                f"Ожидался статус 204, но получен {response.status_code}."
            )

    @allure.feature('Поиск')
    @allure.story('Негативный тест: Поиск с длиной строки больше 150 символов')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Тест поиска с длиной строки больше 150 символов")
    @allure.description(
        "Тест проверяет, что система не принимает "
        "строку длиной больше 150 символов и возвращает "
        "соответствующую ошибку 422."
    )
    @pytest.mark.api
    def test_search_long_query(self, search_api):

        with allure.step(
            "Отправить GET-запрос для поиска с длиной строки > 150 символов"
                ):
            response = search_api.search_with_long_query(SEARCH_MORE150_SYMBOL)

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

    @allure.feature('Поиск')
    @allure.story('Негативный тест: Вывод результатов поиска без авторизации')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Тест вывода результатов поиска без авторизации")
    @allure.description(
        "Тест проверяет, что POST запрос для вывода результатов поиска "
        "без токена авторизации возвращает корректный статус 401 Unauthorized."
    )
    @pytest.mark.api
    def test_search_without_authorization(self, search_api_no_auth):

        with allure.step(
            "Отправить POST-запрос для вывода результатов поиска"
                ):
            response = search_api_no_auth.post_search_results(
                "гарри поттер", 21
                )

        with allure.step(
            "Проверить, что статус ответа равен 401 Unauthorized"
                ):
            assert response.status_code == 401, (
                "Ожидался статус 401 Unauthorized, но получен "
                f"{response.status_code}."
            )

        with allure.step("Проверить, что ответ содержит сообщение об ошибке"):
            response_body = response.json()
            assert "message" in response_body, "'message' отсутствует "
            "в ответе сервера."
            assert response_body[
                "message"] == "Authorization обязательное поле", (
                "Ожидалось сообщение 'Authorization поле', но получено: "
                f"{response_body.get('message')}."
            )
