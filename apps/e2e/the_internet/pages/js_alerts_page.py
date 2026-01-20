"""The Internet JavaScript Alerts Page."""

from playwright.sync_api import Page
import allure
from pages.base_page import BasePage


class JavaScriptAlertsPage(BasePage):
    """Page object for JavaScript Alerts page."""

    URL_SUFFIX = "/javascript_alerts"

    def __init__(self, page: Page):
        super().__init__(page)
        self.alert_button = self.page.get_by_text("Click for JS Alert")
        self.confirm_button = self.page.get_by_text("Click for JS Confirm")
        self.prompt_button = self.page.get_by_text("Click for JS Prompt")
        self.result = self.page.locator('#result')

    @allure.step("Navigate to JavaScript Alerts Page")
    def navigate_to_alerts(self, base_url: str):
        """Navigate to alerts page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Click alert button")
    def click_alert(self):
        """Click the alert button."""
        self.alert_button.click()

    @allure.step("Click confirm button")
    def click_confirm(self):
        """Click the confirm button."""
        self.confirm_button.click()

    @allure.step("Click prompt button")
    def click_prompt(self):
        """Click the prompt button."""
        self.prompt_button.click()

    def get_result_text(self) -> str:
        """Get result text."""
        return self.result.inner_text()
