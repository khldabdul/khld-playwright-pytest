"""Sauce Demo Inventory Page."""

from playwright.sync_api import Page, Locator
import allure
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page object for Inventory page."""

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.inventory_list = self.page.locator('.inventory_list')
        self.items = self.page.locator('.inventory_item')
        self.shopping_cart_badge = self.page.locator('.shopping_cart_badge')
        self.shopping_cart_link = self.page.locator('.shopping_cart_link')
        self.sort_select = self.page.locator('.product_sort_container')

    @allure.step("Add product to cart: {product_name}")
    def add_to_cart(self, product_name: str):
        """Add a specific product to cart by name."""
        # Find item by text description inside inventory item
        # Simplified: Use data-test format normally, but here we construct it dynamically or find by text
        # The site uses kebab-case data-tests like 'add-to-cart-sauce-labs-backpack'
        slug = product_name.lower().replace(" ", "-")
        self.page.locator(f'[data-test="add-to-cart-{slug}"]').click()

    def get_cart_count(self) -> int:
        """Get number of items in cart."""
        if self.shopping_cart_badge.is_visible():
            return int(self.shopping_cart_badge.inner_text())
        return 0

    @allure.step("Go to cart")
    def go_to_cart(self):
        """Navigate to cart page."""
        self.shopping_cart_link.click()

    def get_item_prices(self) -> list[float]:
        """Get list of all item prices currently visible."""
        price_elements = self.page.locator('.inventory_item_price').all()
        return [float(el.inner_text().replace('$', '')) for el in price_elements]

    def get_item_names(self) -> list[str]:
        """Get list of all product names."""
        name_elements = self.page.locator('.inventory_item_name').all()
        return [el.inner_text() for el in name_elements]

    @allure.step("Sort by: {sort_option}")
    def sort_products(self, sort_option: str):
        """Sort products by given option."""
        self.sort_select.select_option(value=sort_option)

    def get_product_count(self) -> int:
        """Get number of products displayed."""
        return self.items.count()

    @allure.step("Remove product from cart: {product_name}")
    def remove_from_cart(self, product_name: str):
        """Remove a specific product from cart."""
        slug = product_name.lower().replace(" ", "-")
        self.page.locator(f'[data-test="remove-{slug}"]').click()

    def is_in_cart(self, product_name: str) -> bool:
        """Check if product is in cart (Remove button visible)."""
        slug = product_name.lower().replace(" ", "-")
        return self.page.locator(f'[data-test="remove-{slug}"]').is_visible()

    @allure.step("Click product: {product_name}")
    def click_product(self, product_name: str):
        """Click on product name to view details."""
        self.page.get_by_text(product_name, exact=True).first.click()
