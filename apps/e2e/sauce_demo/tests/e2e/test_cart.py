"""Sauce Demo Shopping Cart Tests.

This test suite covers shopping cart operations including:
- Adding multiple products to cart
- Viewing cart contents
- Removing products from cart
- Continuing shopping from cart

Application: https://www.saucedemo.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import e2e_test


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
    testcase="TC-SD-020",
    requirement="US-CART-002",
    app="sauce_demo",
    severity=allure.severity_level.NORMAL,
    title="Add multiple products to cart",
    link="https://www.saucedemo.com/",
    description="""
    Verify that multiple products can be added to the cart.

    **Test Steps:**
    1. Login to the application
    2. Add 3 products to cart
    3. Verify cart badge shows correct count

    **Test Coverage:**
    - Multiple item addition
    - Cart counter accuracy
    - Button state changes

    **Business Value:**
    Enables users to add multiple items to cart for bulk purchases.
    """,
)
def test_add_multiple_products(login_page, inventory_page, sauce_demo_config):
    """TC-SD-020: Add multiple products to cart."""
    user = sauce_demo_config.test_users["standard"]
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]

    with allure.step("Login and navigate to inventory"):
        login_page.attach()
        login_page.login(user["username"], user["password"])

    with allure.step("Add 3 products to cart"):
        for product in products:
            inventory_page.add_to_cart(product)

    with allure.step("Verify cart badge shows 3"):
        assert inventory_page.get_cart_count() == 3


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
    story="View Cart",
    testcase="TC-SD-021",
    requirement="US-CART-003",
    app="sauce_demo",
    severity=allure.severity_level.CRITICAL,
    critical=True,
    smoke=True,
    title="View cart contents",
    link="https://www.saucedemo.com/",
    description="""
    Verify that cart contents are displayed correctly.

    **Test Steps:**
    1. Login to the application
    2. Add 2 products to cart
    3. Navigate to cart page
    4. Verify all products are displayed

    **Test Coverage:**
    - Cart page navigation
    - Product display in cart
    - Cart data accuracy

    **Business Value:**
    Core functionality for reviewing selected items before checkout.
    """,
)
def test_view_cart_contents(login_page, inventory_page, cart_page, sauce_demo_config):
    """TC-SD-021: View cart contents."""
    user = sauce_demo_config.test_users["standard"]
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]

    with allure.step("Login and navigate to inventory"):
        login_page.attach()
        login_page.login(user["username"], user["password"])

    with allure.step("Add 2 products to cart"):
        for product in products:
            inventory_page.add_to_cart(product)

    with allure.step("Navigate to cart page"):
        inventory_page.go_to_cart()

    with allure.step("Verify all products are displayed"):
        cart_items = cart_page.get_item_names()
        assert len(cart_items) == 2
        for product in products:
            assert product in cart_items


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
    story="Remove from Cart",
    testcase="TC-SD-022",
    requirement="US-CART-004",
    app="sauce_demo",
    severity=allure.severity_level.NORMAL,
    title="Remove product from cart",
    link="https://www.saucedemo.com/",
    description="""
    Verify that products can be removed from the cart.

    **Test Steps:**
    1. Login to the application
    2. Add 2 products to cart
    3. Navigate to cart page
    4. Remove one product
    5. Verify cart updates correctly

    **Test Coverage:**
    - Product removal functionality
    - Cart counter update after removal
    - Cart data integrity

    **Business Value:**
    Enables users to remove unwanted items from cart.
    """,
)
def test_remove_product_from_cart(login_page, inventory_page, cart_page, sauce_demo_config):
    """TC-SD-022: Remove product from cart."""
    user = sauce_demo_config.test_users["standard"]
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]

    with allure.step("Login and add products to cart"):
        login_page.attach()
        login_page.login(user["username"], user["password"])
        for product in products:
            inventory_page.add_to_cart(product)

    with allure.step("Navigate to cart page"):
        inventory_page.go_to_cart()

    with allure.step("Remove 'Sauce Labs Backpack' from cart"):
        cart_page.remove_item("Sauce Labs Backpack")

    with allure.step("Verify only 1 item remains"):
        assert cart_page.get_item_count() == 1

    with allure.step("Verify correct item was removed"):
        cart_items = cart_page.get_item_names()
        assert "Sauce Labs Bike Light" in cart_items
        assert "Sauce Labs Backpack" not in cart_items


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
    story="Continue Shopping",
    testcase="TC-SD-023",
    requirement="US-CART-005",
    app="sauce_demo",
    severity=allure.severity_level.NORMAL,
    title="Continue shopping from cart",
    link="https://www.saucedemo.com/",
    description="""
    Verify that user can continue shopping from cart.

    **Test Steps:**
    1. Login to the application
    2. Add product to cart
    3. Navigate to cart page
    4. Click continue shopping
    5. Verify redirect to inventory page

    **Test Coverage:**
    - Continue shopping navigation
    - Cart to inventory redirect
    - Shopping flow continuity

    **Business Value:**
    Enables users to easily return to shopping from cart view.
    """,
)
def test_continue_shopping(login_page, inventory_page, cart_page, sauce_demo_config):
    """TC-SD-023: Continue shopping from cart."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Login and add product to cart"):
        login_page.attach()
        login_page.login(user["username"], user["password"])
        inventory_page.add_to_cart("Sauce Labs Backpack")

    with allure.step("Navigate to cart page"):
        inventory_page.go_to_cart()

    with allure.step("Click continue shopping"):
        cart_page.continue_shopping()

    with allure.step("Verify back on inventory page"):
        expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(inventory_page.inventory_list).to_be_visible()
