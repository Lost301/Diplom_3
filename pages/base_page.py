"""Базовый класс Page Object: общие методы работы с элементами."""
import time

import allure
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators import ModalLocators


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Дождаться видимости элемента {locator}")
    def wait_for_element_visible(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Дождаться кликабельности элемента {locator}")
    def wait_for_element_clickable(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Дождаться исчезновения элемента {locator}")
    def wait_for_element_invisible(self, locator, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    @allure.step("Дождаться исчезновения оверлея модального окна")
    def wait_modal_overlay_invisible(self, timeout=15):
        try:
            self.wait_for_element_invisible(ModalLocators.MODAL_OVERLAY, timeout=timeout)
        except TimeoutException:
            # оверлей не исчезает - всё равно попробуем кликнуть ещё раз
            pass

    @allure.step("Кликнуть по элементу {locator}")
    def click(self, locator, attempts=3):
        last_error = None
        for attempt in range(attempts):
            element = self.wait_for_element_clickable(locator)
            try:
                element.click()
                return
            except ElementClickInterceptedException as error:
                # поверх элемента может вспыхнуть оверлей модального окна -
                # ждём его исчезновения и повторяем клик
                last_error = error
                self.wait_modal_overlay_invisible()
                time.sleep(1)
        raise last_error

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator):
        return self.wait_for_element_visible(locator).text

    @allure.step("Проверить, что элемент {locator} отображается")
    def is_element_displayed(self, locator):
        return self.wait_for_element_visible(locator).is_displayed()

    @allure.step("Перетащить элемент {source_locator} с индексом {source_index} в зону {target_locator}")
    def drag_and_drop(self, source_locator, target_locator, source_index=0):
        source = self.driver.find_elements(*source_locator)[source_index]
        target = self.wait_for_element_visible(target_locator)
        self.driver.execute_script(
            """
            const source = arguments[0], target = arguments[1];
            const dt = new DataTransfer();
            source.dispatchEvent(new DragEvent('dragstart', {bubbles: true, dataTransfer: dt}));
            target.dispatchEvent(new DragEvent('dragover', {bubbles: true, dataTransfer: dt}));
            target.dispatchEvent(new DragEvent('drop', {bubbles: true, dataTransfer: dt}));
            source.dispatchEvent(new DragEvent('dragend', {bubbles: true, dataTransfer: dt}));
            """,
            source,
            target,
        )

    @allure.step("Открыть страницу {url}")
    def open(self, url):
        self.driver.get(url)

    @allure.step("Проверить, что текущий URL соответствует {url}")
    def is_current_url(self, url):
        WebDriverWait(self.driver, 15).until(EC.url_to_be(url))
        return self.driver.current_url == url

    @allure.step("Обновить страницу")
    def refresh(self):
        self.driver.refresh()
