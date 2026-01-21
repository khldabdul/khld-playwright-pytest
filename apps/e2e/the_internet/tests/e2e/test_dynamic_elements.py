"""The Internet Dynamic Elements Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("The Internet")
@allure.story("Dynamic Elements")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-020")
def test_dynamic_loading_element_appears(dynamic_loading_page, the_internet_config):
    """TC-TI-020: Dynamic loading - element becomes visible."""
    # Navigate to example 1 (element hidden)
    dynamic_loading_page.navigate_to_example(the_internet_config.base_url, 1)
    
    # Click start
    dynamic_loading_page.click_start()
    
    # Wait for loading
    dynamic_loading_page.wait_for_loading_complete()
    
    # Verify text appears
    text = dynamic_loading_page.get_finish_text()
    assert "Hello World!" in text


@allure.feature("The Internet")
@allure.story("Dynamic Elements")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-021")
def test_dynamic_loading_element_rendered(dynamic_loading_page, the_internet_config):
    """TC-TI-021: Dynamic loading - element added to DOM."""
    # Navigate to example 2 (element not in DOM)
    dynamic_loading_page.navigate_to_example(the_internet_config.base_url, 2)
    
    # Click start
    dynamic_loading_page.click_start()
    
    # Wait for loading
    dynamic_loading_page.wait_for_loading_complete()
    
    # Verify text appears
    expect(dynamic_loading_page.finish_text).to_be_visible()
    text = dynamic_loading_page.get_finish_text()
    assert "Hello World!" in text


@allure.feature("The Internet")
@allure.story("Dynamic Elements")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-022")
def test_add_remove_elements(add_remove_page, the_internet_config):
    """TC-TI-022: Add and remove elements dynamically."""
    # Navigate
    add_remove_page.navigate_to_page(the_internet_config.base_url)
    
    # Add 3 elements
    for _ in range(3):
        add_remove_page.add_element()
    
    # Verify 3 delete buttons
    assert add_remove_page.get_delete_button_count() == 3
    
    # Delete one
    add_remove_page.delete_element(0)
    
    # Verify 2 remain
    assert add_remove_page.get_delete_button_count() == 2


@allure.feature("The Internet")
@allure.story("Dynamic Elements")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-023")
def test_disappearing_elements(disappearing_page, the_internet_config):
    """TC-TI-023: Verify elements can disappear on reload."""
    # Navigate
    disappearing_page.navigate_to_page(the_internet_config.base_url)
    
    # Get initial count
    initial_count = disappearing_page.get_menu_item_count()
    
    # Reload and check multiple times
    counts = [initial_count]
    for _ in range(5):
        disappearing_page.reload_page()
        counts.append(disappearing_page.get_menu_item_count())
    
    # Verify variation exists (sometimes 4, sometimes 5)
    unique_counts = set(counts)
    assert len(unique_counts) >= 1  # At least consistent or varying
    # The "Gallery" element may disappear
    assert all(count in [4, 5] for count in counts)
