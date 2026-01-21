"""Medusa Store - Cart Operations Tests."""

import pytest
import allure
from playwright.sync_api import expect


@allure.epic("Medusa Store")
@allure.feature("Cart Operations")
@pytest.mark.app("medusa_store")
@pytest.mark.e2e
class TestCartOperations:
    """Test suite for shopping cart operations."""

    @pytest.mark.testcase("TC-MS-021")
    @allure.title("TC-MS-021: View cart after adding product")
    def test_view_cart_with_items(self, store_page, product_page, cart_page, medusa_store_config):
        """Test viewing cart page after adding a product."""
        # Navigate and add product
        store_page.navigate_to_store()
        store_page.select_product("Hoodie")
        product_page.add_to_cart()
        
        # Verify cart badge shows item
        product_page.verify_cart_badge_visible()

    @pytest.mark.testcase("TC-MS-022")
    @allure.title("TC-MS-022: Cart page loads correctly")
    def test_cart_page_loads(self, cart_page, medusa_store_config):
        """Test that cart page loads (empty or with items)."""
        # Navigate directly to cart
        cart_page.navigate_to_cart()
        
        # Page should load without errors
        # Cart might be empty or have items depending on session
        assert cart_page.page.url.endswith("/cart")
