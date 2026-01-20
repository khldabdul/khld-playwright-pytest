"""Pages package for Page Object Model."""

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

__all__ = ["BasePage", "LoginPage", "DashboardPage"]
