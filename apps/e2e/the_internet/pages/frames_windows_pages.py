"""The Internet Frames and Windows Pages."""

from playwright.sync_api import Page
import allure
from pages.base_page import BasePage


class IFramePage(BasePage):
    """Page object for iFrame (TinyMCE) page."""

    URL_SUFFIX = "/iframe"

    def __init__(self, page: Page):
        super().__init__(page)
        self.iframe = self.page.frame_locator('#mce_0_ifr')
        self.editor_body = self.iframe.locator('body#tinymce')

    @allure.step("Navigate to iFrame Page")
    def navigate_to_page(self, base_url: str):
        """Navigate to iframe page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Type in editor: {text}")
    def type_in_editor(self, text: str):
        """Clear and type text in TinyMCE editor."""
        # Wait for editor to be ready
        self.editor_body.wait_for(state="visible")
        # Use fill directly instead of clicking
        self.editor_body.fill(text)

    def get_editor_text(self) -> str:
        """Get text from editor."""
        return self.editor_body.inner_text()


class NestedFramesPage(BasePage):
    """Page object for Nested Frames page."""

    URL_SUFFIX = "/nested_frames"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Navigate to Nested Frames")
    def navigate_to_page(self, base_url: str):
        """Navigate to nested frames page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    def get_frame_text(self, frame_name: str) -> str:
        """Get text from specific frame."""
        if frame_name in ["LEFT", "MIDDLE", "RIGHT"]:
            # These are in the top frameset
            top_frame = self.page.frame(name="frame-top")
            if top_frame:
                target_frame = top_frame.child_frames[
                    ["LEFT", "MIDDLE", "RIGHT"].index(frame_name)
                ]
                return target_frame.locator('body').inner_text()
        elif frame_name == "BOTTOM":
            bottom_frame = self.page.frame(name="frame-bottom")
            if bottom_frame:
                return bottom_frame.locator('body').inner_text()
        return ""


class MultipleWindowsPage(BasePage):
    """Page object for Multiple Windows page."""

    URL_SUFFIX = "/windows"

    def __init__(self, page: Page):
        super().__init__(page)
        self.click_here_link = self.page.get_by_text("Click Here")

    @allure.step("Navigate to Multiple Windows")
    def navigate_to_page(self, base_url: str):
        """Navigate to windows page."""
        self.navigate(f"{base_url}{self.URL_SUFFIX}")

    @allure.step("Click to open new window")
    def open_new_window(self):
        """Click link to open new window."""
        self.click_here_link.click()
