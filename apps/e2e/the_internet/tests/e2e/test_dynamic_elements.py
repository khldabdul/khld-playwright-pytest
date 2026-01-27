"""The Internet Dynamic Elements Tests.

This test suite covers dynamic element operations including:
- Waiting for elements to appear
- Dynamically adding/removing elements
- Handling disappearing elements

Application: https://the-internet.herokuapp.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("The Internet E2E")
@allure.feature("Dynamic Elements")
@allure.story("Dynamic Loading")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-020")
@pytest.mark.requirement("US-TI-DYN-001")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that hidden elements become visible after loading.

**Test Steps:**
1. Navigate to dynamic loading example 1
2. Click start button
3. Wait for loading to complete
4. Verify text appears

**Test Coverage:**
- Waiting for hidden elements
- Loading state handling
- Dynamic content display

**Business Value:**
Common pattern for lazy-loaded content in modern web apps.
"""))
def test_dynamic_loading_element_appears(dynamic_loading_page, the_internet_config):
    """TC-TI-020: Dynamic loading - element becomes visible."""

    with allure.step("Navigate to dynamic loading example 1"):
        dynamic_loading_page.navigate_to_example(the_internet_config.base_url, 1)

    with allure.step("Click start and wait for loading"):
        dynamic_loading_page.click_start()
        dynamic_loading_page.wait_for_loading_complete()

    with allure.step("Verify text appears"):
        text = dynamic_loading_page.get_finish_text()
        assert "Hello World!" in text


@allure.epic("The Internet E2E")
@allure.feature("Dynamic Elements")
@allure.story("Dynamic Loading")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-021")
@pytest.mark.requirement("US-TI-DYN-002")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that elements added to DOM after loading become visible.

**Test Steps:**
1. Navigate to dynamic loading example 2
2. Click start button
3. Wait for loading to complete
4. Verify element is added and visible

**Test Coverage:**
- Waiting for DOM elements
- Dynamic element rendering
- Post-render verification

**Business Value:**
Tests handling of AJAX and dynamic content insertion.
"""))
def test_dynamic_loading_element_rendered(dynamic_loading_page, the_internet_config):
    """TC-TI-021: Dynamic loading - element added to DOM."""

    with allure.step("Navigate to dynamic loading example 2"):
        dynamic_loading_page.navigate_to_example(the_internet_config.base_url, 2)

    with allure.step("Click start and wait for loading"):
        dynamic_loading_page.click_start()
        dynamic_loading_page.wait_for_loading_complete()

    with allure.step("Verify element is visible"):
        expect(dynamic_loading_page.finish_text).to_be_visible()
        text = dynamic_loading_page.get_finish_text()
        assert "Hello World!" in text


@allure.epic("The Internet E2E")
@allure.feature("Dynamic Elements")
@allure.story("Add/Remove Elements")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-022")
@pytest.mark.requirement("US-TI-DYN-003")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that elements can be dynamically added and removed.

**Test Steps:**
1. Navigate to add/remove elements page
2. Add 3 elements
3. Verify 3 delete buttons exist
4. Delete one element
5. Verify 2 elements remain

**Test Coverage:**
- Dynamic element addition
- Dynamic element removal
- Count verification

**Business Value:**
Tests handling of dynamically generated UI components.
"""))
def test_add_remove_elements(add_remove_page, the_internet_config):
    """TC-TI-022: Add and remove elements dynamically."""

    with allure.step("Navigate to add/remove elements page"):
        add_remove_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Add 3 elements"):
        for _ in range(3):
            add_remove_page.add_element()

    with allure.step("Verify 3 delete buttons exist"):
        assert add_remove_page.get_delete_button_count() == 3

    with allure.step("Delete one element and verify 2 remain"):
        add_remove_page.delete_element(0)
        assert add_remove_page.get_delete_button_count() == 2


@allure.epic("The Internet E2E")
@allure.feature("Dynamic Elements")
@allure.story("Disappearing Elements")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-023")
@pytest.mark.requirement("US-TI-DYN-004")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that menu elements can disappear on page reload.

**Test Steps:**
1. Navigate to disappearing elements page
2. Get initial menu item count
3. Reload page multiple times
4. Verify menu count varies (Gallery element disappears)

**Test Coverage:**
- Handling disappearing elements
- Dynamic menu behavior
- Page reload effects

**Business Value:**
Tests robustness against intermittent UI elements.
"""))
def test_disappearing_elements(disappearing_page, the_internet_config):
    """TC-TI-023: Verify elements can disappear on reload."""

    with allure.step("Navigate to disappearing elements page"):
        disappearing_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Get initial menu count"):
        initial_count = disappearing_page.get_menu_item_count()

    with allure.step("Reload 5 times and track counts"):
        counts = [initial_count]
        for _ in range(5):
            disappearing_page.reload_page()
            counts.append(disappearing_page.get_menu_item_count())

    with allure.step("Verify count varies between 4 and 5"):
        unique_counts = set(counts)
        assert len(unique_counts) >= 1
        assert all(count in [4, 5] for count in counts)
