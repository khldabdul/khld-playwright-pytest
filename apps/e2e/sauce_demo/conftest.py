"""Sauce Demo E2E Fixtures."""

import pytest
from playwright.sync_api import Page

from apps.e2e.sauce_demo.pages.login_page import LoginPage
from apps.e2e.sauce_demo.pages.inventory_page import InventoryPage
from apps.e2e.sauce_demo.pages.cart_page import CartPage
from apps.e2e.sauce_demo.pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage


@pytest.fixture(scope="session")
def sauce_demo_config(app_configs):
    """Get Sauce Demo configuration."""
    config = app_configs.get("sauce_demo")
    if not config:
        pytest.skip("Sauce Demo not configured")
    return config


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_step_one_page(page: Page) -> CheckoutStepOnePage:
    return CheckoutStepOnePage(page)


@pytest.fixture
def checkout_step_two_page(page: Page) -> CheckoutStepTwoPage:
    return CheckoutStepTwoPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)
