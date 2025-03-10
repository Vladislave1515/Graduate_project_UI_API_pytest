from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from pages.Search_Page_UI import wait_for_element


def wait_for_element_to_disappear(driver, locator, timeout=3):
    """
    Ждёт, пока указанный элемент исчезнет с DOM-дерева.
    """
    WebDriverWait(driver, timeout).until_not(
        EC.presence_of_element_located(locator)
    )


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.buy_button = (
            By.CSS_SELECTOR, ".product-card__controls .button"
            )
        self.cart_item_count = (
            By.CSS_SELECTOR,
            ".sticky-header__controls .header-cart__badge"
            )
        self.cart_icon = (
            By.CSS_SELECTOR, ".header-cart__icon.header-cart__icon--desktop"
            )
        self.remove_button = (
            By.CSS_SELECTOR, ".cart-item__actions-button--delete.light-blue"
            )
        self.notification_text = (
            By.CSS_SELECTOR, ".item-removed__description-title"
            )

    def click_buy_button(self):
        """
        Клик по кнопке 'КУПИТЬ', даже если она заблокирована.
        """
        try:
            # Ждать, пока кнопка станет кликабельной
            buy_button = wait_for_element(
                self.driver, self.buy_button,
                EC.element_to_be_clickable, timeout=5
            )

            # Прокрутить страницу до кнопки
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", buy_button
                )

            # Выполнить клик через JavaScript
            self.driver.execute_script(
                "arguments[0].click();", buy_button
                )
        except ElementClickInterceptedException:
            print("Кнопка перекрыта другим элементом, ждём устранения.")
            blocker_locator = (By.CSS_SELECTOR, "input.search.search-input")
            wait_for_element_to_disappear(self.driver, blocker_locator)
            # Повторить клик
            self.driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            print("Ошибка:", str(e))

    def get_cart_item_count(self):
        """
        Получает количество товаров в корзине.
        Возвращает int или 0, если элементов нет.
        """
        try:
            cart_count = wait_for_element(
                self.driver, self.cart_item_count,
                EC.presence_of_element_located, timeout=3
            )
            return int(cart_count.text)
        except TimeoutException:
            return 0

    def open_cart(self):
        """
        Открыть корзину, нажав на иконку корзины.
        """
        cart_icon = wait_for_element(
            self.driver, self.cart_icon,
            EC.element_to_be_clickable, timeout=3
        )
        cart_icon.click()

    def remove_item_from_cart(self):
        """
        Удалить товар из корзины, нажав на кнопку удаления.
        """
        remove_button = wait_for_element(
            self.driver, self.remove_button,
            EC.element_to_be_clickable, timeout=3
        )
        remove_button.click()

    def get_notification_message(self):
        """
        Получить текст уведомления об удалении товара из корзины.
        """
        notification = wait_for_element(
            self.driver, self.notification_text,
            EC.presence_of_element_located, timeout=3
        )
        return notification.text
