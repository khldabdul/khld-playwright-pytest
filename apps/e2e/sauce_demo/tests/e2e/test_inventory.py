"""Sauce Demo Inventory Tests.

This test suite covers inventory page operations including:
- Viewing all products
- Sorting products by price and name
- Adding products to cart
- Viewing product details

Application: https://www.saucedemo.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import e2e_test


@allure.epic("Sauce Demo E2E")
@allure.feature("Inventory")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@e2e_test(
    epic="Sauce Demo E2E",
    feature="Inventory",
    story="View Products",
    testcase="TC-SD-010",
    requirement="US-INV-001",
    app="sauce_demo",
    severity=allure.severity_level.CRITICAL,
    critical=True,
    smoke=True,
    title="View all products",
    link="https://www.saucedemo.com/",
    description="""
    Verify that all products are displayed correctly on the inventory page.

    **Test Steps:**
    1. Login to the application
    2. Navigate to inventory page
    3. Verify all 6 products are displayed
    4. Verify each product has name and price

    **Test Coverage:**
    - Product list display
    - Product data completeness
    - Price data validation

    **Business Value:**
    Core user journey for browsing available products.
    """,
)
def test_view_all_products(login_page, inventory_page, sauce_demo_config):
    """TC-SD-010: View all products on inventory page."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Login and navigate to inventory"):
        login_page.attach()
        login_page.login(user["username"], user["password"])

    with allure.step("Verify 6 products displayed"):
        assert inventory_page.get_product_count() == 6

    with allure.step("Verify all products have names and prices"):
        names = inventory_page.get_item_names()
        prices = inventory_page.get_item_prices()
        assert len(names) == 6
        assert len(prices) == 6
        assert all(name for name in names)
        assert all(price > 0 for price in prices)


@allure.epic("Sauce Demo E2E")
@allure.feature("Inventory")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@e2e_test(
    epic="Sauce Demo E2E",
    feature="Inventory",
    story="Sort Products",
    testcase="TC-SD-011",
    requirement="US-INV-002",
    app="sauce_demo",
    severity=allure.severity_level.NORMAL,
    title="Sort by price (low to high)",
    link="https://www.saucedemo.com/",
    description="""
    Verify that products can be sorted by price (low to high).

    **Test Steps:**
    1. Login to the application
    2. Select sort option "Price (low to high)"
    3. Verify products are sorted correctly

    **Test Coverage:**
    - Price sorting functionality
    - Sort order validation

    **Business Value:**
    Enables users to find products by price range.
    """,
)
def test_sort_by_price_low_to_high(login_page, inventory_page, sauce_demo_config):
    """TC-SD-011: Sort products by price (low to high)."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Login and navigate to inventory"):
        login_page.attach()
        login_page.login(user["username"], user["password"])

    with allure.step("Sort products by price (low to high)"):
        inventory_page.sort_products("lohi")

    with allure.step("Verify prices are sorted ascending"):
        prices = inventory_page.get_item_prices()
        assert prices == sorted(prices)
        assert prices[0] == 7.99  # Lowest price item


@allure.epic("Sauce Demo E2E")
@allure.feature("Inventory")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@e2e_test(
    epic="Sauce Demo E2E",
    feature="Inventory",
    story="Sort Products",
    testcase="TC-SD-012",
    requirement="US-INV-003",
    app="sauce_demo",
    severity=allure.severity_level.NORMAL,
    title="Sort by name (Z to A)",
    link="https://www.saucedemo.com/",
    description="""
    Verify that products can be sorted by name (Z to A).

    **Test Steps:**
    1. Login to the application
    2. Select sort option "Name (Z to A)"
    3. Verify products are sorted correctly

    **Test Coverage:**
    - Name sorting functionality
    - Sort order validation

    **Business Value:**
    Enables users to find products alphabetically.
    """,
)
def test_sort_by_name_z_to_a(login_page, inventory_page, sauce_demo_config):
    """TC-SD-012: Sort products by name (Z to A)."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Login and navigate to inventory"):
        login_page.attach()
        login_page.login(user["username"], user["password"])

    with allure.step("Sort products by name (Z to A)"):
        inventory_page.sort_products("za")

    with allure.step("Verify names are sorted descending"):
        names = inventory_page.get_item_names()
        assert names == sorted(names, reverse=True)


@allure.epic("Sauce Demo E2E")
@allure.feature("Shopping Cart")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@e2e_test(
    epic="Sauce Demo E2E",
    feature="Shopping Cart",
    story="Add to Cart",
    testcase="TC-SD-013",
    requirement="US-CART-001",
    app="sauce_demo",
    severity=allure.severity_level.CRITICAL,
    critical=True,
    smoke=True,
    title="Add product to cart",
    link="https://www.saucedemo.com/",
    description="""
    Verify that a product can be added to the cart.

    **Test Steps:**
    1. Login to the application
    2. Click "Add to cart" on a product
    3. Verify button changes to "Remove"
    4. Verify cart badge updates

    **Test Coverage:**
    - Add to cart functionality
    - Cart counter update
    - Button state change

    **Business Value:**
    Core functionality for adding items to shopping cart.
    """,
)
def test_add_product_to_cart(login_page, inventory_page, sauce_demo_config):
    """TC-SD-013: Add product to cart."""
    user = sauce_demo_config.test_users["standard"]
    product_name = "Sauce Labs Backpack"

    with allure.step("Login and navigate to inventory"):
        login_page.attach()
        login_page.login(user["username"], user["password"])

    with allure.step(f"Add '{product_name}' to cart"):
        inventory_page.add_to_cart(product_name)

    with allure.step("Verify button changed to Remove"):
        assert inventory_page.is_in_cart(product_name)

    with allure.step("Verify cart badge shows 1"):
        assert inventory_page.get_cart_count() == 1


@allure.epic("Sauce Demo E2E")
@allure.feature("Product Details")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@e2e_test(
    epic="Sauce Demo E2E",
    feature="Product Details",
    story="View Product Details",
    testcase="TC-SD-014",
    requirement="US-INV-004",
    app="sauce_demo",
    severity=allure.severity_level.NORMAL,
    title="View product details",
    link="https://www.saucedemo.com/",
    description="""
    Verify that product details can be viewed.

    **Test Steps:**
    1. Login to the application
    2. Click on a product name/image
    3. Verify navigation to product detail page
    4. Verify product details are displayed

    **Test Coverage:**
    - Product detail page navigation
    - Product information display

    **Business Value:**
    Enables users to view detailed product information.
    """,
)
def test_view_product_details(login_page, inventory_page, sauce_demo_config):
    """TC-SD-014: View product details page."""
    user = sauce_demo_config.test_users["standard"]
    product_name = "Sauce Labs Backpack"

    with allure.step("Login and navigate to inventory"):
        login_page.attach()
        login_page.login(user["username"], user["password"])

    with allure.step(f"Click on '{product_name}'"):
        inventory_page.click_product(product_name)

    with allure.step("Verify navigated to product detail page"):
        expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory-item.html?id=4")

    with allure.step("Verify product name is visible"):
        expect(inventory_page.page.locator('.inventory_details_name')).to_contain_text(product_name)
