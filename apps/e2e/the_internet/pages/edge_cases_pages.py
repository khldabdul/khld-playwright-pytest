"""The Internet Edge Cases Pages."""

from playwright.sync_api import Page
import allure
from pages.base_page import BasePage


class BrokenImagesPage(BasePage):
    """Page object for Broken Images page."""

    URL_SUFFIX = "/broken_images"

    def __init__(self, page: Page):
        super().__init__(page)
        self.images = self.page.locator('img')

    @allure.step("Navigate to Broken Images")
    def navigate_to_page(self, base_url: str):
        """Navigate to broken images page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    def count_images(self) -> int:
        """Count total images."""
        return self.images.count()

    def check_image_loaded(self, index: int) -> bool:
        """Check if image at index is loaded (naturalWidth > 0)."""
        result = self.images.nth(index).evaluate("img => img.naturalWidth > 0")
        return bool(result)


class ChallengingDOMPage(BasePage):
    """Page object for Challenging DOM page."""

    URL_SUFFIX = "/challenging_dom"

    def __init__(self, page: Page):
        super().__init__(page)
        # Use stable selectors instead of dynamic IDs
        self.buttons = self.page.locator('.button')
        self.table_rows = self.page.locator('table tbody tr')

    @allure.step("Navigate to Challenging DOM")
    def navigate_to_page(self, base_url: str):
        """Navigate to challenging DOM page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Click button {index}")
    def click_button(self, index: int):
        """Click button by index."""
        self.buttons.nth(index).click()

    def get_table_row_count(self) -> int:
        """Get number of table rows."""
        return self.table_rows.count()

    def get_cell_text(self, row: int, col: int) -> str:
        """Get text from specific cell."""
        return self.table_rows.nth(row).locator('td').nth(col).inner_text()


class InfiniteScrollPage(BasePage):
    """Page object for Infinite Scroll page."""

    URL_SUFFIX = "/infinite_scroll"

    def __init__(self, page: Page):
        super().__init__(page)
        self.paragraphs = self.page.locator('.jscroll-added')

    @allure.step("Navigate to Infinite Scroll")
    def navigate_to_page(self, base_url: str):
        """Navigate to infinite scroll page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Scroll to bottom")
    def scroll_to_bottom(self):
        """Scroll to bottom of page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def get_paragraph_count(self) -> int:
        """Get number of loaded paragraphs."""
        return self.paragraphs.count()
