"""Medusa Store - Product Browsing Tests."""

import pytest
import allure
from playwright.sync_api import expect


@allure.epic("Medusa Store")
@allure.feature("Product Browsing")
@pytest.mark.app("medusa_store")
@pytest.mark.e2e
class TestProductBrowsing:
    """Test suite for product browsing."""

    @allure.title("TC-MS-010: View product details")
    def test_view_product_details(self, store_page, product_page, medusa_store_config):
        """Test viewing product detail page."""
        # Navigate to store
        store_page.navigate_to_store()
        
        # Click on first product
        store_page.select_product("Hoodie")  # Use known product
        
        # Verify product details are visible
        product_page.verify_product_details_visible()

    @allure.title("TC-MS-020: Add product to cart")
    def test_add_to_cart(self, store_page, product_page, medusa_store_config):
        """Test adding a product to cart."""
        # Navigate to store
        store_page.navigate_to_store()
        
        # Select product
        store_page.select_product("Hoodie")
        
        # Add to cart
        product_page.add_to_cart()
        
        # Verify cart badge is visible (indicates item added)
        product_page.verify_cart_badge_visible()
