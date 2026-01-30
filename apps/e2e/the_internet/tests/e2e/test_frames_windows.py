"""The Internet Frames and Windows Tests.

This test suite covers iframe and multi-window operations including:
- iFrame content access
- Nested frame navigation
- Multiple window handling

Application: https://the-internet.herokuapp.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import e2e_test


@e2e_test(
    epic="The Internet E2E",
    feature="Frames & Windows",
    story="iFrame Editor",
    testcase="TC-TI-050",
    requirement="US-TI-FRAME-001",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Access iFrame TinyMCE editor",
    link="https://the-internet.herokuapp.com/iframe",
    description="""
Verify that iFrame content can be accessed and read.

**Test Steps:**
1. Navigate to iFrame page
2. Access the TinyMCE editor iframe
3. Verify editor body is visible
4. Read text content from iframe

**Test Coverage:**
- iFrame access
- Cross-frame content reading
- Editor verification

**Business Value:}
Tests WYSIWYG editor integration patterns.
""",
)
def test_iframe_editor(iframe_page, the_internet_config):
    """TC-TI-050: Access iFrame TinyMCE editor."""

    with allure.step("Navigate to iFrame page"):
        iframe_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Verify editor iframe is accessible"):
        expect(iframe_page.editor_body).to_be_visible()

    with allure.step("Read text from iframe"):
        text = iframe_page.get_editor_text()
        assert len(text) > 0


@e2e_test(
    epic="The Internet E2E",
    feature="Frames & Windows",
    story="Nested Frames",
    testcase="TC-TI-051",
    requirement="US-TI-FRAME-002",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Read content from nested frames",
    link="https://the-internet.herokuapp.com/nested_frames",
    description="""
Verify that content can be read from nested frames.

**Test Steps:**
1. Navigate to nested frames page
2. Read content from LEFT frame
3. Read content from MIDDLE frame
4. Read content from RIGHT frame
5. Read content from BOTTOM frame
6. Verify all frames have expected text

**Test Coverage:**
- Nested frame access
- Multi-level frame navigation
- Content extraction

**Business Value:}
Tests complex frame hierarchy handling.
""",
)
def test_nested_frames(nested_frames_page, the_internet_config):
    """TC-TI-051: Read content from nested frames."""

    with allure.step("Navigate to nested frames page"):
        nested_frames_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Read content from all frames"):
        left_text = nested_frames_page.get_frame_text("LEFT")
        middle_text = nested_frames_page.get_frame_text("MIDDLE")
        right_text = nested_frames_page.get_frame_text("RIGHT")
        bottom_text = nested_frames_page.get_frame_text("BOTTOM")

    with allure.step("Verify all frames have expected text"):
        assert "LEFT" in left_text
        assert "MIDDLE" in middle_text
        assert "RIGHT" in right_text
        assert "BOTTOM" in bottom_text


@e2e_test(
    epic="The Internet E2E",
    feature="Frames & Windows",
    story="Multiple Windows",
    testcase="TC-TI-052",
    requirement="US-TI-WIN-001",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Handle multiple windows/tabs",
    link="https://the-internet.herokuapp.com/windows",
    description="""
Verify that multiple browser windows can be handled.

**Test Steps:**
1. Navigate to multiple windows page
2. Open new window
3. Verify new window content
4. Close new window

**Test Coverage:**
- Multi-window handling
- New window/tab interaction
- Window cleanup

**Business Value:}
Tests handling of popups and new windows.
""",
)
def test_multiple_windows(multiple_windows_page, the_internet_config, page):
    """TC-TI-052: Handle multiple windows/tabs."""

    with allure.step("Navigate to multiple windows page"):
        multiple_windows_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Open new window and capture reference"):
        with page.context.expect_page() as new_page_info:
            multiple_windows_page.open_new_window()
        new_page = new_page_info.value

    with allure.step("Verify new window content"):
        expect(new_page.locator('h3')).to_contain_text("New Window")

    with allure.step("Close new window"):
        new_page.close()
