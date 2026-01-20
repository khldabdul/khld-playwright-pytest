"""The Internet Interactions Pages."""

from playwright.sync_api import Page
import allure
from pages.base_page import BasePage


class DragDropPage(BasePage):
    """Page object for Drag and Drop page."""

    URL_SUFFIX = "/drag_and_drop"

    def __init__(self, page: Page):
        super().__init__(page)
        self.column_a = self.page.locator('#column-a')
        self.column_b = self.page.locator('#column-b')

    @allure.step("Navigate to Drag and Drop")
    def navigate_to_page(self, base_url: str):
        """Navigate to drag and drop page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Drag column A to column B")
    def drag_a_to_b(self):
        """Drag column A to column B position."""
        self.column_a.drag_to(self.column_b)

    def get_column_a_text(self) -> str:
        """Get text from column A."""
        return self.column_a.inner_text()

    def get_column_b_text(self) -> str:
        """Get text from column B."""
        return self.column_b.inner_text()


class HoverPage(BasePage):
    """Page object for Hover page."""

    URL_SUFFIX = "/hovers"

    def __init__(self, page: Page):
        super().__init__(page)
        self.user_images = self.page.locator('.figure')

    @allure.step("Navigate to Hover Page")
    def navigate_to_page(self, base_url: str):
        """Navigate to hover page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Hover over user {index}")
    def hover_user(self, index: int):
        """Hover over user image by index."""
        self.user_images.nth(index).hover()

    def is_user_info_visible(self, index: int) -> bool:
        """Check if user info is visible for given index."""
        user_info = self.user_images.nth(index).locator('.figcaption')
        return user_info.is_visible()

    def get_user_name(self, index: int) -> str:
        """Get user name text."""
        return self.user_images.nth(index).locator('h5').inner_text()


class TablesPage(BasePage):
    """Page object for Tables page."""

    URL_SUFFIX = "/tables"

    def __init__(self, page: Page):
        super().__init__(page)
        self.table = self.page.locator('#table1')
        self.headers = self.table.locator('thead th')
        self.rows = self.table.locator('tbody tr')

    @allure.step("Navigate to Tables Page")
    def navigate_to_page(self, base_url: str):
        """Navigate to tables page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Click header {header_text}")
    def click_header(self, header_text: str):
        """Click on column header."""
        self.table.get_by_text(header_text, exact=True).click()

    def get_column_values(self, column_index: int) -> list[str]:
        """Get all values from a specific column."""
        cells = self.rows.locator(f'td:nth-child({column_index + 1})')
        return [cell.inner_text() for cell in cells.all()]
