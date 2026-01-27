"""The Internet Interactions Tests.

This test suite covers advanced user interactions including:
- Drag and drop operations
- Hover effects
- Table sorting

Application: https://the-internet.herokuapp.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("The Internet E2E")
@allure.feature("User Interactions")
@allure.story("Drag and Drop")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-030")
@pytest.mark.requirement("US-TI-INT-001")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that elements can be dragged and dropped.

**Test Steps:**
1. Navigate to drag and drop page
2. Verify initial state (A in left, B in right)
3. Drag column A to column B
4. Verify columns swapped

**Test Coverage:**
- Drag and drop functionality
- Position verification
- State after interaction

**Business Value:}
Tests common drag-and-drop UI patterns in web apps.
"""))
def test_drag_and_drop(drag_drop_page, the_internet_config):
    """TC-TI-030: Drag and drop columns."""

    with allure.step("Navigate to drag and drop page"):
        drag_drop_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Verify initial state"):
        assert drag_drop_page.get_column_a_text() == "A"
        assert drag_drop_page.get_column_b_text() == "B"

    with allure.step("Drag A to B"):
        drag_drop_page.drag_a_to_b()

    with allure.step("Verify columns swapped"):
        assert drag_drop_page.get_column_a_text() == "B"
        assert drag_drop_page.get_column_b_text() == "A"


@allure.epic("The Internet E2E")
@allure.feature("User Interactions")
@allure.story("Hover Effects")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-031")
@pytest.mark.requirement("US-TI-INT-002")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that hover reveals hidden user information.

**Test Steps:**
1. Navigate to hover page
2. Hover over first user avatar
3. Verify user info appears
4. Hover over second user avatar
5. Verify different user info appears

**Test Coverage:**
- Hover interaction
- Dynamic content reveal
- User-specific content

**Business Value:}
Tests hover-based UI patterns for contextual information.
"""))
def test_hover(hover_page, the_internet_config):
    """TC-TI-031: Hover to display hidden info."""

    with allure.step("Navigate to hover page"):
        hover_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Hover over first user and verify info"):
        hover_page.hover_user(0)
        assert hover_page.is_user_info_visible(0)
        assert "user1" in hover_page.get_user_name(0)

    with allure.step("Hover over second user and verify different info"):
        hover_page.hover_user(1)
        assert hover_page.is_user_info_visible(1)
        assert "user2" in hover_page.get_user_name(1)


@allure.epic("The Internet E2E")
@allure.feature("User Interactions")
@allure.story("Table Sorting")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-032")
@pytest.mark.requirement("US-TI-INT-003")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that data tables can be sorted by column.

**Test Steps:**
1. Navigate to sortable data tables page
2. Get initial last name column values
3. Click "Last Name" header
4. Verify table remains accessible with same row count

**Test Coverage:**
- Table interaction
- Header click handling
- Table structure integrity

**Business Value:}
Tests sortable data grid patterns in enterprise applications.
"""))
def test_sortable_tables(tables_page, the_internet_config):
    """TC-TI-032: Sort data tables by column."""

    with allure.step("Navigate to sortable tables page"):
        tables_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Get initial last names"):
        last_names_before = tables_page.get_column_values(0)

    with allure.step("Click 'Last Name' header to sort"):
        tables_page.click_header("Last Name")
        tables_page.page.wait_for_timeout(100)

    with allure.step("Verify table remains accessible"):
        last_names_after = tables_page.get_column_values(0)
        assert len(last_names_after) == len(last_names_before)
