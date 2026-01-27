"""Sauce Demo Navigation Tests.

This test suite covers application navigation operations including:
- User logout
- Reset application state

Application: https://www.saucedemo.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import e2e_test


@e2e_test(
    epic="Sauce Demo E2E",
    feature="Navigation",
    story="Session Management",
    testcase="TC-SD-040",
    requirement="US-NAV-001",
    app="sauce_demo",
    severity=allure.severity_level.NORMAL,
    title="User logout",
    link="https://www.saucedemo.com/",
    description="""
    Verify that a user can successfully log out.

    **Test Steps:**
    1. Login to the application
    2. Open hamburger menu
    3. Click logout link
    4. Verify redirect to login page

    **Test Coverage:**
    - User logout functionality
    - Session termination
    - Post-logout redirect verification

    **Business Value:**
    Critical for user session management and security.
    """,
)
def test_logout(login_page, inventory_page, sauce_demo_config):
    """TC-SD-040: Logout functionality."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Login to the application"):
        login_page.attach()
        login_page.login(user["username"], user["password"])

    with allure.step("Open hamburger menu"):
        menu_button = inventory_page.page.locator('#react-burger-menu-btn')
        menu_button.click()

    with allure.step("Click logout link"):
        logout_link = inventory_page.page.locator('#logout_sidebar_link')
        logout_link.wait_for(state="visible")
        logout_link.click()

    with allure.step("Verify redirect to login page"):
        expect(login_page.page).to_have_url("https://www.saucedemo.com/")
        expect(login_page.username_input).to_be_visible()


@e2e_test(
    epic="Sauce Demo E2E",
    feature="Navigation",
    story="State Management",
    testcase="TC-SD-041",
    requirement="US-NAV-002",
    app="sauce_demo",
    severity=allure.severity_level.NORMAL,
    title="Reset app state clears cart",
    link="https://www.saucedemo.com/",
    description="""
    Verify that resetting app state clears the cart.

    **Test Steps:**
    1. Login to the application
    2. Add items to cart
    3. Open hamburger menu
    4. Click reset app state link
    5. Verify cart is cleared

    **Test Coverage:**
    - Application state reset functionality
    - Cart clearing after reset
    - Button state restoration

    **Business Value:**
    Enables users to reset their session and start fresh.
    """,
)
def test_reset_app_state(login_page, inventory_page, sauce_demo_config):
    """TC-SD-041: Reset app state clears cart."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Login and add items to cart"):
        login_page.attach()
        login_page.login(user["username"], user["password"])
        inventory_page.add_to_cart("Sauce Labs Backpack")
        inventory_page.add_to_cart("Sauce Labs Bike Light")

    with allure.step("Verify cart has 2 items"):
        assert inventory_page.get_cart_count() == 2

    with allure.step("Open menu and reset app state"):
        menu_button = inventory_page.page.locator('#react-burger-menu-btn')
        menu_button.click()

        reset_link = inventory_page.page.locator('#reset_sidebar_link')
        reset_link.wait_for(state="visible")
        reset_link.click()

        close_button = inventory_page.page.locator('#react-burger-cross-btn')
        close_button.click()

    with allure.step("Wait for reset to complete"):
        inventory_page.page.wait_for_timeout(1000)
        inventory_page.page.goto("https://www.saucedemo.com/inventory.html")

    with allure.step("Verify cart is cleared and buttons restored"):
        assert inventory_page.get_cart_count() == 0
        assert not inventory_page.is_in_cart("Sauce Labs Backpack")
        assert not inventory_page.is_in_cart("Sauce Labs Bike Light")
