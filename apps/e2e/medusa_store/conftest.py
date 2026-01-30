"""Medusa Store E2E Fixtures."""

import pytest
from playwright.sync_api import Page

from apps.e2e.medusa_store.pages.store_page import StorePage
from apps.e2e.medusa_store.pages.product_page import ProductPage
from apps.e2e.medusa_store.pages.cart_page import CartPage
from apps.e2e.medusa_store.pages.checkout_page import CheckoutPage


@pytest.fixture(scope="session")
def medusa_store_config(app_configs):
    """Get Medusa Store configuration."""
    config = app_configs.get("medusa_store")
    if not config:
        pytest.skip("Medusa Store not configured")
    return config


@pytest.fixture
def store_page(page: Page) -> StorePage:
    return StorePage(page)


@pytest.fixture
def product_page(page: Page) -> ProductPage:
    return ProductPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)
