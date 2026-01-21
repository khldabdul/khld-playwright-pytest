"""Petstore API - Pet Tests."""

import pytest
import allure
import random
import string
from typing import Any

from requests import HTTPError


def generate_random_string(length: int = 8) -> str:
    """Generate random string."""
    return ''.join(random.choices(string.ascii_letters, k=length))


@allure.feature("Petstore API")
@allure.story("Pet Management")
@pytest.mark.app("petstore")
@pytest.mark.api
class TestPetstorePets:
    """Test suite for Petstore Pet operations."""

    @pytest.fixture
    def new_pet(self, petstore_client) -> dict[str, Any]:
        """Fixture to create a new pet and clean it up."""
        pet_id = random.randint(100000, 999999)
        name = f"pet_{generate_random_string()}"
        
        pet_data = {
            "id": pet_id,
            "category": {"id": 1, "name": "dogs"},
            "name": name,
            "photoUrls": ["https://example.com/photo.jpg"],
            "tags": [{"id": 1, "name": "friendly"}],
            "status": "available"
        }
        
        pet = petstore_client.add_pet(pet_data)
        yield pet
        
        # Cleanup
        try:
            petstore_client.delete_pet(pet_id)
        except:
            pass

    @allure.title("Add new pet")
    @pytest.mark.testcase("TC-PS-001")
    @pytest.mark.smoke
    def test_add_pet(self, petstore_client):
        """Test adding a new pet."""
        pet_id = random.randint(100000, 999999)
        name = f"pet_{generate_random_string()}"
        
        pet_data = {
            "id": pet_id,
            "category": {"id": 1, "name": "cats"},
            "name": name,
            "photoUrls": [],
            "tags": [],
            "status": "available"
        }
        
        response = petstore_client.add_pet(pet_data)
        
        assert response["id"] == pet_id
        assert response["name"] == name
        assert response["status"] == "available"
        
        # Cleanup
        petstore_client.delete_pet(pet_id)

    @allure.title("Get pet by ID")
    @pytest.mark.testcase("TC-PS-002")
    @pytest.mark.smoke
    def test_get_pet(self, petstore_client, new_pet):
        """Test retrieving a pet by ID."""
        pet_id = new_pet["id"]
        
        response = petstore_client.get_pet(pet_id)
        
        assert response["id"] == pet_id
        assert response["name"] == new_pet["name"]

    @allure.title("Update pet")
    @pytest.mark.testcase("TC-PS-004")
    def test_update_pet(self, petstore_client, new_pet):
        """Test updating a pet."""
        new_pet["status"] = "sold"
        new_pet["name"] = f"sold_{new_pet['name']}"
        
        response = petstore_client.update_pet(new_pet)
        
        assert response["status"] == "sold"
        assert response["name"] == new_pet["name"]
        
        # Verify update with get
        updated = petstore_client.get_pet(new_pet["id"])
        assert updated["status"] == "sold"

    @allure.title("Find pets by status")
    @pytest.mark.testcase("TC-PS-006")
    def test_find_pets_by_status(self, petstore_client):
        """Test finding pets by status."""
        status = "available"
        
        pets = petstore_client.find_pets_by_status(status)
        
        assert len(pets) > 0
        assert pets[0]["status"] == status

    @allure.title("Delete pet")
    @pytest.mark.testcase("TC-PS-005")
    def test_delete_pet(self, petstore_client):
        """Test deleting a pet."""
        # Create a pet specifically to delete
        pet_id = random.randint(100000, 999999)
        pet_data = {
            "id": pet_id,
            "name": "delete_me",
            "photoUrls": [],
            "status": "available"
        }
        petstore_client.add_pet(pet_data)
        
        # Delete it
        assert petstore_client.delete_pet(pet_id) is True
        
        # Verify it's gone
        with pytest.raises(HTTPError) as exc:
            petstore_client.get_pet(pet_id)
        assert exc.value.response.status_code == 404
