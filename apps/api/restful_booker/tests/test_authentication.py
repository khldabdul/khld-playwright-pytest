"""Restful Booker API - Authentication Tests.

This test suite covers authentication operations including:
- API health check
- Token creation with valid credentials
- Token creation failure with invalid credentials

API Documentation: https://restful-booker.herokuapp.com/apidoc/index.html
"""

from __future__ import annotations

import allure
import pytest

from infrastructure.utils.allure_helpers import api_test


@allure.epic("Restful Booker API")
@allure.feature("Authentication")
@allure.label("layer", "api")
@allure.label("type", "functional")
@pytest.mark.app("restful_booker")
@pytest.mark.api
class TestAuthentication:
    """Test suite for Restful Booker authentication."""

    @api_test(
        epic="Restful Booker API",
        feature="Authentication",
        story="Health Check",
        testcase="TC-RB-001",
        requirement="US-AUTH-001",
        severity=allure.severity_level.CRITICAL,
        title="API health check - ping service",
        smoke=True,
        description="""
        Verify that the API service is responsive and available.

        **Test Coverage:**
        - API health check endpoint
        - Service availability verification
        - Basic connectivity check

        **Business Value:**
        Critical for monitoring API availability and uptime.
        """,
    )
    def test_ping_service(self, restful_booker_client):
        """Test that the API health check endpoint responds."""
        with allure.step("Ping the API"):
            is_alive = restful_booker_client.ping()

        with allure.step("Verify API is responsive"):
            assert is_alive is True, "API should respond to ping"

    @api_test(
        epic="Restful Booker API",
        feature="Authentication",
        story="Token Creation",
        testcase="TC-RB-010",
        requirement="US-AUTH-002",
        severity=allure.severity_level.CRITICAL,
        title="Create authentication token with valid credentials",
        link="https://restful-booker.herokuapp.com/apidoc/index.html#header-Auth",
        link_name="API Docs",
        smoke=True,
        description="""
        Verify that an authentication token can be created with valid credentials.

        **Test Coverage:**
        - Token creation with valid credentials
        - Token format validation
        - Token is properly generated

        **Business Value:**
        Core authentication mechanism for secure API access.
        """,
    )
    def test_create_token_valid_credentials(self, restful_booker_client):
        """Test successful token creation with valid credentials."""
        with allure.step("Create token with admin/password123"):
            token = restful_booker_client.create_token()

        with allure.step("Verify token is returned"):
            assert token is not None, "Token should be returned"
            assert isinstance(token, str), "Token should be a string"
            assert len(token) > 0, "Token should not be empty"

    @api_test(
        epic="Restful Booker API",
        feature="Authentication",
        story="Token Creation",
        testcase="TC-RB-011",
        requirement="US-AUTH-003",
        severity=allure.severity_level.NORMAL,
        title="Token creation fails with invalid credentials",
        regression=True,
        description="""
        Verify that token creation fails with invalid credentials.

        **Test Coverage:**
        - Authentication failure handling
        - Invalid credential rejection
        - Error message clarity

        **Business Value:**
        Ensures security by rejecting invalid authentication attempts.
        """,
    )
    def test_create_token_invalid_credentials(self, restful_booker_client):
        """Test that token creation fails with invalid credentials."""
        with allure.step("Attempt to create token with wrong password"):
            with pytest.raises(ValueError, match="Authentication failed"):
                restful_booker_client.create_token(username="admin", password="wrong")
