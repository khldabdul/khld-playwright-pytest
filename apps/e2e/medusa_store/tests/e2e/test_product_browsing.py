"""Medusa Store - Product Browsing Tests.

This test suite covers product browsing operations including:
- Viewing product details
- Adding products to cart

Application: Medusa Store E-commerce Demo
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("Medusa Store E2E")
@allure.feature("Product Browsing")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "medusa_store")
@pytest.mark.app("medusa_store")
@pytest.mark.e2e
class TestProductBrowsing:
    """Test suite for product browsing."""

    @allure.story("View Product Details")
    @allure.title("TC-MS-010: View product details")
    @allure.description_html(markdown_to_html("""
    Verify that product details page displays correctly.

    **Test Steps:**
    1. Navigate to store homepage
    2. Select a product (Hoodie)
    3. Verify product details are visible

    **Test Coverage:**
    - Product detail page navigation
    - Product information display
    - Detail page accessibility

    **Business Value:**
    Essential for users to make informed purchase decisions.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.critical
    @pytest.mark.testcase("TC-MS-010")
    @pytest.mark.requirement("US-MS-PROD-001")
    @pytest.mark.smoke
    def test_view_product_details(self, store_page, product_page, medusa_store_config):
        """Test viewing product detail page."""
        product_name = "Hoodie"

        with allure.step("Navigate to store homepage"):
            store_page.navigate_to_store()

        with allure.step(f"Select product '{product_name}'"):
            store_page.select_product(product_name)

        with allure.step("Verify product details are visible"):
            product_page.verify_product_details_visible()

    @allure.story("Add to Cart")
    @allure.title("TC-MS-020: Add product to cart")
    @allure.description_html(markdown_to_html("""
    Verify that a product can be added to cart.

    **Test Steps:**
    1. Navigate to store homepage
    2. Select a product (Hoodie)
    3. Click add to cart button
    4. Verify cart badge becomes visible

    **Test Coverage:**
    - Add to cart functionality
    - Cart badge visibility
    - Cart state update

    **Business Value:**
    Core functionality for starting the purchase process.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.critical
    @pytest.mark.testcase("TC-MS-020")
    @pytest.mark.requirement("US-MS-PROD-002")
    @pytest.mark.smoke
    def test_add_to_cart(self, store_page, product_page, medusa_store_config):
        """Test adding a product to cart."""
        product_name = "Hoodie"

        with allure.step("Navigate to store homepage"):
            store_page.navigate_to_store()

        with allure.step(f"Select product '{product_name}'"):
            store_page.select_product(product_name)

        with allure.step("Add product to cart"):
            product_page.add_to_cart()

        with allure.step("Verify cart badge is visible"):
            product_page.verify_cart_badge_visible()
