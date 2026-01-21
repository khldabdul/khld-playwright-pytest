"""ReqRes API - Resources Tests."""

import pytest
import allure
import requests

@allure.feature("ReqRes API")
@allure.story("Resources")
@pytest.mark.app("reqres")
@pytest.mark.api
class TestReqResResources:
    """Test suite for ReqRes resource operations."""

    @allure.title("Get list of resources")
    @pytest.mark.testcase("TC-RR-030")
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

    @allure.title("Get single resource")
    @pytest.mark.testcase("TC-RR-031")
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

    @allure.title("Get resource not found")
    @pytest.mark.testcase("TC-RR-032")
    def test_get_resource_not_found(self, reqres_client):
        """Test retrieving a non-existent resource returns 404."""
        with pytest.raises(requests.HTTPError) as exc:
            reqres_client.get_resource(23)
        assert exc.value.response.status_code == 404
