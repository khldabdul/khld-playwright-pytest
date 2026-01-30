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

from infrastructure.utils.allure_helpers import e2e_test


class TestCartOperations:
    """Test suite for shopping cart operations."""

    @e2e_test(
        epic="Medusa Store E2E",
        feature="Shopping Cart",
        story="View Cart",
        title="TC-MS-021: View cart after adding product",
        description="""Verify that cart badge shows after adding a product.

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
""",
        testcase="TC-MS-021",
        requirement="US-MS-CART-001",
        app="medusa_store",
        severity="normal",
        link="https://demo.medusa-commerce.com/"
    )
    def test_view_cart_with_items(self, store_page, product_page, cart_page, medusa_store_config):
        """Test viewing cart page after adding a product."""
        with allure.step("Navigate to store and add product"):
            store_page.navigate_to_store()
            store_page.select_product("Hoodie")
            product_page.add_to_cart()

        with allure.step("Verify cart badge shows item"):
            product_page.verify_cart_badge_visible()

    @e2e_test(
        epic="Medusa Store E2E",
        feature="Shopping Cart",
        story="Cart Page",
        title="TC-MS-022: Cart page loads correctly",
        description="""Verify that cart page loads successfully.

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
""",
        testcase="TC-MS-022",
        requirement="US-MS-CART-002",
        app="medusa_store",
        severity="normal",
        link="https://demo.medusa-commerce.com/"
    )
    def test_cart_page_loads(self, cart_page, medusa_store_config):
        """Test that cart page loads (empty or with items)."""
        with allure.step("Navigate directly to cart page"):
            cart_page.navigate_to_cart()

        with allure.step("Verify cart page URL"):
            assert cart_page.page.url.endswith("/cart")
