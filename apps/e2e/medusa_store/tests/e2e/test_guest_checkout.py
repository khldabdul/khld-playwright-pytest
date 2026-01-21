"""Medusa Store Checkout Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("Medusa Store")
@allure.story("Guest Checkout")
@pytest.mark.app("medusa_store")
@pytest.mark.e2e
@pytest.mark.critical
@pytest.mark.testcase("TC-MS-040")
@pytest.mark.smoke
def test_guest_checkout_flow(
    store_page,
    product_page,
    cart_page,
    checkout_page,
    medusa_store_config
):
    """
    Test guest checkout flow: 
    Store -> Product -> Add to Cart -> Cart -> Checkout -> Payment -> Order.
    """
    # 1. Navigate to Store
    store_page.navigate_to_store()
    
    # 2. Select Product
    # Using 'Hoodie' as verified in manual steps
    store_page.select_product("Hoodie")
    
    # 3. Add to Cart
    product_page.add_to_cart()
    # Wait for cart icon to show items (optional visual check) or just click it
    product_page.go_to_cart()
    
    # 4. Proceed to Checkout
    cart_page.checkout()
    
    # 5. Fill Shipping Info
    checkout_data = medusa_store_config.extra_config["test_checkout"]
    checkout_page.fill_shipping(checkout_data)
    
    # 6. Select Delivery
    checkout_page.select_delivery()
    
    # 7. Select Payment
    checkout_page.select_payment()
    
    # 8. Place Order
    checkout_page.place_order()
    
    # 9. Verify Confirmation
    # The order-id span contains just the number, not "Order #..."
    order_id_element = checkout_page.page.locator('[data-testid="order-id"]')
    expect(order_id_element).to_be_visible()
    order_id = order_id_element.inner_text()
    assert order_id.isdigit(), f"Expected numeric order ID, got: {order_id}"
