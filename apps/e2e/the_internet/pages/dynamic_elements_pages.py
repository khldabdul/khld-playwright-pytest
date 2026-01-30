"""The Internet Dynamic Loading Pages."""

from playwright.sync_api import Page
import allure
from pages.base_page import BasePage


class DynamicLoadingPage(BasePage):
    """Page object for Dynamic Loading pages."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.start_button = self.page.get_by_text("Start")
        self.loading_indicator = self.page.locator('#loading')
        self.finish_text = self.page.locator('#finish')

    @allure.step("Navigate to dynamic loading example {example_num}")
    def navigate_to_example(self, base_url: str, example_num: int):
        """Navigate to specific dynamic loading example."""
        self.navigate(f"{base_url}/dynamic_loading/{example_num}")

    @allure.step("Click start button")
    def click_start(self):
        """Click the start button."""
        self.start_button.click()

    def wait_for_loading_complete(self):
        """Wait for loading to complete."""
        self.loading_indicator.wait_for(state="hidden")

    def get_finish_text(self) -> str:
        """Get the finish message text."""
        return self.finish_text.inner_text()


class AddRemoveElementsPage(BasePage):
    """Page object for Add/Remove Elements page."""

    URL_SUFFIX = "/add_remove_elements/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.add_button = self.page.get_by_text("Add Element")
        self.delete_buttons = self.page.locator('.added-manually')

    @allure.step("Navigate to Add/Remove Elements")
    def navigate_to_page(self, base_url: str):
        """Navigate to add/remove elements page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Add element")
    def add_element(self):
        """Click add element button."""
        self.add_button.click()

    @allure.step("Delete element {index}")
    def delete_element(self, index: int = 0):
        """Delete element by index."""
        self.delete_buttons.nth(index).click()

    def get_delete_button_count(self) -> int:
        """Get number of delete buttons."""
        return self.delete_buttons.count()


class DisappearingElementsPage(BasePage):
    """Page object for Disappearing Elements."""

    URL_SUFFIX = "/disappearing_elements"

    def __init__(self, page: Page):
        super().__init__(page)
        self.menu_items = self.page.locator('ul li')

    @allure.step("Navigate to Disappearing Elements")
    def navigate_to_page(self, base_url: str):
        """Navigate to disappearing elements page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    def get_menu_item_count(self) -> int:
        """Get number of menu items."""
        return self.menu_items.count()

    def reload_page(self):
        """Reload the page."""
        self.page.reload()
