"""The Internet JavaScript Dialogs Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("The Internet")
@allure.story("JavaScript Dialogs")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-040")
def test_js_alert(js_alerts_page, the_internet_config):
    """TC-TI-040: Handle JavaScript alert."""
    # Navigate
    js_alerts_page.navigate_to_alerts(the_internet_config.base_url)
    
    # Set up alert handler
    js_alerts_page.page.once("dialog", lambda dialog: dialog.accept())
    
    # Trigger alert
    js_alerts_page.click_alert()
    
    # Verify result
    result = js_alerts_page.get_result_text()
    assert "You successfully clicked an alert" in result


@allure.feature("The Internet")
@allure.story("JavaScript Dialogs")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-041")
def test_js_confirm_accept(js_alerts_page, the_internet_config):
    """TC-TI-041: Handle JavaScript confirm - Accept."""
    # Navigate
    js_alerts_page.navigate_to_alerts(the_internet_config.base_url)
    
    # Set up confirm handler - accept
    js_alerts_page.page.once("dialog", lambda dialog: dialog.accept())
    
    # Trigger confirm
    js_alerts_page.click_confirm()
    
    # Verify result
    result = js_alerts_page.get_result_text()
    assert "You clicked: Ok" in result


@allure.feature("The Internet")
@allure.story("JavaScript Dialogs")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-042")
def test_js_confirm_dismiss(js_alerts_page, the_internet_config):
    """TC-TI-042: Handle JavaScript confirm - Dismiss."""
    # Navigate
    js_alerts_page.navigate_to_alerts(the_internet_config.base_url)
    
    # Set up confirm handler - dismiss
    js_alerts_page.page.once("dialog", lambda dialog: dialog.dismiss())
    
    # Trigger confirm
    js_alerts_page.click_confirm()
    
    # Verify result
    result = js_alerts_page.get_result_text()
    assert "You clicked: Cancel" in result


@allure.feature("The Internet")
@allure.story("JavaScript Dialogs")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-043")
def test_js_prompt(js_alerts_page, the_internet_config):
    """TC-TI-043: Handle JavaScript prompt."""
    # Navigate
    js_alerts_page.navigate_to_alerts(the_internet_config.base_url)
    
    # Set up prompt handler with text
    test_text = "Hello Playwright"
    js_alerts_page.page.once("dialog", lambda dialog: dialog.accept(test_text))
    
    # Trigger prompt
    js_alerts_page.click_prompt()
    
    # Verify result
    result = js_alerts_page.get_result_text()
    assert f"You entered: {test_text}" in result
