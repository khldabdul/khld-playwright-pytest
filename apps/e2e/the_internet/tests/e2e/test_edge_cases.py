"""The Internet Edge Cases Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("The Internet")
@allure.story("Edge Cases")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
def test_broken_images(broken_images_page, the_internet_config):
    """TC-TI-070: Identify broken images."""
    # Navigate
    broken_images_page.navigate_to_page(the_internet_config.base_url)
    
    # Check all images
    count = broken_images_page.count_images()
    assert count > 0
    
    # Check which ones are broken
    broken_count = 0
    working_count = 0
    
    for i in range(count):
        if broken_images_page.check_image_loaded(i):
            working_count += 1
        else:
            broken_count += 1
    
    # The page should have some broken images
    assert broken_count > 0, "Should have at least one broken image"
    print(f"Found {broken_count} broken images, {working_count} working images")


@allure.feature("The Internet")
@allure.story("Edge Cases")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
def test_challenging_dom(challenging_dom_page, the_internet_config):
    """TC-TI-071: Find elements despite dynamic IDs."""
    # Navigate
    challenging_dom_page.navigate_to_page(the_internet_config.base_url)
    
    # Click buttons (test that we can find them despite changing IDs)
    challenging_dom_page.click_button(0)
    challenging_dom_page.click_button(1)
    
    # Verify table is accessible
    row_count = challenging_dom_page.get_table_row_count()
    assert row_count == 10
    
    # Verify we can read cell data
    first_cell = challenging_dom_page.get_cell_text(0, 0)
    assert first_cell  # Should have some text


@allure.feature("The Internet")
@allure.story("Edge Cases")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
def test_infinite_scroll(infinite_scroll_page, the_internet_config):
    """TC-TI-072: Infinite scroll loads new content."""
    # Navigate
    infinite_scroll_page.navigate_to_page(the_internet_config.base_url)
    
    # Get initial count (wait a moment for first load)
    infinite_scroll_page.page.wait_for_timeout(1000)
    initial_count = infinite_scroll_page.get_paragraph_count()
    
    # Scroll multiple times
    for _ in range(3):
        infinite_scroll_page.scroll_to_bottom()
        infinite_scroll_page.page.wait_for_timeout(1000)
    
    # Verify more paragraphs loaded
    final_count = infinite_scroll_page.get_paragraph_count()
    assert final_count > initial_count, f"Should load more paragraphs: {initial_count} -> {final_count}"
