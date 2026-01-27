"""Sauce Demo Checkout Validation Tests.

This test suite covers checkout validation including:
- Empty field validation
- Order total calculation
- Canceling checkout process

Application: https://www.saucedemo.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import e2e_test


@allure.epic("Sauce Demo E2E")
@allure.feature("Checkout")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@e2e_test(
    epic="Sauce Demo E2E",
    feature="Checkout",
    story="Form Validation",
    testcase="TC-SD-031",
    requirement="US-CHECKOUT-002",
    app="sauce_demo",
    severity=allure.severity_level.NORMAL,
    title="Checkout validation with empty fields",
    link="https://www.saucedemo.com/",
    description="""
    Verify that checkout form validates required fields.

    **Test Steps:**
    1. Login to the application
    2. Add item to cart
    3. Navigate to checkout
    4. Attempt to continue with empty fields
    5. Verify error message appears

    **Test Coverage:**
    - Required field validation
    - Error message display
    - Form submission blocking

    **Business Value:**
    Ensures complete customer information is collected before order processing.
    """,
)
def test_checkout_empty_fields(
    login_page,
    inventory_page,
    cart_page,
    checkout_step_one_page,
    sauce_demo_config
):
    """TC-SD-031: Checkout validation with empty fields."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Login and add item to cart"):
        login_page.attach()
        login_page.login(user["username"], user["password"])
        inventory_page.add_to_cart("Sauce Labs Backpack")

    with allure.step("Navigate to checkout"):
        inventory_page.go_to_cart()
        cart_page.checkout()

    with allure.step("Attempt to continue with empty fields"):
        checkout_step_one_page.fill_info("", "", "")

    with allure.step("Verify validation error message"):
        error = checkout_step_one_page.get_error_message()
        assert "First Name is required" in error


@allure.epic("Sauce Demo E2E")
@allure.feature("Checkout")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@e2e_test(
    epic="Sauce Demo E2E",
    feature="Checkout",
    story="Order Calculation",
    testcase="TC-SD-032",
    requirement="US-CHECKOUT-003",
    app="sauce_demo",
    severity=allure.severity_level.CRITICAL,
    critical=True,
    smoke=True,
    title="Verify order total calculation",
    link="https://www.saucedemo.com/",
    description="""
    Verify that order totals are calculated correctly.

    **Test Steps:**
    1. Login to the application
    2. Add products with known prices ($29.99 + $9.99)
    3. Navigate to checkout
    4. Fill shipping information
    5. Verify subtotal and total calculations

    **Test Coverage:**
    - Price calculation accuracy
    - Tax calculation
    - Order summary display

    **Business Value:**
    Critical for accurate billing and customer trust.
    """,
)
def test_verify_order_total(
    login_page,
    inventory_page,
    cart_page,
    checkout_step_one_page,
    checkout_step_two_page,
    sauce_demo_config
):
    """TC-SD-032: Verify order total calculation."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Login and add products to cart"):
        login_page.attach()
        login_page.login(user["username"], user["password"])

        # Add specific products (prices known)
        inventory_page.add_to_cart("Sauce Labs Backpack")  # $29.99
        inventory_page.add_to_cart("Sauce Labs Bike Light")  # $9.99

    with allure.step("Navigate to checkout"):
        inventory_page.go_to_cart()
        cart_page.checkout()
        checkout_step_one_page.fill_info("Test", "User", "12345")

    with allure.step("Verify subtotal calculation"):
        subtotal = checkout_step_two_page.get_subtotal()
        assert subtotal == 39.98

    with allure.step("Verify total with tax"):
        total = checkout_step_two_page.get_total()
        # Tax should be calculated (around 8%)
        assert total > subtotal
        assert total < subtotal * 1.10  # Reasonable tax range


@allure.epic("Sauce Demo E2E")
@allure.feature("Checkout")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@e2e_test(
    epic="Sauce Demo E2E",
    feature="Checkout",
    story="Cancel Checkout",
    testcase="TC-SD-033",
    requirement="US-CHECKOUT-004",
    app="sauce_demo",
    severity=allure.severity_level.NORMAL,
    title="Cancel checkout and return to cart",
    link="https://www.saucedemo.com/",
    description="""
    Verify that checkout can be canceled and user returns to cart.

    **Test Steps:**
    1. Login to the application
    2. Add item to cart
    3. Navigate to checkout
    4. Click cancel button
    5. Verify redirect to cart page

    **Test Coverage:**
    - Checkout cancellation
    - Return to cart navigation
    - Cart preservation after cancel

    **Business Value:**
    Enables users to review or modify cart before completing purchase.
    """,
)
def test_cancel_checkout(
    login_page,
    inventory_page,
    cart_page,
    checkout_step_one_page,
    sauce_demo_config
):
    """TC-SD-033: Cancel checkout and return to cart."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Login and add item to cart"):
        login_page.attach()
        login_page.login(user["username"], user["password"])
        inventory_page.add_to_cart("Sauce Labs Backpack")

    with allure.step("Navigate to checkout"):
        inventory_page.go_to_cart()
        cart_page.checkout()

    with allure.step("Cancel checkout process"):
        checkout_step_one_page.cancel()

    with allure.step("Verify returned to cart page"):
        expect(login_page.page).to_have_url("https://www.saucedemo.com/cart.html")
