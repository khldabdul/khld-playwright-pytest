"""Restful Booker API - Authentication Tests."""

import allure
import pytest


@allure.epic("Restful Booker API")
@allure.feature("Authentication")
@pytest.mark.api
class TestAuthentication:
    """Test suite for Restful Booker authentication."""

    @allure.story("Health Check")
    @allure.title("API is responsive")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.testcase("TC-RB-001")
    @pytest.mark.smoke
    def test_ping_service(self, restful_booker_client):
        """Test that the API health check endpoint responds."""
        with allure.step("Ping the API"):
            is_alive = restful_booker_client.ping()

        with allure.step("Verify API is responsive"):
            assert is_alive is True, "API should respond to ping"

    @allure.story("Token Creation")
    @allure.title("Create token with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.testcase("TC-RB-010")
    @pytest.mark.smoke
    def test_create_token_valid_credentials(self, restful_booker_client):
        """Test successful token creation with valid credentials."""
        with allure.step("Create token with admin/password123"):
            token = restful_booker_client.create_token()

        with allure.step("Verify token is returned"):
            assert token is not None, "Token should be returned"
            assert isinstance(token, str), "Token should be a string"
            assert len(token) > 0, "Token should not be empty"

    @allure.story("Token Creation")
    @allure.title("Create token fails with invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-RB-011")
    @pytest.mark.regression
    def test_create_token_invalid_credentials(self, restful_booker_client):
        """Test that token creation fails with invalid credentials."""
        with allure.step("Attempt to create token with wrong password"):
            with pytest.raises(ValueError, match="Authentication failed"):
                restful_booker_client.create_token(username="admin", password="wrong")
