"""ReqRes API - Authentication Tests.

This test suite covers authentication operations including:
- User registration
- User login
- Error handling for missing credentials

API Documentation: https://reqres.in/api-docs/
"""

from __future__ import annotations

import pytest
import allure

from requests import HTTPError

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("ReqRes API")
@allure.feature("Authentication")
@allure.label("layer", "api")
@allure.label("type", "functional")
@pytest.mark.app("reqres")
@pytest.mark.api
class TestReqResAuth:
    """Test suite for ReqRes authentication."""

    @allure.story("Register User")
    @allure.title("Register new user successfully")
    @allure.description_html(markdown_to_html("""
    Verify that a new user can be registered with valid credentials.

    **Test Coverage:**
    - User registration with valid email and password
    - Response contains user ID and authentication token
    - Token is properly generated and not empty

    **Business Value:**
    Core functionality for user onboarding and account creation.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://reqres.in/api-docs/#/Auth/Register", name="API Docs")
    @pytest.mark.testcase("TC-RR-022")
    @pytest.mark.requirement("US-AUTH-001")
    @pytest.mark.smoke
    def test_register_successful(self, reqres_client):
        """Test successful registration with defined user."""
        email = "eve.holt@reqres.in"
        password = "pistol"

        with allure.step(f"Register user with email {email}"):
            response = reqres_client.register(email=email, password=password)

        with allure.step("Verify registration response"):
            assert "id" in response
            assert "token" in response
            assert response["token"] is not None

    @allure.story("Register User")
    @allure.title("Register user fails without password")
    @allure.description_html(markdown_to_html("""
    Verify that registration fails with missing password.

    **Test Coverage:**
    - Validation error handling for missing password
    - Proper HTTP status code (400 Bad Request)
    - Error message clarity and accuracy

    **Business Value:**
    Ensures data integrity by preventing incomplete registrations.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-RR-023")
    @pytest.mark.requirement("US-AUTH-002")
    def test_register_unsuccessful(self, reqres_client):
        """Test registration failure without password."""
        email = "sydney@fife"

        with allure.step("Attempt registration without password"):
            with pytest.raises(HTTPError) as exc:
                reqres_client.register(email=email, password=None)

        with allure.step("Verify error response"):
            assert exc.value.response.status_code == 400
            assert exc.value.response.json()["error"] == "Missing password"

    @allure.story("Login")
    @allure.title("Login user successfully")
    @allure.description_html(markdown_to_html("""
    Verify that a registered user can login with valid credentials.

    **Test Coverage:**
    - User login with valid email and password
    - Response contains authentication token
    - Token is properly generated and not empty

    **Business Value:**
    Core authentication mechanism for user access to the system.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://reqres.in/api-docs/#/Auth/Login", name="API Docs")
    @pytest.mark.testcase("TC-RR-020")
    @pytest.mark.requirement("US-AUTH-003")
    @pytest.mark.smoke
    def test_login_successful(self, reqres_client):
        """Test successful login."""
        email = "eve.holt@reqres.in"
        password = "cityslicka"

        with allure.step(f"Login with email {email}"):
            response = reqres_client.login(email=email, password=password)

        with allure.step("Verify token is returned"):
            assert "token" in response
            assert response["token"] is not None

    @allure.story("Login")
    @allure.title("Login user fails without password")
    @allure.description_html(markdown_to_html("""
    Verify that login fails with missing password.

    **Test Coverage:**
    - Validation error handling for missing password
    - Proper HTTP status code (400 Bad Request)
    - Error message clarity and accuracy

    **Business Value:**
    Ensures security by preventing authentication with incomplete credentials.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-RR-021")
    @pytest.mark.requirement("US-AUTH-004")
    def test_login_unsuccessful(self, reqres_client):
        """Test login failure without password."""
        email = "peter@klaven"

        with allure.step("Attempt login without password"):
            with pytest.raises(HTTPError) as exc:
                reqres_client.login(email=email, password=None)

        with allure.step("Verify error response"):
            assert exc.value.response.status_code == 400
            assert exc.value.response.json()["error"] == "Missing password"
