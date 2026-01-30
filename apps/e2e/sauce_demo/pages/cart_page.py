"""Sauce Demo Cart Page."""

from playwright.sync_api import Page
import allure
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for Cart page."""

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_items = self.page.locator('.cart_item')
        self.checkout_button = self.page.locator('[data-test="checkout"]')
        self.continue_shopping_button = self.page.locator('[data-test="continue-shopping"]')

    def get_item_names(self) -> list[str]:
        """Get names of items in cart."""
        return self.cart_items.locator('.inventory_item_name').all_inner_texts()

    @allure.step("Proceed to checkout")
    def checkout(self):
        """Click checkout button."""
        self.checkout_button.click()

    @allure.step("Remove item from cart: {product_name}")
    def remove_item(self, product_name: str):
        """Remove specific item from cart."""
        slug = product_name.lower().replace(" ", "-")
        self.page.locator(f'[data-test="remove-{slug}"]').click()

    @allure.step("Continue shopping")
    def continue_shopping(self):
        """Click continue shopping button."""
        self.continue_shopping_button.click()

    def get_item_count(self) -> int:
        """Get number of items in cart."""
        return self.cart_items.count()
