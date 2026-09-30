"""Селекторы страниц Stellar Burgers."""
from selenium.webdriver.common.by import By


class MainPageLocators:
    # Шапка
    CONSTRUCTOR_LINK = (By.XPATH, "//header//a[@href='/']")
    FEED_LINK = (By.XPATH, "//header//a[@href='/feed']")

    # Ингредиенты
    INGREDIENT_CARD = (By.XPATH, "//a[contains(@class,'BurgerIngredient_ingredient__')]")
    # значение счётчика внутри карточки ингредиента (ищется относительно карточки)
    INGREDIENT_COUNTER_VALUE = (By.XPATH, ".//p[contains(@class,'counter_counter__num__')]")

    # Конструктор
    CONSTRUCTOR_BASKET = (By.XPATH, "//section[contains(@class,'BurgerConstructor_basket__')]")
    ORDER_BUTTON = (By.XPATH, "//button[contains(@class,'button_button_type_primary__')]")


class FeedPageLocators:
    # Счётчики «Выполнено за все время» / «Выполнено за сегодня»
    TOTAL_ORDERS_COUNTER = (By.XPATH, "(//p[contains(@class,'OrderFeed_number__')])[1]")
    TODAY_ORDERS_COUNTER = (By.XPATH, "(//p[contains(@class,'OrderFeed_number__')])[2]")

    # Раздел «В работе» — список с зелёной подсветкой (класс orderListReady):
    # в него попадают заказы со статусом «В работе», при пустом списке
    # отображается текст «Все текущие заказы готовы!»
    IN_WORK_LIST = (By.XPATH, "//ul[contains(@class,'OrderFeed_orderListReady__')]")
    IN_WORK_ITEM = (By.XPATH, "//ul[contains(@class,'OrderFeed_orderListReady__')]/li")


class ModalLocators:
    # Открытое модальное окно и его оверлей
    OPENED_MODAL = (By.XPATH, "//*[contains(@class,'Modal_modal_opened__')]")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class,'Modal_modal_overlay__')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//*[contains(@class,'Modal_modal_opened__')]//button[contains(@class,'Modal_modal__close__')]")

    # Модалка деталей ингредиента
    INGREDIENT_MODAL_TITLE = (
        By.XPATH,
        "//*[contains(@class,'Modal_modal_opened__')]"
        "//h2[contains(text(),'Детали ингредиента')]",
    )

    # Модалка номера заказа
    ORDER_NUMBER = (
        By.XPATH,
        "//*[contains(@class,'Modal_modal_opened__')]"
        "//h2[contains(@class,'Modal_modal__title')]",
    )
