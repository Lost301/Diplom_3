"""Page Object страницы ленты заказов."""
import allure
from selenium.webdriver.support.ui import WebDriverWait

from data import Urls
from locators import FeedPageLocators
from pages.base_page import BasePage


class FeedPage(BasePage):
    @allure.step("Открыть страницу ленты заказов")
    def open_feed_page(self):
        self.open(Urls.FEED_PAGE)

    @allure.step("Получить значение счётчика «Выполнено за все время»")
    def get_total_orders_count(self):
        return int(self.get_text(FeedPageLocators.TOTAL_ORDERS_COUNTER))

    @allure.step("Получить значение счётчика «Выполнено за сегодня»")
    def get_today_orders_count(self):
        return int(self.get_text(FeedPageLocators.TODAY_ORDERS_COUNTER))

    @allure.step("Дождаться увеличения счётчика «Выполнено за все время» (было {previous})")
    def wait_total_orders_increased(self, previous, timeout=60):
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.get_total_orders_count() > previous
        )

    @allure.step("Дождаться увеличения счётчика «Выполнено за сегодня» (было {previous})")
    def wait_today_orders_increased(self, previous, timeout=60):
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.get_today_orders_count() > previous
        )

    @allure.step("Получить номера заказов в разделе «В работе»")
    def get_in_work_order_numbers(self):
        items = self.driver.find_elements(*FeedPageLocators.IN_WORK_ITEM)
        return [item.text.strip() for item in items]

    @allure.step("Дождаться появления заказа с номером {number} в разделе «В работе»")
    def wait_order_in_work(self, number, timeout=90):
        def _order_in_work(d):
            numbers = self.get_in_work_order_numbers()
            digits = ["".join(ch for ch in n if ch.isdigit()) for n in numbers]
            return str(number) in digits or f"{number:07d}" in digits

        WebDriverWait(self.driver, timeout).until(_order_in_work)
