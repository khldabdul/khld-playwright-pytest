"""Petstore API - Store Tests.

This test suite covers store order operations including:
- Viewing store inventory
- Placing new orders
- Retrieving orders by ID
- Deleting orders

API Documentation: https://petstore.swagger.io/
"""

from __future__ import annotations

import pytest
import allure
import random
from typing import Any
from datetime import datetime, timezone

from requests import HTTPError

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("Petstore API")
@allure.feature("Store Operations")
@allure.label("layer", "api")
@allure.label("type", "functional")
@pytest.mark.app("petstore")
@pytest.mark.api
class TestPetstoreStore:
    """Test suite for Petstore Store operations."""

    @allure.story("View Inventory")
    @allure.title("Get store inventory")
    @allure.description_html(markdown_to_html("""
    Verify that the store inventory can be retrieved.

    **Test Coverage:**
    - Retrieve inventory counts by status
    - Response contains status categories
    - Data structure is correct

    **Business Value:**
    Essential for monitoring store inventory levels.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://petstore.swagger.io/#/store/getInventory", name="API Docs")
    @pytest.mark.testcase("TC-PS-020")
    @pytest.mark.requirement("US-STORE-001")
    @pytest.mark.smoke
    def test_get_inventory(self, petstore_client):
        """Test retrieving store inventory."""
        with allure.step("Get store inventory"):
            inventory = petstore_client.get_inventory()

        with allure.step("Verify inventory data"):
            assert isinstance(inventory, dict)
            assert len(inventory) > 0
            # Common keys usually present
            assert any(k in inventory for k in ["available", "pending", "sold"])

    @allure.story("Create Order")
    @allure.title("Place new order")
    @allure.description_html(markdown_to_html("""
    Verify that a new order can be placed successfully.

    **Test Coverage:**
    - Order creation with valid data
    - Response contains order ID and details
    - Order data is persisted correctly

    **Business Value:**
    Core functionality for processing customer orders.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://petstore.swagger.io/#/store/placeOrder", name="API Docs")
    @pytest.mark.testcase("TC-PS-021")
    @pytest.mark.requirement("US-STORE-002")
    @pytest.mark.smoke
    def test_place_order(self, petstore_client):
        """Test placing an order."""
        order_id = random.randint(1, 9999)
        pet_id = random.randint(100000, 999999)

        with allure.step("Place order"):
            order_data = {
                "id": order_id,
                "petId": pet_id,
                "quantity": 1,
                "shipDate": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "status": "placed",
                "complete": True
            }
            response = petstore_client.place_order(order_data)

        with allure.step("Verify order was placed"):
            assert response["id"] == order_id
            assert response["petId"] == pet_id
            assert response["status"] == "placed"
            assert response["complete"] is True

        # Cleanup
        petstore_client.delete_order(order_id)

    @allure.story("View Order Details")
    @allure.title("Get order by ID")
    @allure.description_html(markdown_to_html("""
    Verify that an order can be retrieved by its ID.

    **Test Coverage:**
    - Retrieve order by ID
    - All order fields are present
    - Data accuracy is maintained

    **Business Value:**
    Essential for viewing order details and tracking.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://petstore.swagger.io/#/store/getOrderById", name="API Docs")
    @pytest.mark.testcase("TC-PS-022")
    @pytest.mark.requirement("US-STORE-003")
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

        with allure.step("Setup: Place test order"):
            petstore_client.place_order(order_data)

        with allure.step("Get order by ID"):
            response = petstore_client.get_order(order_id)

        with allure.step("Verify order details"):
            assert response["id"] == order_id
            assert response["petId"] == pet_id
            assert response["status"] == "approved"

        # Cleanup
        petstore_client.delete_order(order_id)

    @allure.story("Delete Order")
    @allure.title("Delete order")
    @allure.description_html(markdown_to_html("""
    Verify that an order can be deleted successfully.

    **Test Coverage:**
    - Order deletion returns success
    - Deleted order is no longer accessible
    - Proper HTTP status code (404) for deleted orders

    **Business Value:**
    Critical for order management and cancellation.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://petstore.swagger.io/#/store/deleteOrder", name="API Docs")
    @pytest.mark.testcase("TC-PS-023")
    @pytest.mark.requirement("US-STORE-004")
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

        with allure.step("Setup: Place test order"):
            petstore_client.place_order(order_data)

        with allure.step(f"Delete order {order_id}"):
            assert petstore_client.delete_order(order_id) is True

        with allure.step("Verify order no longer exists"):
            with pytest.raises(HTTPError) as exc:
                petstore_client.get_order(order_id)
            assert exc.value.response.status_code == 404
