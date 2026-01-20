"""Sauce Demo Checkout Pages."""

from playwright.sync_api import Page
import allure
from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    """Page object for Checkout Step 1 (Information)."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = self.page.locator('[data-test="firstName"]')
        self.last_name_input = self.page.locator('[data-test="lastName"]')
        self.postal_code_input = self.page.locator('[data-test="postalCode"]')
        self.continue_button = self.page.locator('[data-test="continue"]')
        self.cancel_button = self.page.locator('[data-test="cancel"]')

    @allure.step("Fill checkout info")
    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        """Fill information form and continue."""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    @allure.step("Cancel checkout")
    def cancel(self):
        """Click cancel button."""
        self.cancel_button.click()

    def get_error_message(self) -> str:
        """Get error message text."""
        error = self.page.locator('[data-test="error"]')
        if error.is_visible():
            return error.inner_text()
        return ""


class CheckoutStepTwoPage(BasePage):
    """Page object for Checkout Step 2 (Overview)."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.finish_button = self.page.locator('[data-test="finish"]')
        self.cancel_button = self.page.locator('[data-test="cancel"]')
        self.subtotal_label = self.page.locator('.summary_subtotal_label')
        self.total_label = self.page.locator('.summary_total_label')

    @allure.step("Finish checkout")
    def finish(self):
        """Complete the purchase."""
        self.finish_button.click()

    def get_subtotal(self) -> float:
        """Get subtotal amount."""
        text = self.subtotal_label.inner_text()
        # Extract number from "Item total: $29.99" format
        return float(text.split('$')[1])

    def get_total(self) -> float:
        """Get total amount including tax."""
        text = self.total_label.inner_text()
        # Extract number from "Total: $32.39" format
        return float(text.split('$')[1])

    @allure.step("Cancel checkout")
    def cancel(self):
        """Click cancel button."""
        self.cancel_button.click()


class CheckoutCompletePage(BasePage):
    """Page object for Checkout Complete."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.header = self.page.locator('.complete-header')
        self.text = self.page.locator('.complete-text')
        self.back_home_button = self.page.locator('[data-test="back-to-products"]')

    def get_header(self) -> str:
        """Get completion header text."""
        return self.header.inner_text()
