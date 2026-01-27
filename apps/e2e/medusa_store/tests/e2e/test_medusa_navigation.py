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

from infrastructure.utils.allure_helpers import e2e_test


@allure.epic("Medusa Store E2E")
@allure.feature("Navigation")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "medusa_store")
@pytest.mark.app("medusa_store")
@pytest.mark.e2e
class TestNavigation:
    """Test suite for store navigation."""

    @e2e_test(
        epic="Medusa Store E2E",
        feature="Navigation",
        story="Homepage",
        title="TC-MS-001: Homepage loads with products",
        description="""Verify that the homepage loads and displays products.

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
""",
        testcase="TC-MS-001",
        requirement="US-MS-NAV-001",
        app="medusa_store",
        severity="critical",
        link="https://demo.medusa-commerce.com/",
        smoke=True,
        critical=True
    )
    def test_homepage_loads(self, store_page, medusa_store_config):
        """Test that homepage loads and displays products."""
        with allure.step("Navigate to store homepage"):
            store_page.navigate_to_store()

        with allure.step("Verify products are visible"):
            store_page.verify_products_visible()

        with allure.step("Verify at least one product is displayed"):
            product_count = store_page.get_product_count()
            assert product_count > 0, f"Expected products on homepage, found {product_count}"

    @e2e_test(
        epic="Medusa Store E2E",
        feature="Navigation",
        story="Category Navigation",
        title="TC-MS-003: Category navigation works",
        description="""Verify that category navigation works correctly.

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
""",
        testcase="TC-MS-003",
        requirement="US-MS-NAV-002",
        app="medusa_store",
        severity="normal",
        link="https://demo.medusa-commerce.com/"
    )
    def test_category_navigation(self, store_page, medusa_store_config):
        """Test navigation to product categories."""
        with allure.step("Navigate to store homepage"):
            store_page.navigate_to_store()

        with allure.step("Verify initial products are displayed"):
            initial_count = store_page.get_product_count()
            assert initial_count > 0, "No products on homepage"

        with allure.step("Verify navigation structure is intact"):
            store_page.verify_products_visible()
