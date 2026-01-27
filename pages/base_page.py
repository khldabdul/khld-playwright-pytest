"""Base Page Object with common utilities."""

from playwright.sync_api import Page, Locator, expect
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

    # Common utilities
    def wait_for_element(self, selector: str, timeout: int = 10000) -> Locator:
        """Wait for element to be visible and return it."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def safe_click(self, selector: str, timeout: int = 10000) -> None:
        """Click element with built-in wait and Allure step."""
        with allure.step(f"Click on {selector}"):
            self.page.locator(selector).click(timeout=timeout)

    def safe_fill(self, selector: str, value: str, timeout: int = 10000) -> None:
        """Fill input with built-in wait and Allure step."""
        with allure.step(f"Fill {selector}"):
            self.page.locator(selector).fill(value, timeout=timeout)

    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """Take screenshot and attach to Allure report."""
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot

    def assert_visible(self, selector: str, timeout: int = 10000) -> None:
        """Assert element is visible."""
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def assert_text(self, selector: str, text: str, timeout: int = 10000) -> None:
        """Assert element contains text."""
        expect(self.page.locator(selector)).to_contain_text(text, timeout=timeout)

    def get_text(self, selector: str, timeout: int = 10000) -> str:
        """Get text content of element."""
        self.wait_for_element(selector, timeout)
        return self.page.locator(selector).text_content() or ""
