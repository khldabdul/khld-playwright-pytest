"""Medusa Store Page."""

from playwright.sync_api import Page, expect
import allure
from pages.base_page import BasePage


class StorePage(BasePage):
    """Page object for Medusa Store main page."""

    URL = "https://next.medusajs.com/us/store"

    def __init__(self, page: Page):
        super().__init__(page)
        self.products = page.locator('[data-testid="product-wrapper"]')
        # Sometimes products are links inside a grid
        self.product_links = page.locator('a[href*="/products/"]')
        # Navigation/categories
        self.nav_links = page.locator('nav a')

    @allure.step("Navigate to Store")
    def navigate_to_store(self):
        """Navigate to store page."""
        self.navigate(self.URL)

    @allure.step("Select product: {name}")
    def select_product(self, name: str):
        """Click on a product by name."""
        # Try to find by text substring in the product link or card
        self.page.get_by_text(name).first.click()

    @allure.step("Navigate to category: {category_name}")
    def navigate_to_category(self, category_name: str):
        """Navigate to a specific category."""
        # Click navigation link containing category name
        self.page.get_by_role("link", name=category_name).click()
        self.page.wait_for_timeout(1500)  # Wait for products to load

    @allure.step("Verify products are visible")
    def verify_products_visible(self):
        """Verify at least one product is displayed."""
        expect(self.product_links.first).to_be_visible()

    @allure.step("Get product count")
    def get_product_count(self) -> int:
        """Get number of visible products."""
        return self.product_links.count()
