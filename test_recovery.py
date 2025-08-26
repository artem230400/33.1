import pytest
import config
from pages.auth_page import AuthPage
from pages.recovery_page import RecoveryPage

class TestPasswordRecovery:
    """Тесты восстановления пароля"""

    def test_recovery_page_loads(self, driver):
        """Страница восстановления пароля загружается"""
        auth_page = AuthPage(driver).open()
        auth_page.go_to_recovery()
        recovery_page = RecoveryPage(driver)
        assert recovery_page.is_page_loaded()

    def test_recovery_with_nonexistent_phone(self, driver):
        """Восстановление с несуществующим номером телефона"""
        auth_page = AuthPage(driver).open()
        auth_page.go_to_recovery()
        recovery_page = RecoveryPage(driver)
        (recovery_page.select_tab("phone")
         .enter_username(config.INVALID_PHONE)
         .submit())
        assert "Учетная запись не найдена" in recovery_page.get_error_message()

    def test_recovery_with_nonexistent_email(self, driver):
        """Восстановление с несуществующей почтой"""
        auth_page = AuthPage(driver).open()
        auth_page.go_to_recovery()
        recovery_page = RecoveryPage(driver)
        (recovery_page.select_tab("mail")
         .enter_username(config.INVALID_EMAIL)
         .submit())
        assert "Учетная запись не найдена" in recovery_page.get_error_message()

    def test_captcha_required(self, driver):
        """Присутствует поле CAPTCHA"""
        auth_page = AuthPage(driver).open()
        auth_page.go_to_recovery()
        recovery_page = RecoveryPage(driver)
        assert recovery_page.is_captcha_present()

    def test_back_button_works(self, driver):
        """Кнопка 'Вернуться назад' работает"""
        auth_page = AuthPage(driver).open()
        auth_page.go_to_recovery()
        recovery_page = RecoveryPage(driver)
        recovery_page.go_back()
        assert "my.rt.ru" in driver.current_url

    @pytest.mark.skip("Требуется переход на форму ввода нового пароля")
    def test_new_password_validation(self, driver):
        """Валидация нового пароля"""
        recovery_page = RecoveryPage(driver)
        recovery_page.enter_new_password(config.SHORT_PASSWORD)
        recovery_page.confirm_new_password(config.SHORT_PASSWORD)
        recovery_page.submit()
        assert "Длина пароля должна быть не менее 8 символов" in recovery_page.get_error_message()