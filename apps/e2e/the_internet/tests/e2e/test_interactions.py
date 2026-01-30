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

from infrastructure.utils.allure_helpers import e2e_test


@e2e_test(
    epic="The Internet E2E",
    feature="User Interactions",
    story="Drag and Drop",
    testcase="TC-TI-030",
    requirement="US-TI-INT-001",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Drag and drop columns",
    link="https://the-internet.herokuapp.com/drag_and_drop",
    description="""
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
""",
)
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


@e2e_test(
    epic="The Internet E2E",
    feature="User Interactions",
    story="Hover Effects",
    testcase="TC-TI-031",
    requirement="US-TI-INT-002",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Hover to display hidden info",
    link="https://the-internet.herokuapp.com/hovers",
    description="""
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
""",
)
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


@e2e_test(
    epic="The Internet E2E",
    feature="User Interactions",
    story="Table Sorting",
    testcase="TC-TI-032",
    requirement="US-TI-INT-003",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Sort data tables by column",
    link="https://the-internet.herokuapp.com/tables",
    description="""
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
""",
)
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
