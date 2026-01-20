"""The Internet Login Page."""

from playwright.sync_api import Page, expect
import allure
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for Login Page."""

    URL_SUFFIX = "/login"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = self.page.locator('#username')
        self.password_input = self.page.locator('#password')
        self.login_button = self.page.locator('button[type="submit"]')
        self.flash_message = self.page.locator('#flash')
        self.logout_button = self.page.locator('a[href="/logout"]')

    @allure.step("Navigate to Login Page")
    def navigate_to_login(self, base_url: str):
        """Navigate to login page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Login with {username}")
    def login(self, username: str, password: str):
        """Perform login."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_flash_message(self) -> str:
        """Get flash message text."""
        return self.flash_message.inner_text()
