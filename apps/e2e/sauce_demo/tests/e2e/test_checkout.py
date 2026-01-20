"""Sauce Demo Checkout Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("Sauce Demo")
@allure.story("Checkout")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.critical
def test_complete_checkout_flow(
    login_page,
    inventory_page,
    cart_page,
    checkout_step_one_page,
    checkout_step_two_page,
    checkout_complete_page,
    sauce_demo_config
):
    """
    Test complete checkout flow: Login -> Add Item -> Cart -> Checkout -> Finish.
    """
    # 1. Login
    login_page.attach()
    user = sauce_demo_config.test_users["standard"]
    login_page.login(user["username"], user["password"])
    
    # Verify login success
    expect(inventory_page.shopping_cart_link).to_be_visible()
    
    # 2. Add item to cart
    product_name = "Sauce Labs Backpack"
    inventory_page.add_to_cart(product_name)
    expect(inventory_page.shopping_cart_badge).to_have_text("1")
    
    # 3. Go to cart
    inventory_page.go_to_cart()
    names = cart_page.get_item_names()
    assert product_name in names
    
    # 4. Checkout
    cart_page.checkout()
    
    # 5. Fill info
    checkout_step_one_page.fill_info(
        first_name="Test",
        last_name="User",
        postal_code="12345"
    )
    
    # 6. Overview
    expect(checkout_step_two_page.subtotal_label).to_contain_text("Item total: $")
    checkout_step_two_page.finish()
    
    # 7. Complete
    header = checkout_complete_page.get_header()
    assert header == "Thank you for your order!"
    expect(checkout_complete_page.back_home_button).to_be_visible()
