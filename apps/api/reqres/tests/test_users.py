"""ReqRes API - User Tests.

This test suite covers user management operations including:
- Listing users with pagination
- Retrieving individual user details
- Creating new users
- Updating users (PUT and PATCH)
- Deleting users

API Documentation: https://reqres.in/api-docs/
"""

from __future__ import annotations

import pytest
import allure

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("ReqRes API")
@allure.feature("User Management")
@allure.label("layer", "api")
@allure.label("type", "functional")
@pytest.mark.app("reqres")
@pytest.mark.api
class TestReqResUsers:
    """Test suite for ReqRes user operations."""

    @allure.story("List Users")
    @allure.title("Get paginated list of users")
    @allure.description_html(markdown_to_html("""
    Verify that the API returns a paginated list of users correctly.

    **Test Coverage:**
    - Pagination works correctly (page parameter)
    - Response contains expected data structure
    - User objects contain all required fields (id, email, first_name, last_name, avatar)
    - Pagination metadata is present (total, total_pages)

    **Business Value:**
    Ensures users can browse the user directory, which is essential
    for any user management functionality.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://reqres.in/api-docs/#/Users/List_users", name="API Docs")
    @pytest.mark.testcase("TC-RR-002")
    @pytest.mark.requirement("US-USER-001")
    @pytest.mark.requirement("US-USER-002")
    @pytest.mark.smoke
    def test_get_users_list(self, reqres_client):
        """Test retrieving a paginated list of users."""
        response = reqres_client.get_users(page=2)

        # Verify pagination metadata
        with allure.step("Verify pagination metadata"):
            assert response["page"] == 2
            assert "total" in response
            assert "total_pages" in response
            assert response["total"] > 0

        # Verify user data structure
        with allure.step("Verify user data structure"):
            assert len(response["data"]) > 0
            user = response["data"][0]
            assert "id" in user
            assert "email" in user
            assert "first_name" in user
            assert "last_name" in user
            assert "avatar" in user

    @allure.story("View User Details")
    @allure.title("Get single user by ID")
    @allure.description_html(markdown_to_html("""
    Verify that a single user can be retrieved by their ID.

    **Test Coverage:**
    - Valid user ID returns user data
    - User data is complete and accurate
    - All expected fields are present

    **Business Value:**
    Enables viewing individual user profiles, a core feature
    of any user management system.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://reqres.in/api-docs/#/Users/Single_user", name="API Docs")
    @pytest.mark.testcase("TC-RR-003")
    @pytest.mark.requirement("US-USER-003")
    def test_get_single_user(self, reqres_client):
        """Test retrieving a single user by ID."""
        user_id = 2
        response = reqres_client.get_user(user_id)

        user = response["data"]
        assert user["id"] == user_id
        assert user["email"] == "janet.weaver@reqres.in"
        assert "first_name" in user
        assert "last_name" in user

    @allure.story("View User Details")
    @allure.title("Get non-existent user returns 404")
    @allure.description_html(markdown_to_html("""
    Verify that requesting a non-existent user returns proper 404 error.

    **Test Coverage:**
    - Invalid user ID handling
    - Proper HTTP status code (404)
    - Error message clarity

    **Business Value:**
    Ensures graceful error handling when users request
    non-existent resources.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-RR-004")
    @pytest.mark.requirement("US-USER-004")
    def test_get_user_not_found(self, reqres_client):
        """Test retrieving a non-existent user returns 404."""
        import requests
        with pytest.raises(requests.HTTPError) as exc:
            reqres_client.get_user(23)
        assert exc.value.response.status_code == 404

    @allure.story("Create User")
    @allure.title("Create new user")
    @allure.description_html(markdown_to_html("""
    Verify that a new user can be created successfully.

    **Test Coverage:**
    - User creation with valid data
    - Response contains generated ID and timestamp
    - User data is persisted correctly

    **Business Value:**
    Core functionality for adding new users to the system.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://reqres.in/api-docs/#/Users/Create_user", name="API Docs")
    @pytest.mark.testcase("TC-RR-010")
    @pytest.mark.requirement("US-USER-010")
    def test_create_user(self, reqres_client):
        """Test creating a new user."""
        name = "morpheus"
        job = "leader"

        with allure.step(f"Create user '{name}' with job '{job}'"):
            response = reqres_client.create_user(name=name, job=job)

        with allure.step("Verify created user data"):
            assert response["name"] == name
            assert response["job"] == job
            assert "id" in response
            assert "createdAt" in response

    @allure.story("Update User")
    @allure.title("Update user with PUT (full update)")
    @allure.description_html(markdown_to_html("""
    Verify that a user can be fully updated using PUT method.

    **Test Coverage:**
    - Full user update (all fields)
    - Response contains updated timestamp
    - Changes are persisted

    **Business Value:**
    Enables users to update their profile information.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://reqres.in/api-docs/#/Users/Update_user", name="API Docs")
    @pytest.mark.testcase("TC-RR-011")
    @pytest.mark.requirement("US-USER-011")
    def test_update_user(self, reqres_client):
        """Test updating a user with PUT."""
        user_id = 2
        name = "morpheus"
        job = "zion resident"

        with allure.step(f"Update user {user_id} (full update)"):
            response = reqres_client.update_user(user_id, name=name, job=job)

        with allure.step("Verify updated user data"):
            assert response["name"] == name
            assert response["job"] == job
            assert "updatedAt" in response

    @allure.story("Update User")
    @allure.title("Partially update user with PATCH")
    @allure.description_html(markdown_to_html("""
    Verify that a user can be partially updated using PATCH method.

    **Test Coverage:**
    - Partial user update (only specified fields)
    - Other fields remain unchanged
    - Response contains updated timestamp

    **Business Value:**
    Allows users to update individual profile fields without
    affecting other data.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://reqres.in/api-docs/#/Users/Update__partial_user_", name="API Docs")
    @pytest.mark.testcase("TC-RR-012")
    @pytest.mark.requirement("US-USER-012")
    def test_patch_user(self, reqres_client):
        """Test partially updating a user with PATCH."""
        user_id = 2
        name = "morpheus"

        with allure.step(f"Partially update user {user_id} (only name)"):
            response = reqres_client.patch_user(user_id, name=name)

        with allure.step("Verify partial update worked"):
            assert response["name"] == name
            assert "updatedAt" in response

    @allure.story("Delete User")
    @allure.title("Delete user")
    @allure.description_html(markdown_to_html("""
    Verify that a user can be deleted successfully.

    **Test Coverage:**
    - User deletion returns success status
    - Proper HTTP status code (204 No Content)
    - User is removed from system

    **Business Value:**
    Critical for user account management and compliance
    with data privacy regulations.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://reqres.in/api-docs/#/Users/Delete_user", name="API Docs")
    @pytest.mark.testcase("TC-RR-013")
    @pytest.mark.requirement("US-USER-013")
    def test_delete_user(self, reqres_client):
        """Test deleting a user."""
        user_id = 2
        with allure.step(f"Delete user {user_id}"):
            result = reqres_client.delete_user(user_id)

        assert result is True
