"""ReqRes API - Authentication Tests."""

import pytest
import allure
import requests

@allure.feature("ReqRes API")
@allure.story("Authentication")
@pytest.mark.app("reqres")
@pytest.mark.api
class TestReqResAuth:
    """Test suite for ReqRes authentication."""

    @allure.title("Register successful")
    @pytest.mark.testcase("TC-RR-022")
    def test_register_successful(self, reqres_client):
        """Test successful registration with defined user."""
        email = "eve.holt@reqres.in"
        password = "pistol"
        
        response = reqres_client.register(email=email, password=password)
        
        assert "id" in response
        assert "token" in response
        assert response["token"] is not None

    @allure.title("Register unsuccessful")
    @pytest.mark.testcase("TC-RR-023")
    def test_register_unsuccessful(self, reqres_client):
        """Test registration failure without password."""
        email = "sydney@fife"
        
        with pytest.raises(requests.HTTPError) as exc:
            reqres_client.register(email=email, password=None)
            
        assert exc.value.response.status_code == 400
        assert exc.value.response.json()["error"] == "Missing password"

    @allure.title("Login successful")
    @pytest.mark.testcase("TC-RR-020")
    @pytest.mark.smoke
    def test_login_successful(self, reqres_client):
        """Test successful login."""
        email = "eve.holt@reqres.in"
        password = "cityslicka"
        
        response = reqres_client.login(email=email, password=password)
        
        assert "token" in response
        assert response["token"] is not None

    @allure.title("Login unsuccessful")
    @pytest.mark.testcase("TC-RR-021")
    def test_login_unsuccessful(self, reqres_client):
        """Test login failure without password."""
        email = "peter@klaven"
        
        with pytest.raises(requests.HTTPError) as exc:
            reqres_client.login(email=email, password=None)
            
        assert exc.value.response.status_code == 400
        assert exc.value.response.json()["error"] == "Missing password"
