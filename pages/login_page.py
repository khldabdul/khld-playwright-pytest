"""Login Page Object."""

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for Login page."""

    # Default Locators (can be overridden per app)
    USERNAME_INPUT = "#username"
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    REMEMBER_ME_CHECKBOX = "#remember-me"
    FORGOT_PASSWORD_LINK = "a[href*='forgot']"
    SIGNUP_LINK = "a[href*='signup'], a[href*='register']"

    def __init__(
        self,
        page: Page,
        app_name: str = "unknown",
        selectors: dict[str, str] | None = None
    ):
        """
        Initialize LoginPage.

        Args:
            page: Playwright Page instance
            app_name: Name of the application
            selectors: Optional custom selectors to override defaults
        """
        super().__init__(page, app_name)
        self.url = "/login"

        # Override selectors if provided
        if selectors:
            if "username_field" in selectors:
                self.USERNAME_INPUT = selectors["username_field"]
            if "email_field" in selectors:
                self.EMAIL_INPUT = selectors["email_field"]
            if "password_field" in selectors:
                self.PASSWORD_INPUT = selectors["password_field"]
            if "submit_button" in selectors:
                self.LOGIN_BUTTON = selectors["submit_button"]
            if "error_message" in selectors:
                self.ERROR_MESSAGE = selectors["error_message"]

    @allure.step("Login with username: {username}")
    def login(self, username: str, password: str) -> None:
        """
        Perform login with username and password.

        Args:
            username: Username to login with
            password: Password to login with
        """
        self.fill(self.USERNAME_INPUT, username, "Username field")
        self.fill(self.PASSWORD_INPUT, password, "Password field")
        self.click(self.LOGIN_BUTTON, "Login button")
        self.wait_for_load_state()

    @allure.step("Login with email: {email}")
    def login_with_email(self, email: str, password: str) -> None:
        """
        Perform login with email and password.

        Args:
            email: Email to login with
            password: Password to login with
        """
        self.fill(self.EMAIL_INPUT, email, "Email field")
        self.fill(self.PASSWORD_INPUT, password, "Password field")
        self.click(self.LOGIN_BUTTON, "Login button")
        self.wait_for_load_state()

    @allure.step("Login with remember me option")
    def login_with_remember_me(self, username: str, password: str) -> None:
        """
        Perform login with remember me option checked.

        Args:
            username: Username to login with
            password: Password to login with
        """
        self.fill(self.USERNAME_INPUT, username, "Username field")
        self.fill(self.PASSWORD_INPUT, password, "Password field")
        self.check(self.REMEMBER_ME_CHECKBOX, "Remember me checkbox")
        self.click(self.LOGIN_BUTTON, "Login button")
        self.wait_for_load_state()

    def get_error_message(self) -> str:
        """
        Get error message text.

        Returns:
            Error message text or empty string
        """
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed.

        Returns:
            True if error message is visible
        """
        return self.is_visible(self.ERROR_MESSAGE)

    def is_login_button_enabled(self) -> bool:
        """
        Check if login button is enabled.

        Returns:
            True if login button is enabled
        """
        return self.is_enabled(self.LOGIN_BUTTON)

    def is_login_page_displayed(self) -> bool:
        """
        Check if login page is displayed.

        Returns:
            True if login elements are visible
        """
        # Check for presence of login form elements
        has_username = self.is_visible(self.USERNAME_INPUT) or self.is_visible(self.EMAIL_INPUT)
        has_password = self.is_visible(self.PASSWORD_INPUT)
        has_submit = self.is_visible(self.LOGIN_BUTTON)

        return has_username and has_password and has_submit

    def navigate_to_forgot_password(self) -> None:
        """Navigate to forgot password page."""
        with allure.step("Navigate to forgot password"):
            self.click(self.FORGOT_PASSWORD_LINK, "Forgot password link")
            self.wait_for_load_state()

    def navigate_to_signup(self) -> None:
        """Navigate to signup/registration page."""
        with allure.step("Navigate to signup"):
            self.click(self.SIGNUP_LINK, "Signup link")
            self.wait_for_load_state()

    @allure.step("Verify login failed with error message")
    def verify_login_failed(self, expected_error: str | None = None) -> None:
        """
        Verify that login failed.

        Args:
            expected_error: Optional expected error message text
        """
        self.verify_visible(self.ERROR_MESSAGE, "Error message")

        if expected_error:
            error_text = self.get_error_message()
            assert expected_error.lower() in error_text.lower(), (
                f"Expected error '{expected_error}' not found in '{error_text}'"
            )
