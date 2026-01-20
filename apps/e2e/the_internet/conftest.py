"""The Internet App E2E Fixtures."""

import pytest
from playwright.sync_api import Page

from apps.e2e.the_internet.pages.login_page import LoginPage
from apps.e2e.the_internet.pages.checkboxes_page import CheckboxesPage
from apps.e2e.the_internet.pages.dropdown_page import DropdownPage
from apps.e2e.the_internet.pages.js_alerts_page import JavaScriptAlertsPage
from apps.e2e.the_internet.pages.dynamic_elements_pages import (
    DynamicLoadingPage,
    AddRemoveElementsPage,
    DisappearingElementsPage
)
from apps.e2e.the_internet.pages.interactions_pages import (
    DragDropPage,
    HoverPage,
    TablesPage
)
from apps.e2e.the_internet.pages.frames_windows_pages import (
    IFramePage,
    NestedFramesPage,
    MultipleWindowsPage
)
from apps.e2e.the_internet.pages.misc_pages import (
    FileUploadPage,
    BasicAuthPage,
    SecurePage,
    NumberInputPage
)
from apps.e2e.the_internet.pages.edge_cases_pages import (
    BrokenImagesPage,
    ChallengingDOMPage,
    InfiniteScrollPage
)


@pytest.fixture(scope="session")
def the_internet_config(app_configs):
    """Get The Internet app configuration."""
    config = app_configs.get("the_internet")
    if not config:
        pytest.skip("The Internet app not configured")
    return config


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def checkboxes_page(page: Page) -> CheckboxesPage:
    return CheckboxesPage(page)


@pytest.fixture
def dropdown_page(page: Page) -> DropdownPage:
    return DropdownPage(page)


@pytest.fixture
def js_alerts_page(page: Page) -> JavaScriptAlertsPage:
    return JavaScriptAlertsPage(page)


@pytest.fixture
def dynamic_loading_page(page: Page) -> DynamicLoadingPage:
    return DynamicLoadingPage(page)


@pytest.fixture
def add_remove_page(page: Page) -> AddRemoveElementsPage:
    return AddRemoveElementsPage(page)


@pytest.fixture
def disappearing_page(page: Page) -> DisappearingElementsPage:
    return DisappearingElementsPage(page)


@pytest.fixture
def drag_drop_page(page: Page) -> DragDropPage:
    return DragDropPage(page)


@pytest.fixture
def hover_page(page: Page) -> HoverPage:
    return HoverPage(page)


@pytest.fixture
def tables_page(page: Page) -> TablesPage:
    return TablesPage(page)


@pytest.fixture
def iframe_page(page: Page) -> IFramePage:
    return IFramePage(page)


@pytest.fixture
def nested_frames_page(page: Page) -> NestedFramesPage:
    return NestedFramesPage(page)


@pytest.fixture
def multiple_windows_page(page: Page) -> MultipleWindowsPage:
    return MultipleWindowsPage(page)


@pytest.fixture
def file_upload_page(page: Page) -> FileUploadPage:
    return FileUploadPage(page)


@pytest.fixture
def basic_auth_page(page: Page) -> BasicAuthPage:
    return BasicAuthPage(page)


@pytest.fixture
def secure_page(page: Page) -> SecurePage:
    return SecurePage(page)


@pytest.fixture
def number_input_page(page: Page) -> NumberInputPage:
    return NumberInputPage(page)


@pytest.fixture
def broken_images_page(page: Page) -> BrokenImagesPage:
    return BrokenImagesPage(page)


@pytest.fixture
def challenging_dom_page(page: Page) -> ChallengingDOMPage:
    return ChallengingDOMPage(page)


@pytest.fixture
def infinite_scroll_page(page: Page) -> InfiniteScrollPage:
    return InfiniteScrollPage(page)
