"""The Internet Checkboxes Page."""

from playwright.sync_api import Page, Locator
import allure
from pages.base_page import BasePage


class CheckboxesPage(BasePage):
    """Page object for Checkboxes Page."""

    URL_SUFFIX = "/checkboxes"

    def __init__(self, page: Page):
        super().__init__(page)
        self.checkboxes = self.page.locator('#checkboxes input[type="checkbox"]')

    @allure.step("Navigate to Checkboxes Page")
    def navigate_to_checkboxes(self, base_url: str):
        """Navigate to checkboxes page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Toggle checkbox {index}")
    def toggle_checkbox(self, index: int, check: bool):
        """Set checkbox state."""
        checkbox = self.checkboxes.nth(index)
        if check:
            checkbox.check()
        else:
            checkbox.uncheck()

    def is_checked(self, index: int) -> bool:
        """Check if checkbox is checked."""
        return self.checkboxes.nth(index).is_checked()
