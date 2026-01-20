"""The Internet Dropdown Page."""

from playwright.sync_api import Page, Locator
import allure
from pages.base_page import BasePage


class DropdownPage(BasePage):
    """Page object for Dropdown Page."""

    URL_SUFFIX = "/dropdown"

    def __init__(self, page: Page):
        super().__init__(page)
        self.dropdown = self.page.locator('#dropdown')

    @allure.step("Navigate to Dropdown Page")
    def navigate_to_dropdown(self, base_url: str):
        """Navigate to dropdown page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Select option {option_value}")
    def select_option(self, option_value: str):
        """Select option by value."""
        self.dropdown.select_option(value=option_value)

    def get_selected_option_text(self) -> str:
        """Get text of selected option."""
        # option[selected="selected"] might not update in all browsers/frameworks
        # but for native select it usually works, or evaluate logic
        return self.page.eval_on_selector('#dropdown', 'el => el.options[el.selectedIndex].text')
