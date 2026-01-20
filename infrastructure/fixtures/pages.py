"""Page object fixtures factory."""

import pytest
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.fixture
def base_page(page: Page) -> BasePage:
    """
    Provide BasePage instance.

    This is a generic page object for common operations.
    """
    return BasePage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """
    Provide LoginPage instance.

    Use for tests that need to interact with login functionality.
    """
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page: Page) -> DashboardPage:
    """
    Provide DashboardPage instance.

    Use for tests that need to interact with dashboard functionality.
    """
    return DashboardPage(page)
