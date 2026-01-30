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

from infrastructure.utils.allure_helpers import api_test


@allure.epic("ReqRes API")
@allure.feature("Authentication")
@allure.label("layer", "api")
@allure.label("type", "functional")
@pytest.mark.app("reqres")
@pytest.mark.api
class TestReqResAuth:
    """Test suite for ReqRes authentication."""

    @api_test(
        epic="ReqRes API",
        feature="Authentication",
        story="Register User",
        testcase="TC-RR-022",
        requirement="US-AUTH-001",
        severity=allure.severity_level.CRITICAL,
        title="Register new user successfully",
        link="https://reqres.in/api-docs/#/Auth/Register",
        link_name="API Docs",
        smoke=True,
        description="""
        Verify that a new user can be registered with valid credentials.

        **Test Coverage:**
        - User registration with valid email and password
        - Response contains user ID and authentication token
        - Token is properly generated and not empty

        **Business Value:**
        Core functionality for user onboarding and account creation.
        """,
    )
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

    @api_test(
        epic="ReqRes API",
        feature="Authentication",
        story="Register User",
        testcase="TC-RR-023",
        requirement="US-AUTH-002",
        severity=allure.severity_level.NORMAL,
        title="Register user fails without password",
        description="""
        Verify that registration fails with missing password.

        **Test Coverage:**
        - Validation error handling for missing password
        - Proper HTTP status code (400 Bad Request)
        - Error message clarity and accuracy

        **Business Value:**
        Ensures data integrity by preventing incomplete registrations.
        """,
    )
    def test_register_unsuccessful(self, reqres_client):
        """Test registration failure without password."""
        email = "sydney@fife"

        with allure.step("Attempt registration without password"):
            with pytest.raises(HTTPError) as exc:
                reqres_client.register(email=email, password=None)

        with allure.step("Verify error response"):
            assert exc.value.response.status_code == 400
            assert exc.value.response.json()["error"] == "Missing password"

    @api_test(
        epic="ReqRes API",
        feature="Authentication",
        story="Login",
        testcase="TC-RR-020",
        requirement="US-AUTH-003",
        severity=allure.severity_level.CRITICAL,
        title="Login user successfully",
        link="https://reqres.in/api-docs/#/Auth/Login",
        link_name="API Docs",
        smoke=True,
        description="""
        Verify that a registered user can login with valid credentials.

        **Test Coverage:**
        - User login with valid email and password
        - Response contains authentication token
        - Token is properly generated and not empty

        **Business Value:**
        Core authentication mechanism for user access to the system.
        """,
    )
    def test_login_successful(self, reqres_client):
        """Test successful login."""
        email = "eve.holt@reqres.in"
        password = "cityslicka"

        with allure.step(f"Login with email {email}"):
            response = reqres_client.login(email=email, password=password)

        with allure.step("Verify token is returned"):
            assert "token" in response
            assert response["token"] is not None

    @api_test(
        epic="ReqRes API",
        feature="Authentication",
        story="Login",
        testcase="TC-RR-021",
        requirement="US-AUTH-004",
        severity=allure.severity_level.NORMAL,
        title="Login user fails without password",
        description="""
        Verify that login fails with missing password.

        **Test Coverage:**
        - Validation error handling for missing password
        - Proper HTTP status code (400 Bad Request)
        - Error message clarity and accuracy

        **Business Value:**
        Ensures security by preventing authentication with incomplete credentials.
        """,
    )
    def test_login_unsuccessful(self, reqres_client):
        """Test login failure without password."""
        email = "peter@klaven"

        with allure.step("Attempt login without password"):
            with pytest.raises(HTTPError) as exc:
                reqres_client.login(email=email, password=None)

        with allure.step("Verify error response"):
            assert exc.value.response.status_code == 400
            assert exc.value.response.json()["error"] == "Missing password"
