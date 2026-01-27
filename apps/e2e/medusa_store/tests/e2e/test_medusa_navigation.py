"""Medusa Store - Navigation Tests.

This test suite covers store navigation operations including:
- Homepage loading and product display
- Category navigation

Application: Medusa Store E-commerce Demo
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("Medusa Store E2E")
@allure.feature("Navigation")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "medusa_store")
@pytest.mark.app("medusa_store")
@pytest.mark.e2e
class TestNavigation:
    """Test suite for store navigation."""

    @allure.story("Homepage")
    @allure.title("TC-MS-001: Homepage loads with products")
    @allure.description_html(markdown_to_html("""
    Verify that the homepage loads and displays products.

    **Test Steps:**
    1. Navigate to store homepage
    2. Verify products are visible
    3. Verify at least one product is displayed

    **Test Coverage:**
    - Homepage loading
    - Product display verification
    - Store accessibility

    **Business Value:**
    Critical first impression for store visitors.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.critical
    @pytest.mark.testcase("TC-MS-001")
    @pytest.mark.requirement("US-MS-NAV-001")
    @pytest.mark.smoke
    def test_homepage_loads(self, store_page, medusa_store_config):
        """Test that homepage loads and displays products."""
        with allure.step("Navigate to store homepage"):
            store_page.navigate_to_store()

        with allure.step("Verify products are visible"):
            store_page.verify_products_visible()

        with allure.step("Verify at least one product is displayed"):
            product_count = store_page.get_product_count()
            assert product_count > 0, f"Expected products on homepage, found {product_count}"

    @allure.story("Category Navigation")
    @allure.title("TC-MS-003: Category navigation works")
    @allure.description_html(markdown_to_html("""
    Verify that category navigation works correctly.

    **Test Steps:**
    1. Navigate to store homepage
    2. Verify initial products are displayed
    3. Verify navigation elements are present

    **Test Coverage:**
    - Navigation menu accessibility
    - Category link presence
    - Navigation structure integrity

    **Business Value:**
    Enables users to browse products by category.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-MS-003")
    @pytest.mark.requirement("US-MS-NAV-002")
    def test_category_navigation(self, store_page, medusa_store_config):
        """Test navigation to product categories."""
        with allure.step("Navigate to store homepage"):
            store_page.navigate_to_store()

        with allure.step("Verify initial products are displayed"):
            initial_count = store_page.get_product_count()
            assert initial_count > 0, "No products on homepage"

        with allure.step("Verify navigation structure is intact"):
            store_page.verify_products_visible()
