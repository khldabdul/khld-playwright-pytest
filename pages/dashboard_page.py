"""Dashboard Page Object."""

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Page Object for Dashboard page."""

    # Default Locators (can be overridden per app)
    DASHBOARD_CONTAINER = "[data-testid='dashboard'], .dashboard, #dashboard"
    WELCOME_MESSAGE = "[data-testid='welcome-message'], .welcome-message, h1"
    USER_MENU = "[data-testid='user-menu'], .user-menu, #user-dropdown"
    LOGOUT_BUTTON = "[data-testid='logout'], a[href*='logout'], button:has-text('Logout')"
    SIDEBAR = "[data-testid='sidebar'], .sidebar, nav"
    MAIN_CONTENT = "[data-testid='main-content'], .main-content, main"
    NOTIFICATION_BELL = "[data-testid='notifications'], .notifications, #notifications"
    LOADING_SPINNER = "[data-testid='loading'], .loading, .spinner"

    def __init__(
        self,
        page: Page,
        app_name: str = "unknown",
        selectors: dict[str, str] | None = None
    ):
        """
        Initialize DashboardPage.

        Args:
            page: Playwright Page instance
            app_name: Name of the application
            selectors: Optional custom selectors to override defaults
        """
        super().__init__(page, app_name)
        self.url = "/dashboard"

        # Override selectors if provided
        if selectors:
            for key, value in selectors.items():
                attr_name = key.upper()
                if hasattr(self, attr_name):
                    setattr(self, attr_name, value)

    def is_loaded(self) -> bool:
        """
        Check if dashboard page is fully loaded.

        Returns:
            True if dashboard is loaded and visible
        """
        # Wait for loading spinner to disappear
        try:
            self.page.wait_for_selector(
                self.LOADING_SPINNER,
                state="hidden",
                timeout=5000
            )
        except Exception:
            pass  # Spinner might not exist

        # Check for dashboard container
        return self.is_visible(self.DASHBOARD_CONTAINER)

    @allure.step("Wait for dashboard to load")
    def wait_for_dashboard(self, timeout: int | None = None) -> None:
        """
        Wait for dashboard to fully load.

        Args:
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout

        # Wait for loading to complete
        self.wait_for_load_state("networkidle")

        # Wait for main content to be visible
        self.page.wait_for_selector(
            self.DASHBOARD_CONTAINER,
            state="visible",
            timeout=timeout
        )

    def get_welcome_message(self) -> str:
        """
        Get welcome message text.

        Returns:
            Welcome message text
        """
        return self.get_text(self.WELCOME_MESSAGE)

    def get_username_from_welcome(self) -> str:
        """
        Extract username from welcome message.

        Returns:
            Username from welcome message
        """
        message = self.get_welcome_message()
        # Try to extract name - common patterns:
        # "Welcome, John!" or "Hello John" or "Welcome back, John Doe"
        for prefix in ["Welcome, ", "Welcome back, ", "Hello ", "Hi "]:
            if prefix in message:
                name = message.split(prefix)[-1]
                # Remove trailing punctuation
                return name.rstrip("!.,")
        return message

    @allure.step("Logout from dashboard")
    def logout(self) -> None:
        """Perform logout action."""
        # Open user menu if exists
        if self.is_visible(self.USER_MENU):
            self.click(self.USER_MENU, "User menu")
            self.page.wait_for_timeout(500)  # Wait for dropdown

        self.click(self.LOGOUT_BUTTON, "Logout button")
        self.wait_for_load_state()

    def navigate_to_section(self, section_name: str) -> None:
        """
        Navigate to a sidebar section.

        Args:
            section_name: Name of the section to navigate to
        """
        with allure.step(f"Navigate to {section_name}"):
            # Try different selector patterns
            selectors = [
                f"[data-testid='{section_name.lower()}']",
                f"a:has-text('{section_name}')",
                f"button:has-text('{section_name}')",
                f".sidebar a:has-text('{section_name}')",
            ]

            for selector in selectors:
                if self.is_visible(selector):
                    self.click(selector, f"{section_name} link")
                    self.wait_for_load_state()
                    return

            raise ValueError(f"Section '{section_name}' not found in sidebar")

    def get_sidebar_items(self) -> list[str]:
        """
        Get list of sidebar navigation items.

        Returns:
            List of sidebar item text
        """
        items = []
        sidebar_links = self.page.locator(f"{self.SIDEBAR} a, {self.SIDEBAR} button")
        count = sidebar_links.count()

        for i in range(count):
            text = sidebar_links.nth(i).text_content()
            if text and text.strip():
                items.append(text.strip())

        return items

    def open_notifications(self) -> None:
        """Open notifications panel."""
        with allure.step("Open notifications"):
            self.click(self.NOTIFICATION_BELL, "Notification bell")

    def get_notification_count(self) -> int:
        """
        Get unread notification count.

        Returns:
            Number of unread notifications
        """
        # Try common patterns for notification badge
        badge_selectors = [
            f"{self.NOTIFICATION_BELL} .badge",
            f"{self.NOTIFICATION_BELL} .count",
            "[data-testid='notification-count']",
        ]

        for selector in badge_selectors:
            if self.is_visible(selector):
                text = self.get_text(selector)
                try:
                    return int(text)
                except ValueError:
                    continue

        return 0

    @allure.step("Verify dashboard is displayed correctly")
    def verify_dashboard_displayed(self) -> None:
        """Verify dashboard page elements are displayed."""
        self.verify_visible(self.DASHBOARD_CONTAINER, "Dashboard container")
        self.verify_visible(self.WELCOME_MESSAGE, "Welcome message")

    @allure.step("Verify user is logged in")
    def verify_logged_in(self, expected_username: str | None = None) -> None:
        """
        Verify user is logged in.

        Args:
            expected_username: Optional expected username in welcome message
        """
        self.verify_dashboard_displayed()

        if expected_username:
            welcome_text = self.get_welcome_message()
            assert expected_username in welcome_text, (
                f"Expected '{expected_username}' in welcome message, got '{welcome_text}'"
            )
