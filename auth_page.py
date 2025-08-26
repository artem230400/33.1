from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthPage:
    PHONE_TAB = (By.ID, "t-btn-tab-phone")
    EMAIL_TAB = (By.ID, "t-btn-tab-mail")
    LOGIN_TAB = (By.ID, "t-btn-tab-login")
    LS_TAB = (By.ID, "t-btn-tab-ls")
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "kc-login")
    FORGOT_PASSWORD_LINK = (By.ID, "forgot_password")
    ERROR_MESSAGE = (By.ID, "form-error-message")
    CODE_LOGIN_BUTTON = (By.ID, "back_to_otp_btn")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get("https://my.rt.ru/")
        return self

    def select_tab(self, tab_name):
        tabs = {
            "phone": self.PHONE_TAB,
            "mail": self.EMAIL_TAB,
            "login": self.LOGIN_TAB,
            "ls": self.LS_TAB
        }
        self.wait.until(EC.element_to_be_clickable(tabs[tab_name])).click()
        return self

    def enter_username(self, username):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        return self

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        return self

    def click_submit(self):
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON)).click()
        return self

    def go_to_recovery(self):
        self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK)).click()
        return self

    def go_to_auth_by_code(self):
        self.wait.until(EC.element_to_be_clickable(self.CODE_LOGIN_BUTTON)).click()
        return self

    def get_error_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
        except:
            return ""

    def get_active_tab_name(self):
        active_tabs = self.driver.find_elements(By.CSS_SELECTOR,
                                                ".rt-tab.rt-tab--small.tabs-input-container__tab.tabs-input-container__tab--active")
        return active_tabs[0].text.lower() if active_tabs else ""