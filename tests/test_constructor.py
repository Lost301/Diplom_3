"""Тесты основной функциональности раздела «Конструктор» (тесты 1–5)."""
import allure

from data import Urls
from locators import FeedPageLocators, MainPageLocators, ModalLocators
from pages.feed_page import FeedPage
from pages.main_page import MainPage


@allure.epic("Stellar Burgers")
@allure.feature("Конструктор")
class TestConstructor:
    @allure.title("Переход по клику на «Конструктор» из ленты заказов")
    def test_click_constructor_opens_constructor(self, driver):
        feed_page = FeedPage(driver)
        feed_page.open_feed_page()
        assert feed_page.is_current_url(Urls.FEED_PAGE)

        main_page = MainPage(driver)
        main_page.click_constructor_link()

        assert main_page.is_current_url(Urls.MAIN_PAGE)
        assert main_page.is_element_displayed(MainPageLocators.CONSTRUCTOR_BASKET)

    @allure.title("Переход по клику на раздел «Лента заказов»")
    def test_click_feed_opens_feed(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        assert main_page.is_current_url(Urls.MAIN_PAGE)

        main_page.click_feed_link()

        assert main_page.is_current_url(Urls.FEED_PAGE)
        feed_page = FeedPage(driver)
        assert feed_page.is_element_displayed(FeedPageLocators.TOTAL_ORDERS_COUNTER)

    @allure.title("Клик на ингредиент открывает всплывающее окно с деталями")
    def test_click_ingredient_opens_details_modal(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()

        main_page.click_ingredient()

        assert main_page.wait_ingredient_modal().is_displayed()

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_close_modal_by_cross(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.click_ingredient()
        main_page.wait_ingredient_modal()

        main_page.close_modal()

        assert len(main_page.driver.find_elements(*ModalLocators.OPENED_MODAL)) == 0

    @allure.title("При добавлении ингредиента в заказ счётчик увеличивается")
    def test_add_ingredient_increases_counter(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        counter_before = main_page.get_ingredient_counter()

        main_page.add_ingredient_to_constructor()

        counter_after = main_page.get_ingredient_counter()
        assert counter_after > counter_before
