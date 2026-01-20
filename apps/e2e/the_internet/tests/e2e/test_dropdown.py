"""The Internet Dropdown Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("The Internet")
@allure.story("Dropdown")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
def test_dropdown_selection(dropdown_page, the_internet_config):
    """Test dropdown selection."""
    # 1. Navigate
    dropdown_page.navigate_to_dropdown(the_internet_config.base_url)
    
    # 2. Select Option 1
    dropdown_page.select_option("1")
    assert dropdown_page.get_selected_option_text() == "Option 1"
    
    # 3. Select Option 2
    dropdown_page.select_option("2")
    assert dropdown_page.get_selected_option_text() == "Option 2"
