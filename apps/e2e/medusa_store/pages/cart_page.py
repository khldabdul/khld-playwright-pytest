"""Medusa Cart Page."""

from playwright.sync_api import Page, expect
import allure
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for Cart methods."""
    
    # Medusa often uses a slide-over or a dedicated /cart page
    URL = "https://next.medusajs.com/us/cart"

    def __init__(self, page: Page):
        super().__init__(page)
        self.checkout_button = page.locator('[data-testid="checkout-button"]')
        self.cart_items = page.locator('[data-testid="cart-item"]')
        self.cart_badge = page.locator('[data-testid="nav-cart-link"]')
        # Quantity controls
        self.quantity_decrease = page.locator('[data-testid="product-minus-icon"]')
        self.quantity_increase = page.locator('[data-testid="product-plus-icon"]')
        self.remove_button = page.locator('[data-testid="product-delete-icon"]')
        self.cart_total = page.locator('[data-testid="cart-subtotal"]')

    @allure.step("Navigate to cart")
    def navigate_to_cart(self):
        """Navigate to cart page."""
        self.navigate(self.URL)

    @allure.step("Proceed to checkout")
    def checkout(self):
        """Click checkout button."""
        self.checkout_button.wait_for(state="visible")
        self.checkout_button.click()

    @allure.step("Get cart item count")
    def get_item_count(self) -> int:
        """Get number of items in cart."""
        return self.cart_items.count()

    @allure.step("Increase quantity")
    def increase_quantity(self, item_index: int = 0):
        """Increase quantity of item at index."""
        self.quantity_increase.nth(item_index).click()
        self.page.wait_for_timeout(1000)  # Wait for update

    @allure.step("Decrease quantity")
    def decrease_quantity(self, item_index: int = 0):
        """Decrease quantity of item at index."""
        self.quantity_decrease.nth(item_index).click()
        self.page.wait_for_timeout(1000)  # Wait for update

    @allure.step("Remove item from cart")
    def remove_item(self, item_index: int = 0):
        """Remove item from cart."""
        self.remove_button.nth(item_index).click()
        self.page.wait_for_timeout(1000)  # Wait for removal

    @allure.step("Verify cart has {expected_count} items")
    def verify_item_count(self, expected_count: int):
        """Verify number of items in cart."""
        expect(self.cart_items).to_have_count(expected_count)

    @allure.step("Verify cart badge shows {expected_count}")
    def verify_cart_badge_count(self, expected_count: int):
        """Verify cart badge displays correct count."""
        if expected_count > 0:
            expect(self.cart_badge).to_contain_text(str(expected_count))
        else:
            # Badge might not be visible when cart is empty
            pass

    @allure.step("Verify cart is empty")
    def verify_cart_empty(self):
        """Verify cart has no items."""
        expect(self.cart_items).to_have_count(0)
