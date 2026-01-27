"""Sauce Demo Checkout Tests.

This test suite covers the complete checkout flow including:
- Adding items to cart
- Filling checkout information
- Completing the purchase

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
    story="Complete Purchase",
    testcase="TC-SD-030",
    requirement="US-CHECKOUT-001",
    app="sauce_demo",
    severity=allure.severity_level.CRITICAL,
    critical=True,
    smoke=True,
    title="Complete checkout flow",
    link="https://www.saucedemo.com/",
    description="""
    Verify that a user can complete the full checkout flow.

    **Test Steps:**
    1. Login to the application
    2. Add item to cart
    3. Navigate to cart
    4. Start checkout process
    5. Fill shipping information
    6. Review order on overview page
    7. Complete purchase
    8. Verify order completion

    **Test Coverage:**
    - End-to-end purchase flow
    - Checkout form submission
    - Order summary display
    - Purchase completion

    **Business Value:**
    Core revenue-generating user journey for completing purchases.
    """,
)
def test_complete_checkout_flow(
    login_page,
    inventory_page,
    cart_page,
    checkout_step_one_page,
    checkout_step_two_page,
    checkout_complete_page,
    sauce_demo_config
):
    """TC-SD-030: Test complete checkout flow: Login -> Add Item -> Cart -> Checkout -> Finish."""
    user = sauce_demo_config.test_users["standard"]
    product_name = "Sauce Labs Backpack"

    with allure.step("Login to the application"):
        login_page.attach()
        login_page.login(user["username"], user["password"])
        expect(inventory_page.shopping_cart_link).to_be_visible()

    with allure.step(f"Add '{product_name}' to cart"):
        inventory_page.add_to_cart(product_name)
        expect(inventory_page.shopping_cart_badge).to_have_text("1")

    with allure.step("Navigate to cart and verify item"):
        inventory_page.go_to_cart()
        names = cart_page.get_item_names()
        assert product_name in names

    with allure.step("Start checkout process"):
        cart_page.checkout()

    with allure.step("Fill shipping information"):
        checkout_step_one_page.fill_info(
            first_name="Test",
            last_name="User",
            postal_code="12345"
        )

    with allure.step("Verify order overview and complete purchase"):
        expect(checkout_step_two_page.subtotal_label).to_contain_text("Item total: $")
        checkout_step_two_page.finish()

    with allure.step("Verify order completion message"):
        header = checkout_complete_page.get_header()
        assert header == "Thank you for your order!"
        expect(checkout_complete_page.back_home_button).to_be_visible()
