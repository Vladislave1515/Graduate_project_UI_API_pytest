# config.py

BASE_URL = "https://www.chitai-gorod.ru"
IMPLICIT_WAIT = 4

BASE_URLS = {
    "cart": "https://web-gate.chitai-gorod.ru/api/v1/",
    "search": "https://web-gate.chitai-gorod.ru/api/v2/"
}

HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ"
    "9.eyJleHAiOjE3NDI3OTM1NzEsImlhdCI6MTc0MjYyNTU3MSwiaXNzIjoiL"
    "2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6IjIzZjFlZTUwYzM2ZWVh"
    "NmNkYjE5Njg5NTJiODA1YzA3NDlhNzMxNjExZjkwODEwYzBhZThhMDRiNTg"
    "yMzNmMWYiLCJ0eXBlIjoxMH0.sa6xGJpsre0ZsfSvod74sYQXAqjjhOQm4EhvtiD8pG4"
}

PRODUCT_IDS = {
    "default_product": 3067555,
    "cart_product": 195147409
}

SEARCH_QUERIES = {
    "name": "search/product?customerCityId=2&phrase=Гарри Поттер и Кубок Огня&"
    "products[page]=1&products[per-page]=48&sortPreset=relevance",
    "category": "search/product?filters[categories]=110090&customerCityId=2&"
    "phrase=Гарри Поттер и Кубок Огня&products[page]=1&products[per-page]=48&"
    "sortPreset=relevance",
    "author": "search/product?filters[authors]=604355&customerCityId=2&"
    "phrase=Роулинг Джоан Кэтлин&products[page]=1&products[per-page]=48&"
    "sortPreset=relevance",
    "query_more_150": "search/product?customerCityId=2&phrase=" + (
        "Гарри Поттер " * 10
        ) + "и Кубок",
    "query_150": "search/product?customerCityId=2&phrase=" + (
        "Гарри Поттер " * 9
        ) + "и Кубок"
}
