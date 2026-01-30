"""Sauce Demo Login Page."""

from playwright.sync_api import Page
import allure
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for Sauce Demo login page."""

    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = self.page.locator('[data-test="username"]')
        self.password_input = self.page.locator('[data-test="password"]')
        self.login_button = self.page.locator('[data-test="login-button"]')
        self.error_message = self.page.locator('[data-test="error"]')

    @allure.step("Navigate to Login Page")
    def attach(self):
        """Navigate to login page."""
        self.navigate(self.URL)

    @allure.step("Login with user: {username}")
    def login(self, username: str, password: str):
        """Login with given credentials."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        """Get displayed error message text."""
        return self.error_message.inner_text()
