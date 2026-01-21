"""Sauce Demo Authentication Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("Sauce Demo")
@allure.story("Authentication")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.critical
@pytest.mark.testcase("TC-SD-001")
@pytest.mark.smoke
def test_successful_login(login_page, inventory_page, sauce_demo_config):
    """TC-SD-001: Successful login with valid credentials."""
    # Navigate
    login_page.attach()
    
    # Login
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Verify redirect to inventory
    expect(inventory_page.inventory_list).to_be_visible()
    expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")


@allure.feature("Sauce Demo")
@allure.story("Authentication")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-002")
def test_invalid_password(login_page, sauce_demo_config):
    """TC-SD-002: Login fails with invalid password."""
    # Navigate
    login_page.attach()
    
    # Attempt login with wrong password
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], "wrong_password")
    
    # Verify error message
    error = login_page.get_error_message()
    assert "Username and password do not match" in error


@allure.feature("Sauce Demo")
@allure.story("Authentication")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-003")
def test_locked_out_user(login_page, sauce_demo_config):
    """TC-SD-003: Locked out user cannot login."""
    # Navigate
    login_page.attach()
    
    # Attempt login with locked user
    user = sauce_demo_config.test_users["locked"]
    login_page.login(user["username"], user["password"])
    
    # Verify error message
    error = login_page.get_error_message()
    assert "Sorry, this user has been locked out" in error


@allure.feature("Sauce Demo")
@allure.story("Authentication")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-004")
def test_empty_credentials(login_page):
    """TC-SD-004: Login fails with empty credentials."""
    # Navigate
    login_page.attach()
    
    # Attempt login with empty fields
    login_page.login("", "")
    
    # Verify error message
    error = login_page.get_error_message()
    assert "Username is required" in error
