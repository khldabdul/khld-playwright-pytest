"""ReqRes API - User Tests."""

import pytest
import allure

@allure.feature("ReqRes API")
@allure.story("User Management")
@pytest.mark.app("reqres")
@pytest.mark.api
class TestReqResUsers:
    """Test suite for ReqRes user operations."""

    @allure.title("Get list of users")
    def test_get_users_list(self, reqres_client):
        """Test retrieving a paginated list of users."""
        response = reqres_client.get_users(page=2)
        
        assert response["page"] == 2
        assert len(response["data"]) > 0
        assert "total" in response
        assert "total_pages" in response
        
        # Verify user structure
        user = response["data"][0]
        assert "id" in user
        assert "email" in user
        assert "first_name" in user
        assert "last_name" in user
        assert "avatar" in user

    @allure.title("Get single user")
    def test_get_single_user(self, reqres_client):
        """Test retrieving a single user by ID."""
        user_id = 2
        response = reqres_client.get_user(user_id)
        
        user = response["data"]
        assert user["id"] == user_id
        assert user["email"] == "janet.weaver@reqres.in"
        assert "first_name" in user
        assert "last_name" in user

    @allure.title("Get user not found")
    def test_get_user_not_found(self, reqres_client):
        """Test retrieving a non-existent user returns 404."""
        import requests
        with pytest.raises(requests.HTTPError) as exc:
            reqres_client.get_user(23)
        assert exc.value.response.status_code == 404

    @allure.title("Create user")
    def test_create_user(self, reqres_client):
        """Test creating a new user."""
        name = "morpheus"
        job = "leader"
        
        response = reqres_client.create_user(name=name, job=job)
        
        assert response["name"] == name
        assert response["job"] == job
        assert "id" in response
        assert "createdAt" in response

    @allure.title("Update user (PUT)")
    def test_update_user(self, reqres_client):
        """Test updating a user with PUT."""
        user_id = 2
        name = "morpheus"
        job = "zion resident"
        
        response = reqres_client.update_user(user_id, name=name, job=job)
        
        assert response["name"] == name
        assert response["job"] == job
        assert "updatedAt" in response

    @allure.title("Update user (PATCH)")
    def test_patch_user(self, reqres_client):
        """Test partially updating a user with PATCH."""
        user_id = 2
        name = "morpheus"
        
        response = reqres_client.patch_user(user_id, name=name)
        
        assert response["name"] == name
        assert "updatedAt" in response

    @allure.title("Delete user")
    def test_delete_user(self, reqres_client):
        """Test deleting a user."""
        user_id = 2
        assert reqres_client.delete_user(user_id) is True
