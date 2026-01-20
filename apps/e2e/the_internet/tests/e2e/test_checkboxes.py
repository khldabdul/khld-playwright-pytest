"""The Internet Checkboxes Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("The Internet")
@allure.story("Checkboxes")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
def test_checkboxes(checkboxes_page, the_internet_config):
    """Test checkbox interactions."""
    # 1. Navigate
    checkboxes_page.navigate_to_checkboxes(the_internet_config.base_url)
    
    # 2. Check initial state (usually 2nd is checked)
    # assert not checkboxes_page.is_checked(0)
    # assert checkboxes_page.is_checked(1)
    
    # 3. Toggle
    checkboxes_page.toggle_checkbox(0, True)
    assert checkboxes_page.is_checked(0)
    
    checkboxes_page.toggle_checkbox(1, False)
    assert not checkboxes_page.is_checked(1)
