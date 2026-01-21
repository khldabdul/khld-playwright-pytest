"""The Internet Frames and Windows Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("The Internet")
@allure.story("Frames & Windows")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-050")
def test_iframe_editor(iframe_page, the_internet_config):
    """TC-TI-050: Access iFrame TinyMCE editor."""
    # Navigate
    iframe_page.navigate_to_page(the_internet_config.base_url)
    
    # Verify we can access and read the iframe content
    # The editor on this site is readonly, so we just verify access
    expect(iframe_page.editor_body).to_be_visible()
    
    # Verify we can read text from iframe
    text = iframe_page.get_editor_text()
    assert len(text) > 0  # Should have some default content


@allure.feature("The Internet")
@allure.story("Frames & Windows")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-051")
def test_nested_frames(nested_frames_page, the_internet_config):
    """TC-TI-051: Read content from nested frames."""
    # Navigate
    nested_frames_page.navigate_to_page(the_internet_config.base_url)
    
    # Read content from each frame
    left_text = nested_frames_page.get_frame_text("LEFT")
    middle_text = nested_frames_page.get_frame_text("MIDDLE")
    right_text = nested_frames_page.get_frame_text("RIGHT")
    bottom_text = nested_frames_page.get_frame_text("BOTTOM")
    
    # Verify each frame has expected text
    assert "LEFT" in left_text
    assert "MIDDLE" in middle_text
    assert "RIGHT" in right_text
    assert "BOTTOM" in bottom_text


@allure.feature("The Internet")
@allure.story("Frames & Windows")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-052")
def test_multiple_windows(multiple_windows_page, the_internet_config, page):
    """TC-TI-052: Handle multiple windows/tabs."""
    # Navigate
    multiple_windows_page.navigate_to_page(the_internet_config.base_url)
    
    # Open new window
    with page.context.expect_page() as new_page_info:
        multiple_windows_page.open_new_window()
    
    new_page = new_page_info.value
    
    # Verify new window content
    expect(new_page.locator('h3')).to_contain_text("New Window")
    
    # Close new window
    new_page.close()
