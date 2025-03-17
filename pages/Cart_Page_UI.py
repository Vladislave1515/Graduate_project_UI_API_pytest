import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from pages.Search_Page_UI import wait_for_element


def wait_for_element_to_disappear(driver, locator, timeout=8):
    """
    Ждёт, пока указанный элемент исчезнет с DOM-дерева.
    """
    logging.info(f"Ожидание исчезновения элемента: {locator}")
    WebDriverWait(driver, timeout).until_not(
        EC.presence_of_element_located(locator)
    )


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.buy_button = (
            By.CSS_SELECTOR,
            ".product-buttons__main-action.product-buttons__main-action > div"
        )
        self.cart_item_count = (
            By.CSS_SELECTOR,
            ".sticky-header__controls > span > span."
            "badge-notice.header-cart__badge"
        )
        self.cart_icon = (
            By.CSS_SELECTOR,
            ".header-controls.header__controls > button:nth-child(4)"
        )
        self.remove_button = (
            By.CSS_SELECTOR,
            ".cart-item__actions-button--delete.light-blue > svg"
        )
        self.notification_text = (
            By.CSS_SELECTOR,
            ".item-removed__description > div.item-removed__description-title"
        )
        self.return_button = (
            By.CSS_SELECTOR,
            ".item-removed__actions-button.light-blue"
        )
        self.quantity_input = (
            By.CSS_SELECTOR,
            ".product-quantity.cart-item__quantity-control > input"
        )  # Поле ввода количества
        self.total_price_locator = (
            By.CSS_SELECTOR,
            ".product-price__value--discount"
        )  # Локатор для итоговой цены
        self.item_price_locator = (
            By.CSS_SELECTOR,
            ".cart-item__counter > div > div.cart-item__counter-unit"
        )  # Локатор для цены одного товара
        self.quantity_plus_button = (
            By.CSS_SELECTOR,
            ".product-quantity__button.product-quantity__button--right"
        )

        logging.info("CartPage инициализирован.")

    def click_buy_button(self):
        """
        Клик по кнопке 'КУПИТЬ', даже если она заблокирована.
        """
        logging.info("Попытка найти кнопку 'КУПИТЬ' для взаимодействия.")
        try:
            # Ждать, пока кнопка станет кликабельной
            buy_button = wait_for_element(
                self.driver, self.buy_button,
                EC.element_to_be_clickable
            )
            logging.info(
                "Кнопка 'КУПИТЬ' найдена и готова для взаимодействия.")

            # Прокрутить страницу до кнопки
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", buy_button
            )
            logging.info("Кнопка 'КУПИТЬ' прокручена в видимую область.")

            # Выполнить клик через JavaScript
            self.driver.execute_script(
                "arguments[0].click();", buy_button
            )
            logging.info("Кнопка 'КУПИТЬ' успешно нажата через JavaScript.")
        except exceptions.ElementClickInterceptedException:
            logging.warning(
                "Кнопка 'КУПИТЬ' перекрыта другим элементом."
            )
            blocker_locator = (By.CSS_SELECTOR, ".popmechanic-main")
            wait_for_element_to_disappear(self.driver, blocker_locator)
            logging.info("Блокирующий элемент исчез. Повторяем попытку.")

            # Повторить клик
            self.driver.execute_script("arguments[0].click();", buy_button)
            logging.info("Кнопка 'КУПИТЬ' успешно нажата.")
        except Exception as e:
            logging.error(
                f"Произошла ошибка при клике по кнопке 'КУПИТЬ': {str(e)}")
            raise

    def open_cart(self):
        """
        Открыть корзину, нажав на иконку корзины.
        """
        logging.info("Попытка открыть корзину.")
        wait_for_element(
            self.driver, self.cart_icon,
            EC.element_to_be_clickable
        ).click()
        logging.info("Корзина успешно открыта.")

        # Ожидание загрузки корзины
        self.wait_for_cart_to_load()

    def remove_item_from_cart(self):
        """
        Удалить товар из корзины, нажав на кнопку удаления.
        """
        logging.info("Попытка удалить товар из корзины.")
        try:
            wait_for_element(
                self.driver, self.remove_button,
                EC.element_to_be_clickable
            ).click()
            logging.info("Товар успешно удалён из корзины.")
        except exceptions.TimeoutException:
            logging.error("Кнопка удаления недоступна.")
            raise

    def click_return_to_cart_button(self):
        """
        Клик по кнопке 'ВЕРНУТЬ В КОРЗИНУ'.
        """
        logging.info("Попытка кликнуть по кнопке 'ВЕРНУТЬ В КОРЗИНУ'.")
        try:
            wait_for_element(
                self.driver, self.return_button,
                EC.element_to_be_clickable
            ).click()
            logging.info("Кнопка 'ВЕРНУТЬ В КОРЗИНУ' успешно нажата.")
        except exceptions.TimeoutException:
            logging.error("Кнопка 'ВЕРНУТЬ В КОРЗИНУ' недоступна.")
            raise

    def get_cart_item_count(self):
        """
        Получает количество товаров в корзине.
        """
        logging.info("Получение количества товаров в корзине.")
        try:
            cart_count = wait_for_element(
                self.driver, self.cart_item_count,
                EC.presence_of_element_located
            )
            count = int(cart_count.text.strip())
            logging.info(f"Количество товаров в корзине: {count}.")
            return count
        except ValueError:
            logging.error(
                f"Ошибка: значение '{cart_count.text}' не может быть \n"
                "преобразовано."
            )
            return 0
        except exceptions.TimeoutException:
            logging.warning(
                "Не удалось получить количество товаров в корзине."
            )
            return 0

    def get_notification_message(self):
        """
        Получить текст уведомления об удалении товара из корзины.
        """
        logging.info("Получение сообщения об удалении товара из корзины.")
        try:
            notification = wait_for_element(
                self.driver, self.notification_text,
                EC.presence_of_element_located
            )
            logging.info(f"Сообщение получено: {notification.text.strip()}.")
            return notification.text.strip()
        except exceptions.TimeoutException:
            logging.error("Сообщение об удалении товара не найдено.")
            return ""

    def cart_update(self):
        """
        Ожидание обновления корзины после удаления товара.
        """
        logging.info("Ожидание обновления корзины после удаления товара.")
        try:
            # Получаем текущее количество товаров в корзине
            initial_count = self.get_cart_item_count()
            logging.info(
                f"Текущее количество товаров в корзине: {initial_count}")

            # Ждём, пока количество товаров уменьшится
            WebDriverWait(self.driver, 7).until(
                lambda driver: self.get_cart_item_count() < initial_count,
                "Корзина не обновилась: товар не был удалён."
            )
            logging.info("Корзина успешно обновилась после удаления товара.")
        except exceptions.TimeoutException:
            logging.error("Корзина не обновилась в течение заданного времени.")
            raise

    def set_item_quantity(self, quantity):
        """
        Устанавливает количество товара в корзине через ручной ввод.
        """
        logging.info(f"Установка количества товара: {quantity}")
        try:
            # Найти поле ввода количества
            quantity_input = wait_for_element(
                self.driver, self.quantity_input,
                EC.element_to_be_clickable
            )
            quantity_input.click()  # Кликаем на поле, чтобы активировать его
            logging.info("Поле ввода количества активировано.")

            # Выделить существующее значение и удалить его
            quantity_input.send_keys(Keys.CONTROL + "a")
            quantity_input.send_keys(Keys.BACKSPACE)
            logging.info("Существующее значение поля ввода удалено.")

            # Ввести новое значение
            quantity_input.send_keys(str(quantity))
            logging.info(f"Введено новое количество: {quantity}")

            # Подтвердить изменение (если требуется)
            quantity_input.send_keys(Keys.ENTER)
            logging.info("Изменение количества подтверждено.")
        except exceptions.TimeoutException:
            logging.error("Поле ввода количества недоступно.")
            raise

    def get_item_quantity(self):
        """
        Получает текущее количество товара в корзине.
        """
        logging.info("Получение текущего количества товара в корзине.")
        try:
            quantity_input = wait_for_element(
                self.driver, self.quantity_input,
                EC.presence_of_element_located,
            )
            return int(quantity_input.get_attribute("value"))
        except exceptions.TimeoutException:
            logging.error("Не удалось получить количество товара.")
            raise

    def get_item_price(self):
        """
        Получает цену одного товара в корзине.
        """
        logging.info("Получение цены одного товара в корзине.")
        try:
            # Дождаться элемента с ценой
            item_price_element = wait_for_element(
                self.driver, self.item_price_locator,
                EC.presence_of_element_located
            )
            # Очистить текст от лишних символов и преобразовать в float
            cleaned_price = item_price_element.text.replace(
                " ", "").replace("₽/шт.", "").strip()
            item_price = float(cleaned_price)
            logging.info(f"Цена товара успешно получена: {item_price}")
            return item_price
        except ValueError as e:
            logging.error(f"Ошибка преобразования цены: {e}")
            raise
        except exceptions.TimeoutException:
            logging.error("Не удалось получить цену товара.")
            raise

    def calculate_expected_price(self, quantity):
        """
        Вычисляет ожидаемую цену на основе количества товара.
        """
        logging.info("Вычисление ожидаемой итоговой цены.")
        item_price = float(self.get_item_price())
        return item_price * quantity

    def get_total_price(self):
        """
        Получает итоговую цену из корзины.
        """
        logging.info("Получение итоговой цены корзины.")
        try:
            # Дождаться появления элемента с итоговой ценой
            total_price_element = wait_for_element(
                self.driver, self.total_price_locator,
                EC.presence_of_element_located
            )
            # Удалить пробелы и валютный знак, затем преобразовать в float
            cleaned_price = total_price_element.text.replace(
                " ", "").replace("₽", "").strip()
            total_price = float(cleaned_price)
            logging.info(f"Итоговая цена успешно получена: {total_price}")
            return total_price
        except ValueError as e:
            logging.error(
                f"Ошибка преобразования строки в число: {e}")
            raise
        except exceptions.TimeoutException:
            logging.error(
                "Не удалось получить итоговую цену: элемент недоступен.")
            raise

    def wait_price_update(self):
        """
        Ожидание обновления локатора цены одного
          товара после изменения количества.
        """
        logging.info("Ожидание обновления цены одного товара.")
        try:
            WebDriverWait(self.driver, 8).until(
                lambda driver: (
                    element := self.
                    driver.find_element(
                        *self.item_price_locator
                        )).is_displayed() and element.text.strip() != "",
                "Цена товара не обновилась в течение заданного времени."
            )
            logging.info("Цена одного товара успешно обновлена.")
        except exceptions.TimeoutException:
            logging.error("Цена товара не обновилась в заданное время.")
            raise

    def wait_for_cart_to_load(self):
        """
        Ожидание загрузки корзины после перехода.
        """
        logging.info("Ожидание загрузки корзины.")
        try:
            WebDriverWait(self.driver, 7).until(
                lambda driver: driver.find_element(
                    *self.cart_item_count).is_displayed(),
                "Корзина не загрузилась в течение заданного времени."
            )
            logging.info("Корзина успешно загружена.")
        except exceptions.TimeoutException:
            logging.error("Корзина не загрузилась.")
            raise

    def click_increase_quantity_button(self):
        """
        Увеличивает количество товара в корзине, нажимая на кнопку "+".
        """
        logging.info(
            "Попытка нажать на кнопку '+' для увеличения количества товара."
            )
        try:
            # Ожидание появления кнопки
            quantity_plus = wait_for_element(
                self.driver, self.quantity_plus_button,
                EC.presence_of_element_located
            )
            # Клик через JavaScript
            self.driver.execute_script("arguments[0].click();", quantity_plus)
            logging.info("Кнопка '+' успешно нажата через JavaScript.")
        except exceptions.TimeoutException:
            logging.error("Кнопка '+' недоступна в течение заданного времени.")
            raise
        except exceptions.ElementClickInterceptedException as e:
            logging.error(f"Ошибка: элемент перекрыт. Детали: {str(e)}")
            raise
        except Exception as e:
            logging.error(
                "Неизвестная ошибка при взаимодействии с кнопкой '+': \n"
                f"{str(e)}"
                )
            raise
