"""The Internet Edge Cases Tests.

This test suite covers edge case scenarios including:
- Broken image detection
- Dynamic ID handling
- Infinite scroll

Application: https://the-internet.herokuapp.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import e2e_test


@e2e_test(
    epic="The Internet E2E",
    feature="Edge Cases",
    story="Broken Images",
    testcase="TC-TI-070",
    requirement="US-TI-EDGE-001",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Identify broken images",
    link="https://the-internet.herokuapp.com/broken_images",
    description="""
Verify that broken images can be identified.

**Test Steps:**
1. Navigate to broken images page
2. Count all images on page
3. Check each image for load status
4. Verify at least one broken image exists

**Test Coverage:**
- Image detection
- Broken image identification
- Image load verification

**Business Value:}
Tests ability to detect and handle broken image assets.
""",
)
def test_broken_images(broken_images_page, the_internet_config):
    """TC-TI-070: Identify broken images."""

    with allure.step("Navigate to broken images page"):
        broken_images_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Check all images for load status"):
        count = broken_images_page.count_images()
        assert count > 0

        broken_count = 0
        working_count = 0

        for i in range(count):
            if broken_images_page.check_image_loaded(i):
                working_count += 1
            else:
                broken_count += 1

    with allure.step("Verify at least one broken image exists"):
        assert broken_count > 0, "Should have at least one broken image"


@e2e_test(
    epic="The Internet E2E",
    feature="Edge Cases",
    story="Dynamic IDs",
    testcase="TC-TI-071",
    requirement="US-TI-EDGE-002",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Find elements despite dynamic IDs",
    link="https://the-internet.herokuapp.com/challenging_dom",
    description="""
Verify that elements with dynamic IDs can be interacted with.

**Test Steps:**
1. Navigate to challenging DOM page
2. Click buttons with dynamic IDs
3. Verify table is accessible
4. Read cell data from table

**Test Coverage:**
- Dynamic ID handling
- Element location despite ID changes
- Table data extraction

**Business Value:}
Tests robustness against dynamic element IDs in SPA frameworks.
""",
)
def test_challenging_dom(challenging_dom_page, the_internet_config):
    """TC-TI-071: Find elements despite dynamic IDs."""

    with allure.step("Navigate to challenging DOM page"):
        challenging_dom_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Click buttons with dynamic IDs"):
        challenging_dom_page.click_button(0)
        challenging_dom_page.click_button(1)

    with allure.step("Verify table is accessible"):
        row_count = challenging_dom_page.get_table_row_count()
        assert row_count == 10

    with allure.step("Verify cell data can be read"):
        first_cell = challenging_dom_page.get_cell_text(0, 0)
        assert first_cell


@e2e_test(
    epic="The Internet E2E",
    feature="Edge Cases",
    story="Infinite Scroll",
    testcase="TC-TI-072",
    requirement="US-TI-EDGE-003",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Infinite scroll loads new content",
    link="https://the-internet.herokuapp.com/infinite_scroll",
    description="""
Verify that infinite scroll loads new content.

**Test Steps:**
1. Navigate to infinite scroll page
2. Wait for initial content load
3. Get initial paragraph count
4. Scroll to bottom multiple times
5. Verify more paragraphs loaded

**Test Coverage:**
- Infinite scroll handling
- Dynamic content loading
- Scroll-triggered actions

**Business Value:}
Tests common infinite scroll pattern in modern web apps.
""",
)
def test_infinite_scroll(infinite_scroll_page, the_internet_config):
    """TC-TI-072: Infinite scroll loads new content."""

    with allure.step("Navigate to infinite scroll page"):
        infinite_scroll_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Get initial paragraph count"):
        infinite_scroll_page.page.wait_for_timeout(1000)
        initial_count = infinite_scroll_page.get_paragraph_count()

    with allure.step("Scroll to bottom 3 times"):
        for _ in range(3):
            infinite_scroll_page.scroll_to_bottom()
            infinite_scroll_page.page.wait_for_timeout(1000)

    with allure.step("Verify more paragraphs loaded"):
        final_count = infinite_scroll_page.get_paragraph_count()
        assert final_count > initial_count, f"Should load more paragraphs: {initial_count} -> {final_count}"
