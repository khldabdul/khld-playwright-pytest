"""The Internet Uploads and Auth Pages."""

from playwright.sync_api import Page
import allure
from pages.base_page import BasePage


class FileUploadPage(BasePage):
    """Page object for File Upload page."""

    URL_SUFFIX = "/upload"

    def __init__(self, page: Page):
        super().__init__(page)
        self.file_input = self.page.locator('#file-upload')
        self.upload_button = self.page.locator('#file-submit')
        self.uploaded_files = self.page.locator('#uploaded-files')

    @allure.step("Navigate to File Upload")
    def navigate_to_page(self, base_url: str):
        """Navigate to upload page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Upload file: {file_path}")
    def upload_file(self, file_path: str):
        """Upload a file."""
        self.file_input.set_input_files(file_path)
        self.upload_button.click()

    def get_uploaded_filename(self) -> str:
        """Get uploaded filename."""
        return self.uploaded_files.inner_text()


class BasicAuthPage(BasePage):
    """Page object for Basic Auth page."""

    URL_SUFFIX = "/basic_auth"

    def __init__(self, page: Page):
        super().__init__(page)
        self.success_message = self.page.locator('.example p')

    @allure.step("Navigate to Basic Auth with credentials")
    def navigate_with_auth(self, username: str, password: str):
        """Navigate to basic auth with credentials in URL."""
        url = f"https://{username}:{password}@the-internet.herokuapp.com{self.URL_SUFFIX}"
        self.navigate(url)

    def get_message(self) -> str:
        """Get success message."""
        return self.success_message.inner_text()


class SecurePage(BasePage):
    """Page object for Secure Area after login."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.logout_button = self.page.locator('a[href="/logout"]')
        self.flash_message = self.page.locator('#flash')

    @allure.step("Logout")
    def logout(self):
        """Click logout button."""
        self.logout_button.click()


class NumberInputPage(BasePage):
    """Page object for Number Input page."""

    URL_SUFFIX = "/inputs"

    def __init__(self, page: Page):
        super().__init__(page)
        self.number_input = self.page.locator('input[type="number"]')

    @allure.step("Navigate to Number Input")
    def navigate_to_page(self, base_url: str):
        """Navigate to inputs page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Enter number: {number}")
    def enter_number(self, number: str):
        """Enter a number."""
        self.number_input.fill(number)

    @allure.step("Increment number")
    def increment(self):
        """Press up arrow to increment."""
        self.number_input.press("ArrowUp")

    @allure.step("Decrement number")
    def decrement(self):
        """Press down arrow to decrement."""
        self.number_input.press("ArrowDown")

    def get_value(self) -> str:
        """Get input value."""
        return self.number_input.input_value()
