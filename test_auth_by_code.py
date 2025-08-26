import pytest
import config
from pages.auth_page import AuthPage
from pages.auth_code_page import AuthCodePage

class TestAuthByCode:
    """Тесты авторизации по временному коду"""

    def test_auth_by_code_page_loads(self, driver):
        """Страница авторизации по коду загружается"""
        auth_page = AuthPage(driver).open()
        auth_page.go_to_auth_by_code()
        code_page = AuthCodePage(driver)
        assert code_page.is_page_loaded()

    def test_code_input_fields_present(self, driver):
        """Присутствуют поля для ввода кода"""
        auth_page = AuthPage(driver).open()
        auth_page.go_to_auth_by_code()
        code_page = AuthCodePage(driver)
        assert code_page.get_code_inputs_count() == 6

    def test_phone_input_validation(self, driver):
        """Валидация поля телефона"""
        auth_page = AuthPage(driver).open()
        auth_page.go_to_auth_by_code()
        code_page = AuthCodePage(driver)
        code_page.enter_phone("123")
        code_page.submit()
        assert "Номер в формате" in code_page.get_error_message()

    def test_get_code_button_works(self, driver):
        """Кнопка 'Получить код' кликабельна"""
        auth_page = AuthPage(driver).open()
        auth_page.go_to_auth_by_code()
        code_page = AuthCodePage(driver)
        assert code_page.is_get_code_button_enabled()