"""Sauce Demo Navigation Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("Sauce Demo")
@allure.story("Navigation")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
def test_logout(login_page, inventory_page, sauce_demo_config):
    """TC-SD-040: Logout functionality."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Open hamburger menu
    menu_button = inventory_page.page.locator('#react-burger-menu-btn')
    menu_button.click()
    
    # Wait for menu to open
    logout_link = inventory_page.page.locator('#logout_sidebar_link')
    logout_link.wait_for(state="visible")
    
    # Click logout
    logout_link.click()
    
    # Verify redirected to login page
    expect(login_page.page).to_have_url("https://www.saucedemo.com/")
    expect(login_page.username_input).to_be_visible()


@allure.feature("Sauce Demo")
@allure.story("Navigation")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
def test_reset_app_state(login_page, inventory_page, sauce_demo_config):
    """TC-SD-041: Reset app state clears cart."""
    # Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Add items to cart
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.add_to_cart("Sauce Labs Bike Light")
    
    # Verify cart has items
    assert inventory_page.get_cart_count() == 2
    
    # Open menu and reset app state
    menu_button = inventory_page.page.locator('#react-burger-menu-btn')
    menu_button.click()
    
    reset_link = inventory_page.page.locator('#reset_sidebar_link')
    reset_link.wait_for(state="visible")
    reset_link.click()
    
    # Close menu
    close_button = inventory_page.page.locator('#react-burger-cross-btn')
    close_button.click()
    
    # Wait for menu animation and state reset
    inventory_page.page.wait_for_timeout(1000)
    
    # Reload or navigate to inventory to see fresh state
    inventory_page.page.goto("https://www.saucedemo.com/inventory.html")
    
    # Verify cart is cleared
    assert inventory_page.get_cart_count() == 0
    
    # Verify "Add to cart" buttons are restored
    assert not inventory_page.is_in_cart("Sauce Labs Backpack")
    assert not inventory_page.is_in_cart("Sauce Labs Bike Light")
