"""Sauce Demo Checkout Validation Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("Sauce Demo")
@allure.story("Checkout Validation")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-031")
def test_checkout_empty_fields(
    login_page,
    inventory_page,
    cart_page,
    checkout_step_one_page,
    sauce_demo_config
):
    """TC-SD-031: Checkout validation with empty fields."""
    # Login and add item
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    inventory_page.add_to_cart("Sauce Labs Backpack")
    
    # Go to checkout
    inventory_page.go_to_cart()
    cart_page.checkout()
    
    # Try to continue with empty fields
    checkout_step_one_page.fill_info("", "", "")
    
    # Verify error message
    error = checkout_step_one_page.get_error_message()
    assert "First Name is required" in error


@allure.feature("Sauce Demo")
@allure.story("Checkout Validation")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.critical
@pytest.mark.testcase("TC-SD-032")
def test_verify_order_total(
    login_page,
    inventory_page,
    cart_page,
    checkout_step_one_page,
    checkout_step_two_page,
    sauce_demo_config
):
    """TC-SD-032: Verify order total calculation."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Add specific products (prices known)
    inventory_page.add_to_cart("Sauce Labs Backpack")  # $29.99
    inventory_page.add_to_cart("Sauce Labs Bike Light")  # $9.99
    
    # Checkout
    inventory_page.go_to_cart()
    cart_page.checkout()
    checkout_step_one_page.fill_info("Test", "User", "12345")
    
    # Verify totals on overview page
    subtotal = checkout_step_two_page.get_subtotal()
    assert subtotal == 39.98
    
    total = checkout_step_two_page.get_total()
    # Tax should be calculated (around 8%)
    assert total > subtotal
    assert total < subtotal * 1.10  # Reasonable tax range


@allure.feature("Sauce Demo")
@allure.story("Checkout Validation")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-033")
def test_cancel_checkout(
    login_page,
    inventory_page,
    cart_page,
    checkout_step_one_page,
    sauce_demo_config
):
    """TC-SD-033: Cancel checkout and return to cart."""
    # Login and add item
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    inventory_page.add_to_cart("Sauce Labs Backpack")
    
    # Go to checkout
    inventory_page.go_to_cart()
    cart_page.checkout()
    
    # Cancel
    checkout_step_one_page.cancel()
    
    # Verify back on cart page
    expect(login_page.page).to_have_url("https://www.saucedemo.com/cart.html")
