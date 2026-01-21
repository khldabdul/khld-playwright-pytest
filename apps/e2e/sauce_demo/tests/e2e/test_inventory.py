"""Sauce Demo Inventory Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("Sauce Demo")
@allure.story("Inventory")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.critical
@pytest.mark.testcase("TC-SD-010")
def test_view_all_products(login_page, inventory_page, sauce_demo_config):
    """TC-SD-010: View all products on inventory page."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Verify 6 products displayed
    assert inventory_page.get_product_count() == 6
    
    # Verify all products have names and prices
    names = inventory_page.get_item_names()
    prices = inventory_page.get_item_prices()
    
    assert len(names) == 6
    assert len(prices) == 6
    assert all(name for name in names)  # No empty names
    assert all(price > 0 for price in prices)  # All prices positive


@allure.feature("Sauce Demo")
@allure.story("Inventory")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-011")
def test_sort_by_price_low_to_high(login_page, inventory_page, sauce_demo_config):
    """TC-SD-011: Sort products by price (low to high)."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Sort by price low to high
    inventory_page.sort_products("lohi")
    
    # Verify prices are sorted ascending
    prices = inventory_page.get_item_prices()
    assert prices == sorted(prices)
    assert prices[0] == 7.99  # Lowest price item


@allure.feature("Sauce Demo")
@allure.story("Inventory")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-012")
def test_sort_by_name_z_to_a(login_page, inventory_page, sauce_demo_config):
    """TC-SD-012: Sort products by name (Z to A)."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Sort by name Z to A
    inventory_page.sort_products("za")
    
    # Verify names are sorted descending
    names = inventory_page.get_item_names()
    assert names == sorted(names, reverse=True)


@allure.feature("Sauce Demo")
@allure.story("Inventory")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.critical
@pytest.mark.testcase("TC-SD-013")
@pytest.mark.smoke
def test_add_product_to_cart(login_page, inventory_page, sauce_demo_config):
    """TC-SD-013: Add product to cart."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Add product
    product_name = "Sauce Labs Backpack"
    inventory_page.add_to_cart(product_name)
    
    # Verify button changed to Remove
    assert inventory_page.is_in_cart(product_name)
    
    # Verify cart badge shows 1
    assert inventory_page.get_cart_count() == 1


@allure.feature("Sauce Demo")
@allure.story("Inventory")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-014")
def test_view_product_details(login_page, inventory_page, sauce_demo_config):
    """TC-SD-014: View product details page."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Click on product
    product_name = "Sauce Labs Backpack"
    inventory_page.click_product(product_name)
    
    # Verify navigated to product detail page
    expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory-item.html?id=4")
    
    # Verify product name is visible
    expect(inventory_page.page.locator('.inventory_details_name')).to_contain_text(product_name)
