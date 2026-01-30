"""Petstore API Client.

This module provides a client for interacting with the Swagger Petstore API.
"""

from __future__ import annotations

from typing import Any

import allure
import requests


class PetstoreClient:
    """Client for Petstore API operations."""

    def __init__(self, base_url: str, api_key: str | None = None):
        """
        Initialize the Petstore API client.

        Args:
            base_url: Base URL for the API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            # Standard browser User-Agent to avoid potential blocking
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        })
        
        if api_key:
            self.session.headers.update({"api_key": api_key})

    @allure.step("Add new pet")
    def add_pet(self, pet_data: dict[str, Any]) -> dict[str, Any]:
        """
        Add a new pet to the store.

        Args:
            pet_data: Pet object that needs to be added to the store

        Returns:
            Created pet data
        """
        response = self.session.post(f"{self.base_url}/pet", json=pet_data)
        response.raise_for_status()
        return response.json()

    @allure.step("Update pet")
    def update_pet(self, pet_data: dict[str, Any]) -> dict[str, Any]:
        """
        Update an existing pet.

        Args:
            pet_data: Pet object that needs to be added to the store

        Returns:
            Updated pet data
        """
        response = self.session.put(f"{self.base_url}/pet", json=pet_data)
        response.raise_for_status()
        return response.json()

    @allure.step("Get pet by ID: {pet_id}")
    def get_pet(self, pet_id: int) -> dict[str, Any]:
        """
        Find pet by ID.

        Args:
            pet_id: ID of pet to return

        Returns:
            Pet data
        """
        response = self.session.get(f"{self.base_url}/pet/{pet_id}")
        response.raise_for_status()
        return response.json()

    @allure.step("Find pets by status: {status}")
    def find_pets_by_status(self, status: str) -> list[dict[str, Any]]:
        """
        Finds Pets by status.

        Args:
            status: Status values that need to be considered for filter (available, pending, sold)

        Returns:
            List of pets
        """
        response = self.session.get(
            f"{self.base_url}/pet/findByStatus",
            params={"status": status}
        )
        response.raise_for_status()
        return response.json()

    @allure.step("Delete pet: {pet_id}")
    def delete_pet(self, pet_id: int) -> bool:
        """
        Deletes a pet.

        Args:
            pet_id: Pet id to delete

        Returns:
            True if successful
        """
        response = self.session.delete(f"{self.base_url}/pet/{pet_id}")
        return response.status_code == 200

    @allure.step("Place an order")
    def place_order(self, order_data: dict[str, Any]) -> dict[str, Any]:
        """
        Place an order for a pet.

        Args:
            order_data: Order object

        Returns:
            Created order data
        """
        response = self.session.post(f"{self.base_url}/store/order", json=order_data)
        response.raise_for_status()
        return response.json()

    @allure.step("Get order by ID: {order_id}")
    def get_order(self, order_id: int) -> dict[str, Any]:
        """
        Find purchase order by ID.

        Args:
            order_id: ID of pet that needs to be fetched

        Returns:
            Order data
        """
        response = self.session.get(f"{self.base_url}/store/order/{order_id}")
        response.raise_for_status()
        return response.json()

    @allure.step("Delete order: {order_id}")
    def delete_order(self, order_id: int) -> bool:
        """
        Delete purchase order by ID.

        Args:
            order_id: ID of the order that needs to be deleted

        Returns:
            True if successful
        """
        response = self.session.delete(f"{self.base_url}/store/order/{order_id}")
        return response.status_code == 200

    @allure.step("Get inventory")
    def get_inventory(self) -> dict[str, int]:
        """
        Returns a map of status codes to quantities.

        Returns:
            Inventory map
        """
        response = self.session.get(f"{self.base_url}/store/inventory")
        response.raise_for_status()
        return response.json()
