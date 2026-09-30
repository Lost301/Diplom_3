"""Тесты раздела «Лента заказов» (тесты 6–8, требуется авторизация)."""
import allure

from pages.feed_page import FeedPage
from pages.main_page import MainPage


@allure.epic("Stellar Burgers")
@allure.feature("Лента заказов")
class TestFeed:
    @allure.title("При создании нового заказа счётчик «Выполнено за все время» увеличивается")
    def test_new_order_increases_total_counter(self, driver, user):
        feed_page = FeedPage(driver)
        feed_page.open_feed_page()
        total_before = feed_page.get_total_orders_count()

        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.add_ingredient_to_constructor()  # булка (считается как 2)
        main_page.add_ingredient_to_constructor(index=1)  # начинка
        main_page.click_order_button()
        main_page.wait_order_number()

        feed_page.open_feed_page()
        feed_page.wait_total_orders_increased(total_before, timeout=60)
        assert feed_page.get_total_orders_count() > total_before

    @allure.title("При создании нового заказа счётчик «Выполнено за сегодня» увеличивается")
    def test_new_order_increases_today_counter(self, driver, user):
        feed_page = FeedPage(driver)
        feed_page.open_feed_page()
        today_before = feed_page.get_today_orders_count()

        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.add_ingredient_to_constructor()
        main_page.add_ingredient_to_constructor(index=1)
        main_page.click_order_button()
        main_page.wait_order_number()

        feed_page.open_feed_page()
        feed_page.wait_today_orders_increased(today_before, timeout=60)
        assert feed_page.get_today_orders_count() > today_before

    @allure.title("После оформления заказа его номер появляется в разделе «В работе»")
    def test_new_order_appears_in_work_section(self, driver, user):
        # лента открыта заранее: обновления по websocket приходят в реальном времени
        feed_page = FeedPage(driver)
        feed_page.open_feed_page()

        driver.switch_to.new_window("tab")
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.add_ingredient_to_constructor()
        main_page.add_ingredient_to_constructor(index=1)
        main_page.click_order_button()
        order_number = main_page.wait_order_number()

        driver.switch_to.window(driver.window_handles[0])
        feed_page.wait_order_in_work(order_number, timeout=90)
        in_work_digits = [
            "".join(ch for ch in n if ch.isdigit())
            for n in feed_page.get_in_work_order_numbers()
        ]
        assert str(order_number) in in_work_digits or f"{order_number:07d}" in in_work_digits
