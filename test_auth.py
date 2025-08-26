import pytest
import config
from pages.auth_page import AuthPage

class TestAuthentication:
    """Тесты авторизации на портале Онлайм"""

    @pytest.mark.skip("Требуются валидные данные: VALID_PHONE и VALID_PASSWORD")
    def test_successful_auth_by_phone(self, driver):
        """Успешная авторизация по номеру телефона"""
        auth_page = AuthPage(driver).open()
        (auth_page.select_tab("phone")
         .enter_username(config.VALID_PHONE)
         .enter_password(config.VALID_PASSWORD)
         .click_submit())
        assert "start.rt.ru" in driver.current_url

    def test_auth_with_nonexistent_phone(self, driver):
        """Авторизация с несуществующим номером телефона"""
        auth_page = AuthPage(driver).open()
        (auth_page.select_tab("phone")
         .enter_username(config.INVALID_PHONE)
         .enter_password(config.INVALID_PASSWORD)
         .click_submit())
        assert "Неверный логин или пароль" in auth_page.get_error_message()

    def test_auth_with_nonexistent_email(self, driver):
        """Авторизация с несуществующей почтой"""
        auth_page = AuthPage(driver).open()
        (auth_page.select_tab("mail")
         .enter_username(config.INVALID_EMAIL)
         .enter_password(config.INVALID_PASSWORD)
         .click_submit())
        assert "Неверный логин или пароль" in auth_page.get_error_message()

    def test_auth_with_empty_credentials(self, driver):
        """Авторизация с пустыми полями"""
        auth_page = AuthPage(driver).open()
        auth_page.click_submit()
        error_text = auth_page.get_error_message()
        assert error_text != ""

    def test_auto_tab_switch_on_email_input(self, driver):
        """Автоматическое переключение на таб 'Почта' при вводе email"""
        auth_page = AuthPage(driver).open()
        auth_page.select_tab("phone")
        auth_page.enter_username("test@mail.ru")
        assert "почта" in auth_page.get_active_tab_name()

    def test_auto_tab_switch_on_phone_input(self, driver):
        """Автоматическое переключение на таб 'Телефон' при вводе номера"""
        auth_page = AuthPage(driver).open()
        auth_page.select_tab("mail")
        auth_page.enter_username("9101234567")
        assert "телефон" in auth_page.get_active_tab_name()

    def test_password_field_masked(self, driver):
        """Поле пароля скрывает ввод"""
        auth_page = AuthPage(driver).open()
        password_field = auth_page.driver.find_element(*auth_page.PASSWORD_INPUT)
        password_field.send_keys("secret_password")
        assert password_field.get_attribute("type") == "password"

    def test_ls_tab_not_present_for_onlime(self, driver):
        """Таб 'Лицевой счет' отсутствует для продукта Онлайм"""
        auth_page = AuthPage(driver).open()
        ls_tabs = auth_page.driver.find_elements(*auth_page.LS_TAB)
        assert len(ls_tabs) == 0

    def test_forgot_password_link_visible(self, driver):
        """Ссылка 'Забыл пароль' отображается"""
        auth_page = AuthPage(driver).open()
        forgot_link = auth_page.driver.find_element(*auth_page.FORGOT_PASSWORD_LINK)
        assert forgot_link.is_displayed()

    def test_auth_by_code_button_visible(self, driver):
        """Кнопка 'Войти по временному коду' отображается"""
        auth_page = AuthPage(driver).open()
        code_button = auth_page.driver.find_element(*auth_page.CODE_LOGIN_BUTTON)
        assert code_button.is_displayed()

    def test_error_message_color(self, driver):
        """Сообщение об ошибке имеет красный цвет"""
        auth_page = AuthPage(driver).open()
        auth_page.click_submit()
        error_element = auth_page.driver.find_element(*auth_page.ERROR_MESSAGE)
        color = error_element.value_of_css_property("color")
        assert "rgb(255, 0, 0)" in color or "rgba(255, 0, 0" in color