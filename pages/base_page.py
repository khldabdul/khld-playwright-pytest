"""Base Page Object."""

from playwright.sync_api import Page, Locator
import allure


class BasePage:
    """Base class for all Page Objects."""

    def __init__(self, page: Page):
        """Initialize with Playwright page."""
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to URL."""
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url)
            
    def get_by_test_id(self, test_id: str) -> Locator:
        """Get element by data-test attribute."""
        return self.page.locator(f'[data-test="{test_id}"]')
