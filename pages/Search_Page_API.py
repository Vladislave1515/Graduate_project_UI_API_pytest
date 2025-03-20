import requests
import logging


class SearchPageAPI:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def search_by_name(self, search_name):
        """
        Выполняет GET запрос для поиска товара по названию.
        """
        url = f"{self.base_url}{search_name}"
        logging.info(f"Отправка GET-запроса на {url}")
        response = requests.get(url, headers=self.headers)
        logging.info(
            "Ответ сервера: статус "
            f"{response.status_code}, тело {response.text}"
        )
        return response

    def search_by_category(self, category_query):
        """
        Выполняет GET-запрос для поиска товаров по категории.
        """
        url = f"{self.base_url}{category_query}"
        logging.info(f"Отправка GET-запроса на {url}")
        response = requests.get(url, headers=self.headers)
        logging.info(
            "Ответ сервера: статус "
            f"{response.status_code}, тело {response.text}"
        )
        return response

    def search_by_author(self, author_query):
        """
        Выполняет GET-запрос для поиска товаров по автору.
        """
        url = f"{self.base_url}{author_query}"
        logging.info(f"Отправка GET-запроса на {url}")
        response = requests.get(url, headers=self.headers)
        logging.info(
            "Ответ сервера: статус "
            f"{response.status_code}, тело {response.text}"
        )
        return response

    def search_by_150_symbols(self, query):
        """
        Выполняет GET-запрос для поиска по длинному запросу (150 символов).
        """
        url = f"{self.base_url}{query}"
        logging.info(f"Отправка GET-запроса на {url}")
        response = requests.get(url, headers=self.headers)
        logging.info(
            "Ответ сервера: статус "
            f"{response.status_code}, тело {response.text}"
        )
        return response

    def post_search_results(self, search_phrase, result_count):
        """
        Отправляет POST-запрос для вывода результатов поиска.
        """
        url = f"{self.base_url}search/results"
        payload = {
            "searchPhrase": search_phrase,
            "resultCount": result_count,
        }
        logging.info(f"Отправка POST-запроса на {url} с телом {payload}")
        response = requests.post(url, json=payload, headers=self.headers)
        logging.info(
            "Ответ сервера: статус "
            f"{response.status_code}, тело {response.text}"
        )
        return response

    def search_with_long_query(self, long_query):
        """
        Выполняет GET-запрос для поиска с длиной строки больше 150 символов.
        """
        url = f"{self.base_url}{long_query}"
        logging.info(f"Отправка GET-запроса на {url}")
        response = requests.get(url, headers=self.headers)
        logging.info(
            "Ответ сервера: статус "
            f"{response.status_code}, тело {response.text}"
        )
        return response
