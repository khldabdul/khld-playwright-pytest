"""Petstore API - Store Tests."""

import pytest
import allure
import random
from typing import Any
from datetime import datetime, timezone

from requests import HTTPError


@allure.feature("Petstore API")
@allure.story("Store Operations")
@pytest.mark.app("petstore")
@pytest.mark.api
class TestPetstoreStore:
    """Test suite for Petstore Store operations."""

    @allure.title("Get inventory")
    @pytest.mark.testcase("TC-PS-020")
    def test_get_inventory(self, petstore_client):
        """Test retrieving store inventory."""
        inventory = petstore_client.get_inventory()
        
        assert isinstance(inventory, dict)
        assert len(inventory) > 0
        # Common keys usually present
        assert any(k in inventory for k in ["available", "pending", "sold"])

    @allure.title("Place order")
    @pytest.mark.testcase("TC-PS-021")
    def test_place_order(self, petstore_client):
        """Test placing an order."""
        order_id = random.randint(1, 9999)
        pet_id = random.randint(100000, 999999)
        
        order_data = {
            "id": order_id,
            "petId": pet_id,
            "quantity": 1,
            "shipDate": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "placed",
            "complete": True
        }
        
        response = petstore_client.place_order(order_data)
        
        assert response["id"] == order_id
        assert response["petId"] == pet_id
        assert response["status"] == "placed"
        assert response["complete"] is True
        
        # Cleanup
        petstore_client.delete_order(order_id)

    @allure.title("Get order by ID")
    @pytest.mark.testcase("TC-PS-022")
    def test_get_order(self, petstore_client):
        """Test retrieving an order by ID."""
        # Setup: Place an order
        order_id = random.randint(1, 9999)
        pet_id = random.randint(100000, 999999)
        
        order_data = {
            "id": order_id,
            "petId": pet_id,
            "quantity": 1,
            "shipDate": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "approved",
            "complete": True
        }
        
        petstore_client.place_order(order_data)
        
        # Test
        response = petstore_client.get_order(order_id)
        
        assert response["id"] == order_id
        assert response["petId"] == pet_id
        assert response["status"] == "approved"
        
        # Cleanup
        petstore_client.delete_order(order_id)

    @allure.title("Delete order")
    @pytest.mark.testcase("TC-PS-023")
    def test_delete_order(self, petstore_client):
        """Test deleting an order."""
        # Setup: Place an order
        order_id = random.randint(1, 9999)
        pet_id = random.randint(100000, 999999)
        
        order_data = {
            "id": order_id,
            "petId": pet_id,
            "quantity": 1,
            "shipDate": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "delivered",
            "complete": True
        }
        
        petstore_client.place_order(order_data)
        
        # Test
        assert petstore_client.delete_order(order_id) is True
        
        # Verify it's gone
        with pytest.raises(HTTPError) as exc:
            petstore_client.get_order(order_id)
        assert exc.value.response.status_code == 404
