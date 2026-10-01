"""Page Object главной страницы (конструктор бургеров)."""
import allure

from data import Urls
from locators import MainPageLocators, ModalLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    @allure.step("Открыть главную страницу")
    def open_main_page(self):
        self.open(Urls.MAIN_PAGE)

    @allure.step("Кликнуть на «Конструктор» в шапке")
    def click_constructor_link(self):
        self.click(MainPageLocators.CONSTRUCTOR_LINK)

    @allure.step("Кликнуть на «Ленту заказов» в шапке")
    def click_feed_link(self):
        self.click(MainPageLocators.FEED_LINK)

    @allure.step("Кликнуть на первый ингредиент в списке")
    def click_ingredient(self):
        self.click(MainPageLocators.INGREDIENT_CARD)

    @allure.step("Дождаться открытия модалки с деталями ингредиента")
    def wait_ingredient_modal(self):
        return self.wait_for_element_visible(ModalLocators.INGREDIENT_MODAL_TITLE)

    @allure.step("Закрыть модальное окно кликом по крестику")
    def close_modal(self):
        self.click(ModalLocators.MODAL_CLOSE_BUTTON)
        self.wait_for_element_invisible(ModalLocators.OPENED_MODAL)

    @allure.step("Добавить ингредиент с индексом {index} в конструктор")
    def add_ingredient_to_constructor(self, index=0):
        self.drag_and_drop(
            MainPageLocators.INGREDIENT_CARD,
            MainPageLocators.CONSTRUCTOR_BASKET,
            source_index=index,
        )

    @allure.step("Получить значение счётчика ингредиента с индексом {index}")
    def get_ingredient_counter(self, index=0):
        cards = self.find_elements(MainPageLocators.INGREDIENT_CARD)
        counters = cards[index].find_elements(*MainPageLocators.INGREDIENT_COUNTER_VALUE)
        # счётчик появляется у ингредиента только после добавления в заказ,
        # до этого его значение равно нулю
        return int(counters[0].text) if counters else 0

    @allure.step("Проверить, что отображается конструктор заказов")
    def is_constructor_displayed(self):
        return self.is_element_displayed(MainPageLocators.CONSTRUCTOR_BASKET)

    @allure.step("Проверить, что модальное окно закрыто")
    def is_modal_closed(self):
        return self.count_elements(ModalLocators.OPENED_MODAL) == 0

    @allure.step("Кликнуть по кнопке «Оформить заказ»")
    def click_order_button(self):
        self.wait_modal_overlay_invisible()
        self.click(MainPageLocators.ORDER_BUTTON)

    @allure.step("Дождаться появления номера заказа в модальном окне")
    def wait_order_number(self, timeout=40):
        number_element = self.wait_for_element_visible(ModalLocators.ORDER_NUMBER, timeout=timeout)
        # номер появляется не мгновенно: сначала в модалке заглушка «9999»
        self.wait_until(
            lambda _: number_element.text.strip().isdigit()
            and number_element.text.strip() != "9999",
            timeout=timeout,
            message="появления номера заказа в модальном окне",
        )
        return int(number_element.text.strip())
