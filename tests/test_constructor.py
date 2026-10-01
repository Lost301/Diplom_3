"""Тесты основной функциональности раздела «Конструктор» (тесты 1–5)."""
import allure

from data import Urls
from pages.feed_page import FeedPage
from pages.main_page import MainPage


@allure.epic("Stellar Burgers")
@allure.feature("Конструктор")
class TestConstructor:
    @allure.title("Переход по клику на «Конструктор» из ленты заказов")
    def test_click_constructor_opens_constructor(self, driver, open_feed_page):
        feed_page = FeedPage(driver)
        assert feed_page.is_current_url(Urls.FEED_PAGE)

        main_page = MainPage(driver)
        main_page.click_constructor_link()

        assert main_page.is_current_url(Urls.MAIN_PAGE)
        assert main_page.is_constructor_displayed()

    @allure.title("Переход по клику на раздел «Лента заказов»")
    def test_click_feed_opens_feed(self, driver, open_main_page):
        main_page = MainPage(driver)
        assert main_page.is_current_url(Urls.MAIN_PAGE)

        main_page.click_feed_link()

        assert main_page.is_current_url(Urls.FEED_PAGE)
        feed_page = FeedPage(driver)
        assert feed_page.is_total_counter_displayed()

    @allure.title("Клик на ингредиент открывает всплывающее окно с деталями")
    def test_click_ingredient_opens_details_modal(self, driver, open_main_page):
        main_page = MainPage(driver)

        main_page.click_ingredient()

        assert main_page.wait_ingredient_modal().is_displayed()

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_close_modal_by_cross(self, driver, open_main_page):
        main_page = MainPage(driver)
        main_page.click_ingredient()
        main_page.wait_ingredient_modal()

        main_page.close_modal()

        assert main_page.is_modal_closed()

    @allure.title("При добавлении ингредиента в заказ счётчик увеличивается")
    def test_add_ingredient_increases_counter(self, driver, open_main_page):
        main_page = MainPage(driver)
        counter_before = main_page.get_ingredient_counter()

        main_page.add_ingredient_to_constructor()

        counter_after = main_page.get_ingredient_counter()
        assert counter_after > counter_before
