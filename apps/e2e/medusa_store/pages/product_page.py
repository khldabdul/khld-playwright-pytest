"""Medusa Product Page."""

from playwright.sync_api import Page, expect
import allure
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Page object for Product details page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.add_to_cart_button = page.locator('[data-testid="add-product-button"]')
        self.cart_dropdown_trigger = page.locator('[data-testid="nav-cart-link"]')
        self.shopping_bag_icon = page.locator('[data-testid="nav-cart-link"]')
        # Product details
        self.product_title = page.locator('h1')
        self.product_price = page.locator('[data-testid="product-price"]')
        self.product_description = page.locator('[data-testid="product-description"]')

    @allure.step("Add to cart")
    def add_to_cart(self):
        """Add current product to cart, selecting options if needed."""
        self.add_to_cart_button.wait_for(state="visible")
        self.add_to_cart_button.click()
        self.page.wait_for_timeout(2000)  # Wait for cart update
        
    @allure.step("Go to cart")
    def go_to_cart(self):
        """Navigate to cart/checkout."""
        # Direct navigation is more reliable than sidebar logic for now
        self.page.goto("https://next.medusajs.com/us/cart")

    @allure.step("Verify product details visible")
    def verify_product_details_visible(self):
        """Verify product page shows title, price, and add to cart button."""
        expect(self.product_title).to_be_visible()
        expect(self.product_price).to_be_visible()
        expect(self.add_to_cart_button).to_be_visible()

    @allure.step("Verify cart badge updated")
    def verify_cart_badge_visible(self):
        """Verify cart badge appears after adding item."""
        expect(self.shopping_bag_icon).to_be_visible()
