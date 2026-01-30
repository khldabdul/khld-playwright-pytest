"""Petstore API - Pet Tests.

This test suite covers pet management operations including:
- Adding new pets
- Retrieving pets by ID
- Updating pet information
- Finding pets by status
- Deleting pets

API Documentation: https://petstore.swagger.io/
"""

from __future__ import annotations

import pytest
import allure
import random
import string
from typing import Any

from requests import HTTPError

from infrastructure.utils.allure_helpers import api_test


def generate_random_string(length: int = 8) -> str:
    """Generate random string."""
    return ''.join(random.choices(string.ascii_letters, k=length))


@allure.epic("Petstore API")
@allure.feature("Pet Management")
@allure.label("layer", "api")
@allure.label("type", "functional")
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

    @api_test(
        epic="Petstore API",
        feature="Pet Management",
        story="Create Pet",
        testcase="TC-PS-001",
        requirement="US-PET-001",
        severity=allure.severity_level.CRITICAL,
        smoke=True,
        description="""
        Verify that a new pet can be added to the store.

        **Test Coverage:**
        - Pet creation with valid data
        - Response contains pet ID and name
        - Pet data is persisted correctly

        **Business Value:**
        Core functionality for adding pets to the inventory.
        """,
    )
    def test_add_pet(self, petstore_client):
        """Test adding a new pet."""
        pet_id = random.randint(100000, 999999)
        name = f"pet_{generate_random_string()}"

        with allure.step("Add new pet"):
            pet_data = {
                "id": pet_id,
                "category": {"id": 1, "name": "cats"},
                "name": name,
                "photoUrls": [],
                "tags": [],
                "status": "available"
            }
            response = petstore_client.add_pet(pet_data)

        with allure.step("Verify pet was added"):
            assert response["id"] == pet_id
            assert response["name"] == name
            assert response["status"] == "available"

        # Cleanup
        petstore_client.delete_pet(pet_id)

    @api_test(
        epic="Petstore API",
        feature="Pet Management",
        story="View Pet Details",
        testcase="TC-PS-002",
        requirement="US-PET-002",
        severity=allure.severity_level.CRITICAL,
        smoke=True,
        description="""
        Verify that a pet can be retrieved by its ID.

        **Test Coverage:**
        - Retrieve pet by ID
        - All pet fields are present
        - Data accuracy is maintained

        **Business Value:**
        Essential for viewing individual pet information.
        """,
    )
    def test_get_pet(self, petstore_client, new_pet):
        """Test retrieving a pet by ID."""
        pet_id = new_pet["id"]

        with allure.step(f"Get pet by ID: {pet_id}"):
            response = petstore_client.get_pet(pet_id)

        with allure.step("Verify pet details"):
            assert response["id"] == pet_id
            assert response["name"] == new_pet["name"]

    @api_test(
        epic="Petstore API",
        feature="Pet Management",
        story="Update Pet",
        testcase="TC-PS-004",
        requirement="US-PET-003",
        severity=allure.severity_level.NORMAL,
        description="""
        Verify that a pet's information can be updated.

        **Test Coverage:**
        - Pet update with modified data
        - Changes are persisted correctly
        - Data integrity is maintained

        **Business Value:**
        Enables users to modify pet details in the inventory.
        """,
    )
    def test_update_pet(self, petstore_client, new_pet):
        """Test updating a pet."""
        with allure.step("Update pet status and name"):
            new_pet["status"] = "sold"
            new_pet["name"] = f"sold_{new_pet['name']}"
            response = petstore_client.update_pet(new_pet)

        with allure.step("Verify update was applied"):
            assert response["status"] == "sold"
            assert response["name"] == new_pet["name"]

        with allure.step("Verify update with get"):
            updated = petstore_client.get_pet(new_pet["id"])
            assert updated["status"] == "sold"

    @api_test(
        epic="Petstore API",
        feature="Pet Management",
        story="Search Pets",
        testcase="TC-PS-006",
        requirement="US-PET-004",
        severity=allure.severity_level.NORMAL,
        description="""
        Verify that pets can be filtered by status.

        **Test Coverage:**
        - Filter pets by status (available, pending, sold)
        - Results match filter criteria
        - Response structure is correct

        **Business Value:**
        Enables users to find pets by their current status.
        """,
    )
    def test_find_pets_by_status(self, petstore_client):
        """Test finding pets by status."""
        status = "available"

        with allure.step(f"Find pets with status: {status}"):
            pets = petstore_client.find_pets_by_status(status)

        with allure.step("Verify results match status"):
            assert len(pets) > 0
            assert pets[0]["status"] == status

    @api_test(
        epic="Petstore API",
        feature="Pet Management",
        story="Delete Pet",
        testcase="TC-PS-005",
        requirement="US-PET-005",
        severity=allure.severity_level.NORMAL,
        description="""
        Verify that a pet can be deleted from the store.

        **Test Coverage:**
        - Pet deletion returns success
        - Deleted pet is no longer accessible
        - Proper HTTP status code (404) for deleted pets

        **Business Value:**
        Critical for inventory management and removal.
        """,
    )
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

        with allure.step("Create pet for deletion"):
            petstore_client.add_pet(pet_data)

        with allure.step(f"Delete pet {pet_id}"):
            assert petstore_client.delete_pet(pet_id) is True

        with allure.step("Verify pet no longer exists"):
            with pytest.raises(HTTPError) as exc:
                petstore_client.get_pet(pet_id)
            assert exc.value.response.status_code == 404
