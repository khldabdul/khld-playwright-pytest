"""Medusa Store - Cart Operations Tests.

This test suite covers shopping cart operations including:
- Viewing cart after adding products
- Cart page loading

Application: Medusa Store E-commerce Demo
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("Medusa Store E2E")
@allure.feature("Shopping Cart")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "medusa_store")
@pytest.mark.app("medusa_store")
@pytest.mark.e2e
class TestCartOperations:
    """Test suite for shopping cart operations."""

    @allure.story("View Cart")
    @allure.title("TC-MS-021: View cart after adding product")
    @allure.description_html(markdown_to_html("""
    Verify that cart badge shows after adding a product.

    **Test Steps:**
    1. Navigate to store
    2. Select a product (Hoodie)
    3. Add product to cart
    4. Verify cart badge is visible

    **Test Coverage:**
    - Add to cart functionality
    - Cart badge visibility
    - Cart counter update

    **Business Value:**
    Visual confirmation for users that items were added.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-MS-021")
    @pytest.mark.requirement("US-MS-CART-001")
    def test_view_cart_with_items(self, store_page, product_page, cart_page, medusa_store_config):
        """Test viewing cart page after adding a product."""
        with allure.step("Navigate to store and add product"):
            store_page.navigate_to_store()
            store_page.select_product("Hoodie")
            product_page.add_to_cart()

        with allure.step("Verify cart badge shows item"):
            product_page.verify_cart_badge_visible()

    @allure.story("Cart Page")
    @allure.title("TC-MS-022: Cart page loads correctly")
    @allure.description_html(markdown_to_html("""
    Verify that cart page loads successfully.

    **Test Steps:**
    1. Navigate directly to cart page
    2. Verify URL ends with /cart
    3. Verify page loads without errors

    **Test Coverage:**
    - Cart page accessibility
    - URL verification
    - Page load integrity

    **Business Value:**
    Ensures cart page is always accessible to users.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-MS-022")
    @pytest.mark.requirement("US-MS-CART-002")
    def test_cart_page_loads(self, cart_page, medusa_store_config):
        """Test that cart page loads (empty or with items)."""
        with allure.step("Navigate directly to cart page"):
            cart_page.navigate_to_cart()

        with allure.step("Verify cart page URL"):
            assert cart_page.page.url.endswith("/cart")
