"""Base Page class for Page Object Model."""

from __future__ import annotations

from typing import Any

import allure
from playwright.sync_api import Locator, Page, expect


class BasePage:
    """
    Base class for all Page Objects.

    Provides common methods for page interactions with Allure integration.
    """

    def __init__(self, page: Page, app_name: str = "unknown"):
        """
        Initialize BasePage.

        Args:
            page: Playwright Page instance
            app_name: Name of the application (for reporting)
        """
        self.page = page
        self.app_name = app_name
        self.timeout = 30000  # Default timeout in milliseconds

    # Navigation Methods

    def navigate(self, url: str) -> None:
        """
        Navigate to URL.

        Args:
            url: URL to navigate to
        """
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url, timeout=self.timeout)

    def navigate_back(self) -> None:
        """Navigate back in browser history."""
        with allure.step("Navigate back"):
            self.page.go_back()

    def navigate_forward(self) -> None:
        """Navigate forward in browser history."""
        with allure.step("Navigate forward"):
            self.page.go_forward()

    def refresh(self) -> None:
        """Refresh the current page."""
        with allure.step("Refresh page"):
            self.page.reload()

    # Wait Methods

    def wait_for_load_state(self, state: str = "load") -> None:
        """
        Wait for specified load state.

        Args:
            state: Load state to wait for (load, domcontentloaded, networkidle)
        """
        self.page.wait_for_load_state(state, timeout=self.timeout)

    def wait_for_element(self, locator: str, state: str = "visible") -> None:
        """
        Wait for element to reach specified state.

        Args:
            locator: Element locator
            state: State to wait for (visible, attached, hidden, detached)
        """
        with allure.step(f"Wait for element {locator} to be {state}"):
            self.page.wait_for_selector(locator, state=state, timeout=self.timeout)

    def wait_for_url(self, url_pattern: str) -> None:
        """
        Wait for URL to match pattern.

        Args:
            url_pattern: URL pattern (string or regex)
        """
        with allure.step(f"Wait for URL: {url_pattern}"):
            self.page.wait_for_url(url_pattern, timeout=self.timeout)

    # Element Interaction Methods

    def click(self, locator: str, name: str | None = None) -> None:
        """
        Click element.

        Args:
            locator: Element locator
            name: Optional human-readable name for reporting
        """
        element_name = name or locator
        with allure.step(f"Click {element_name}"):
            try:
                self.page.locator(locator).click(timeout=self.timeout)
            except Exception as e:
                self._attach_step_screenshot(f"Failed clicking {element_name}")
                raise

    def double_click(self, locator: str, name: str | None = None) -> None:
        """
        Double-click element.

        Args:
            locator: Element locator
            name: Optional human-readable name for reporting
        """
        element_name = name or locator
        with allure.step(f"Double-click {element_name}"):
            self.page.locator(locator).dblclick(timeout=self.timeout)

    def fill(self, locator: str, text: str, name: str | None = None) -> None:
        """
        Fill input field.

        Args:
            locator: Element locator
            text: Text to fill
            name: Optional human-readable name for reporting
        """
        element_name = name or locator
        # Don't log sensitive data like passwords
        display_text = "***" if "password" in element_name.lower() else text
        with allure.step(f"Fill {element_name} with '{display_text}'"):
            self.page.locator(locator).fill(text, timeout=self.timeout)

    def clear(self, locator: str) -> None:
        """
        Clear input field.

        Args:
            locator: Element locator
        """
        with allure.step(f"Clear {locator}"):
            self.page.locator(locator).clear()

    def type_text(self, locator: str, text: str, delay: int = 50) -> None:
        """
        Type text character by character.

        Args:
            locator: Element locator
            text: Text to type
            delay: Delay between keystrokes in ms
        """
        with allure.step(f"Type text into {locator}"):
            self.page.locator(locator).press_sequentially(text, delay=delay)

    def select_option(self, locator: str, value: str, name: str | None = None) -> None:
        """
        Select option from dropdown.

        Args:
            locator: Element locator
            value: Value to select
            name: Optional human-readable name for reporting
        """
        element_name = name or locator
        with allure.step(f"Select '{value}' from {element_name}"):
            self.page.locator(locator).select_option(value, timeout=self.timeout)

    def check(self, locator: str, name: str | None = None) -> None:
        """
        Check checkbox.

        Args:
            locator: Element locator
            name: Optional human-readable name for reporting
        """
        element_name = name or locator
        with allure.step(f"Check {element_name}"):
            self.page.locator(locator).check(timeout=self.timeout)

    def uncheck(self, locator: str, name: str | None = None) -> None:
        """
        Uncheck checkbox.

        Args:
            locator: Element locator
            name: Optional human-readable name for reporting
        """
        element_name = name or locator
        with allure.step(f"Uncheck {element_name}"):
            self.page.locator(locator).uncheck(timeout=self.timeout)

    def hover(self, locator: str, name: str | None = None) -> None:
        """
        Hover over element.

        Args:
            locator: Element locator
            name: Optional human-readable name for reporting
        """
        element_name = name or locator
        with allure.step(f"Hover over {element_name}"):
            self.page.locator(locator).hover(timeout=self.timeout)

    # Element State Methods

    def get_text(self, locator: str) -> str:
        """
        Get element text content.

        Args:
            locator: Element locator

        Returns:
            Text content of the element
        """
        return self.page.locator(locator).text_content() or ""

    def get_inner_text(self, locator: str) -> str:
        """
        Get element inner text.

        Args:
            locator: Element locator

        Returns:
            Inner text of the element
        """
        return self.page.locator(locator).inner_text()

    def get_value(self, locator: str) -> str:
        """
        Get input field value.

        Args:
            locator: Element locator

        Returns:
            Value of the input field
        """
        return self.page.locator(locator).input_value()

    def get_attribute(self, locator: str, attribute: str) -> str | None:
        """
        Get element attribute.

        Args:
            locator: Element locator
            attribute: Attribute name

        Returns:
            Attribute value or None
        """
        return self.page.locator(locator).get_attribute(attribute)

    def is_visible(self, locator: str) -> bool:
        """
        Check if element is visible.

        Args:
            locator: Element locator

        Returns:
            True if element is visible
        """
        return self.page.locator(locator).is_visible()

    def is_enabled(self, locator: str) -> bool:
        """
        Check if element is enabled.

        Args:
            locator: Element locator

        Returns:
            True if element is enabled
        """
        return self.page.locator(locator).is_enabled()

    def is_checked(self, locator: str) -> bool:
        """
        Check if checkbox/radio is checked.

        Args:
            locator: Element locator

        Returns:
            True if element is checked
        """
        return self.page.locator(locator).is_checked()

    def count_elements(self, locator: str) -> int:
        """
        Count matching elements.

        Args:
            locator: Element locator

        Returns:
            Number of matching elements
        """
        return self.page.locator(locator).count()

    # Assertion Methods

    def verify_visible(self, locator: str, name: str | None = None) -> None:
        """
        Verify element is visible.

        Args:
            locator: Element locator
            name: Optional human-readable name for reporting
        """
        element_name = name or locator
        with allure.step(f"Verify {element_name} is visible"):
            expect(self.page.locator(locator)).to_be_visible(timeout=self.timeout)

    def verify_hidden(self, locator: str, name: str | None = None) -> None:
        """
        Verify element is hidden.

        Args:
            locator: Element locator
            name: Optional human-readable name for reporting
        """
        element_name = name or locator
        with allure.step(f"Verify {element_name} is hidden"):
            expect(self.page.locator(locator)).to_be_hidden(timeout=self.timeout)

    def verify_text(self, locator: str, expected_text: str, name: str | None = None) -> None:
        """
        Verify element contains expected text.

        Args:
            locator: Element locator
            expected_text: Expected text content
            name: Optional human-readable name for reporting
        """
        element_name = name or locator
        with allure.step(f"Verify {element_name} has text '{expected_text}'"):
            expect(self.page.locator(locator)).to_have_text(expected_text, timeout=self.timeout)

    def verify_url(self, expected_url: str) -> None:
        """
        Verify current URL matches expected.

        Args:
            expected_url: Expected URL (string or regex pattern)
        """
        with allure.step(f"Verify URL is {expected_url}"):
            expect(self.page).to_have_url(expected_url, timeout=self.timeout)

    def verify_title(self, expected_title: str) -> None:
        """
        Verify page title.

        Args:
            expected_title: Expected page title
        """
        with allure.step(f"Verify title is '{expected_title}'"):
            expect(self.page).to_have_title(expected_title, timeout=self.timeout)

    # Utility Methods

    def get_locator(self, selector: str) -> Locator:
        """
        Get Playwright Locator object.

        Args:
            selector: Element selector

        Returns:
            Playwright Locator
        """
        return self.page.locator(selector)

    def evaluate_js(self, expression: str) -> Any:
        """
        Evaluate JavaScript expression.

        Args:
            expression: JavaScript expression to evaluate

        Returns:
            Result of the expression
        """
        return self.page.evaluate(expression)

    def take_screenshot(self, name: str = "screenshot", full_page: bool = False) -> bytes:
        """
        Take screenshot and attach to report.

        Args:
            name: Screenshot name
            full_page: Whether to capture full page

        Returns:
            Screenshot bytes
        """
        screenshot = self.page.screenshot(full_page=full_page)
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        return screenshot

    def _attach_step_screenshot(self, name: str) -> None:
        """
        Attach screenshot to current Allure step.

        Args:
            name: Screenshot name
        """
        try:
            screenshot = self.page.screenshot()
            allure.attach(
                screenshot,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass  # Screenshot capture failed, continue
