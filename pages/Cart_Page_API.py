import requests
import logging


class CartPageAPI:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

        logging.info("CartPageAPI инициализирован.")

    def validate_response(self, response):
        """
        Проверяет успешность ответа и валидность JSON.
        """
        try:
            if "application/json" not in response.headers.get(
                    "Content-Type", ""
                    ):
                logging.error(
                    "Ответ сервера не является JSON. Статус: "
                    f"{response.status_code}, "
                    f"Content-Type: {response.headers.get('Content-Type')}"
                )
                raise ValueError("Ответ сервера не содержит JSON.")

            response_body = response.json()
            logging.info(f"Тело ответа: {response_body}")
            return response_body
        except ValueError as e:
            logging.error(
                "Не удалось декодировать JSON из ответа сервера. "
                f"Статус: {response.status_code}, Тело: {response.text}"
            )
            raise ValueError(
                "Ошибка декодирования JSON в ответе сервера."
                ) from e

    def add_product_to_cart(self, product_id):
        """
        Отправляет POST запрос для добавления товара в корзину.
        """
        url = f"{self.base_url}cart/product"
        payload = {
            "id": product_id,
            "adData": {
                "item_list_name": "index",
                "product_shelf": "Новинки литературы"
            }
        }
        logging.info(f"Отправка POST запроса на {url} с телом {payload}")
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code != 200:
            logging.error(
                "Ошибка ответа сервера: "
                f"{response.status_code}, {response.text}"
                )
            raise Exception(f"Сервер вернул ошибку: {response.status_code}")

        if not response.text:  # Проверяем, пустое ли тело
            logging.info("Ответ сервера пустой, возвращаем только статус.")
            return {"status": response.status_code}

        return self.validate_response(response)

    def get_cart_contents(self):
        """
        Отправляет GET запрос для получения списка товаров в корзине.
        """
        url = f"{self.base_url}cart"
        logging.info(
            f"Отправка GET-запроса на {url} для проверки содержимого корзины."
            )
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logging.error(
                "Ошибка ответа сервера: "
                f"{response.status_code}, {response.text}"
                )
            raise Exception(f"Сервер вернул ошибку: {response.status_code}")
        return self.validate_response(response)

    def update_product_quantity(self, product_id, quantity):
        """
        Отправляет PUT запрос для изменения количества товара в корзине.
        """
        url = f"{self.base_url}cart"
        payload = [
            {
                "id": product_id,
                "quantity": quantity
            }
        ]
        logging.info(f"Отправка PUT-запроса на {url} с телом {payload}")
        response = requests.put(url, json=payload, headers=self.headers)

        # Логируем статус ответа и тело
        logging.info(
            "Ответ сервера: статус "
            f"{response.status_code}, тело {response.text}"
            )

        # Обработка ожидаемых статусов
        if response.status_code not in [200, 422]:
            logging.error(
                "Неожиданный статус ответа сервера: "
                f"{response.status_code}, {response.text}"
            )
            raise Exception(
                "Сервер вернул неожиданный статус: "
                f"{response.status_code}"
                )

        # Возвращаем ответ напрямую (или разбираем JSON при необходимости)
        return response

    def delete_product_from_cart(self, product_id):
        """
        Отправляет DELETE запрос для удаления товара из корзины.
        """
        url = f"{self.base_url}cart/product/{product_id}"
        logging.info(f"Отправка DELETE-запроса на {url}")
        response = requests.delete(url, headers=self.headers)
        logging.info(
            "Ответ сервера: статус "
            f"{response.status_code}, тело {response.text}"
        )
        return response

    def restore_product_to_cart(self, product_id):
        """
        Отправляет POST запрос для возврата удалённого товара в корзину.
        """
        url = f"{self.base_url}cart/product-restore"
        payload = {
            "productId": product_id
        }
        logging.info(f"Отправка POST-запроса на {url} с телом {payload}")
        response = requests.post(url, json=payload, headers=self.headers)
        logging.info(
            "Ответ сервера: статус "
            f"{response.status_code}, тело {response.text}"
        )
        return response

    def post_request_without_body(self, endpoint):
        """
        Отправляет POST запрос без тела и возвращает ответ сервера.
        """
        url = f"{self.base_url}{endpoint}"
        logging.info(f"Отправка POST-запроса на {url} без тела")
        response = requests.post(url, headers=self.headers)
        logging.info(
            "Ответ сервера: статус "
            f"{response.status_code}, тело {response.text}"
        )
        return response
