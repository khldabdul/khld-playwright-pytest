"""ReqRes API - Resources Tests."""

from __future__ import annotations

import pytest
import allure
import requests

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("ReqRes API")
@allure.feature("Resource Management")
@allure.label("layer", "api")
@allure.label("type", "functional")
@pytest.mark.app("reqres")
@pytest.mark.api
class TestReqResResources:
    """Test suite for ReqRes resource operations."""

    @allure.story("List Resources")
    @allure.title("Get list of resources")
    @allure.description_html(markdown_to_html("""
    Verify that the API returns a list of resources correctly.

    **Test Coverage:**
    - Response contains expected data structure
    - Resource objects contain all required fields (id, name, year, color, pantone_value)
    - Pagination metadata is present (total)

    **Business Value:**
    Ensures the resource catalog is accessible, which is essential
    for browsing available resources in the system.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://reqres.in/api-docs/#/Resources/List_resources", name="API Docs")
    @pytest.mark.testcase("TC-RR-030")
    @pytest.mark.requirement("US-RES-001")
    @pytest.mark.smoke
    def test_get_resources(self, reqres_client):
        """Test retrieving list of resources."""
        response = reqres_client.get_resources()

        assert len(response["data"]) > 0
        assert "total" in response

        # Verify resource structure
        resource = response["data"][0]
        assert "id" in resource
        assert "name" in resource
        assert "year" in resource
        assert "color" in resource
        assert "pantone_value" in resource

    @allure.story("View Resource Details")
    @allure.title("Get single resource")
    @allure.description_html(markdown_to_html("""
    Verify that a single resource can be retrieved by its ID.

    **Test Coverage:**
    - Valid resource ID returns resource data
    - Resource data is complete and accurate
    - All expected fields are present including color codes

    **Business Value:**
    Enables viewing individual resource details, a core feature
    of any resource management system.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://reqres.in/api-docs/#/Resources/Single_resource", name="API Docs")
    @pytest.mark.testcase("TC-RR-031")
    @pytest.mark.requirement("US-RES-002")
    def test_get_single_resource(self, reqres_client):
        """Test retrieving a single resource."""
        resource_id = 2
        response = reqres_client.get_resource(resource_id)

        data = response["data"]
        assert data["id"] == resource_id
        assert data["name"] == "fuchsia rose"
        assert data["year"] == 2001
        assert data["color"] == "#C74375"
        assert "pantone_value" in data

    @allure.story("View Resource Details")
    @allure.title("Get non-existent resource returns 404")
    @allure.description_html(markdown_to_html("""
    Verify that requesting a non-existent resource returns proper 404 error.

    **Test Coverage:**
    - Invalid resource ID handling
    - Proper HTTP status code (404)
    - Error message clarity

    **Business Value:**
    Ensures graceful error handling when users request
    non-existent resources.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-RR-032")
    @pytest.mark.requirement("US-RES-003")
    def test_get_resource_not_found(self, reqres_client):
        """Test retrieving a non-existent resource returns 404."""
        with pytest.raises(requests.HTTPError) as exc:
            reqres_client.get_resource(23)
        assert exc.value.response.status_code == 404
