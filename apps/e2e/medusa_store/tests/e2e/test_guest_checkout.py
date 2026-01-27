"""Medusa Store - Guest Checkout Tests.

This test suite covers guest checkout flow including:
- Product selection
- Adding to cart
- Checkout process
- Order placement

Application: Medusa Store E-commerce Demo
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import e2e_test


@e2e_test(
    epic="Medusa Store E2E",
    feature="Checkout",
    story="Guest Checkout",
    title="TC-MS-040: Complete guest checkout flow",
    description="""Verify complete guest checkout flow.

**Test Steps:**
1. Navigate to store
2. Select product (Hoodie)
3. Add product to cart
4. Navigate to cart
5. Proceed to checkout
6. Fill shipping information
7. Select delivery option
8. Select payment option
9. Place order
10. Verify order confirmation with order ID

**Test Coverage:**
- End-to-end guest checkout
- Shipping form handling
- Delivery and payment selection
- Order confirmation

**Business Value:**
Core revenue-generating user journey for completing purchases.
""",
    testcase="TC-MS-040",
    requirement="US-MS-CHECKOUT-001",
    app="medusa_store",
    severity="critical",
    link="https://demo.medusa-commerce.com/",
    smoke=True,
    critical=True
)
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
    product_name = "Hoodie"
    checkout_data = medusa_store_config.extra_config["test_checkout"]

    with allure.step("Navigate to store"):
        store_page.navigate_to_store()

    with allure.step(f"Select product '{product_name}'"):
        store_page.select_product(product_name)

    with allure.step("Add product to cart and navigate to cart"):
        product_page.add_to_cart()
        product_page.go_to_cart()

    with allure.step("Proceed to checkout"):
        cart_page.checkout()

    with allure.step("Fill shipping information"):
        checkout_page.fill_shipping(checkout_data)

    with allure.step("Select delivery option"):
        checkout_page.select_delivery()

    with allure.step("Select payment option"):
        checkout_page.select_payment()

    with allure.step("Place order"):
        checkout_page.place_order()

    with allure.step("Verify order confirmation with numeric order ID"):
        order_id_element = checkout_page.page.locator('[data-testid="order-id"]')
        expect(order_id_element).to_be_visible()
        order_id = order_id_element.inner_text()
        assert order_id.isdigit(), f"Expected numeric order ID, got: {order_id}"
