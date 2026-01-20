"""Sauce Demo Shopping Cart Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("Sauce Demo")
@allure.story("Shopping Cart")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
def test_add_multiple_products(login_page, inventory_page, sauce_demo_config):
    """TC-SD-020: Add multiple products to cart."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Add 3 products
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    for product in products:
        inventory_page.add_to_cart(product)
    
    # Verify cart badge shows 3
    assert inventory_page.get_cart_count() == 3


@allure.feature("Sauce Demo")
@allure.story("Shopping Cart")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.critical
def test_view_cart_contents(login_page, inventory_page, cart_page, sauce_demo_config):
    """TC-SD-021: View cart contents."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Add products
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    for product in products:
        inventory_page.add_to_cart(product)
    
    # Go to cart
    inventory_page.go_to_cart()
    
    # Verify products in cart
    cart_items = cart_page.get_item_names()
    assert len(cart_items) == 2
    for product in products:
        assert product in cart_items


@allure.feature("Sauce Demo")
@allure.story("Shopping Cart")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
def test_remove_product_from_cart(login_page, inventory_page, cart_page, sauce_demo_config):
    """TC-SD-022: Remove product from cart."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Add products
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    for product in products:
        inventory_page.add_to_cart(product)
    
    # Go to cart
    inventory_page.go_to_cart()
    
    # Remove one item
    cart_page.remove_item("Sauce Labs Backpack")
    
    # Verify only 1 item remains
    assert cart_page.get_item_count() == 1
    
    # Verify correct item removed
    cart_items = cart_page.get_item_names()
    assert "Sauce Labs Bike Light" in cart_items
    assert "Sauce Labs Backpack" not in cart_items


@allure.feature("Sauce Demo")
@allure.story("Shopping Cart")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
def test_continue_shopping(login_page, inventory_page, cart_page, sauce_demo_config):
    """TC-SD-023: Continue shopping from cart."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Add product and go to cart
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.go_to_cart()
    
    # Continue shopping
    cart_page.continue_shopping()
    
    # Verify back on inventory page
    expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(inventory_page.inventory_list).to_be_visible()
