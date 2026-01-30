"""Medusa Checkout Page."""

from playwright.sync_api import Page
import allure
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page object for Checkout steps."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Inputs
        # fallback to semantic selectors if testids are flaky
        self.first_name = self.page.locator('input[name="shipping_address.first_name"], [data-testid="shipping-first-name-input"]')
        self.last_name = self.page.locator('input[name="shipping_address.last_name"], [data-testid="shipping-last-name-input"]')
        self.address = self.page.locator('input[name="shipping_address.address_1"], [data-testid="shipping-address-input"]')
        self.postal_code = self.page.locator('input[name="shipping_address.postal_code"], [data-testid="shipping-postal-code-input"]')
        self.city = self.page.locator('input[name="shipping_address.city"], [data-testid="shipping-city-input"]')
        self.state = self.page.locator('input[name="shipping_address.province"], [data-testid="shipping-province-input"]')
        self.country_select = self.page.locator('select[name="shipping_address.country_code"], [data-testid="shipping-country-select"]')
        self.email = self.page.locator('input[type="email"], [data-testid="email-input"]')
        self.phone = self.page.locator('input[name="shipping_address.phone"], [data-testid="shipping-phone-input"]')

        # Buttons
        self.submit_address_button = self.page.locator('[data-testid="submit-address-button"]')
        self.submit_delivery_button = self.page.locator('[data-testid="submit-delivery-option-button"]')
        self.submit_payment_button = self.page.locator('[data-testid="submit-payment-button"]')
        self.place_order_button = self.page.locator('[data-testid="submit-order-button"]')
        
        # Options
        self.manual_payment_radio = self.page.locator('[data-testid="radio-button-manual"]') # Assuming ID or testid for manual payment

    @allure.step("Fill shipping address")
    def fill_shipping(self, data: dict):
        """Fill shipping details."""
        # Wait for form to be ready
        self.first_name.wait_for(state="visible")
        
        # Select country FIRST (required before other fields)
        self.country_select.wait_for(state="visible")
        self.country_select.select_option("us")  # US country code
        
        # Fill form fields
        self.first_name.fill(data["first_name"])
        self.last_name.fill(data["last_name"])
        self.address.fill(data["address"])
        self.postal_code.fill(data["postal_code"])
        self.city.fill(data["city"])
        self.state.fill(data.get("state", "NY"))
        self.email.fill(data["email"])
        self.phone.fill(data.get("phone", "1234567890"))
        
        # Click continue button using text (more stable than testid)
        self.page.get_by_role("button", name="Continue to delivery").click()
        
        # Wait for delivery section to load
        self.page.wait_for_timeout(1500)

    @allure.step("Select delivery")
    def select_delivery(self):
        """Select default delivery and continue."""
        # Wait for delivery options to appear
        delivery_options = self.page.locator('[role="radio"]', has_text="Standard shipping")
        delivery_options.first.wait_for(state="visible")
        delivery_options.first.click()
        
        # Wait for button to become enabled after selection
        continue_button = self.page.get_by_role("button", name="Continue to payment")
        continue_button.wait_for(state="visible")
        # Extra wait for enabled state (button starts disabled)
        self.page.wait_for_timeout(500)
        continue_button.click()

    @allure.step("Select payment")
    def select_payment(self):
        """Select manual payment and continue."""
        # Wait for payment section
        payment_option = self.page.get_by_text("Manual Payment")
        payment_option.wait_for(state="visible")
        payment_option.click()
        
        # Continue button
        continue_button = self.page.get_by_role("button", name="Continue to review")
        continue_button.wait_for(state="visible")
        self.page.wait_for_timeout(500)
        continue_button.click()

    @allure.step("Place order")
    def place_order(self):
        """Click place order."""
        place_order_btn = self.page.get_by_role("button", name="Place order")
        place_order_btn.wait_for(state="visible")
        self.page.wait_for_timeout(500)
        place_order_btn.click()

    @allure.step("Verify confirmation")
    def verify_confirmation(self) -> str:
        """Return confirmation text or order ID."""
        return self.page.locator('[data-testid="order-id"]').inner_text()
