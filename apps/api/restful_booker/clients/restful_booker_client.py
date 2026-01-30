"""Restful Booker API Client.

This module provides a client for interacting with the Restful Booker API.
"""

from __future__ import annotations

from typing import Any

import allure
import requests


class RestfulBookerClient:
    """Client for Restful Booker API operations."""

    def __init__(self, base_url: str):
        """
        Initialize the Restful Booker API client.

        Args:
            base_url: Base URL for the API
        """
        self.base_url = base_url.rstrip("/")
        self.token: str | None = None
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    @allure.step("Ping API health check")
    def ping(self) -> bool:
        """
        Ping the API to check if it's running.

        Returns:
            True if API is responsive
        """
        response = self.session.get(f"{self.base_url}/ping")
        return response.status_code == 201

    @allure.step("Create authentication token")
    def create_token(self, username: str = "admin", password: str = "password123") -> str:
        """
        Create an authentication token.

        Args:
            username: Username for authentication
            password: Password for authentication

        Returns:
            Authentication token

        Raises:
            ValueError: If authentication fails
        """
        response = self.session.post(
            f"{self.base_url}/auth",
            json={"username": username, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                self.token = data["token"]
                allure.attach(
                    self.token,
                    name="Auth Token",
                    attachment_type=allure.attachment_type.TEXT
                )
                return self.token
            else:
                reason = data.get("reason", "Unknown error")
                raise ValueError(f"Authentication failed: {reason}")
        else:
            raise ValueError(f"Authentication request failed: {response.status_code}")

    @allure.step("Get all booking IDs")
    def get_bookings(self, **filters) -> list[dict[str, int]]:
        """
        Get all booking IDs, optionally filtered.

        Args:
            **filters: Query parameters for filtering (firstname, lastname, checkin, checkout)

        Returns:
            List of booking objects with bookingid
        """
        response = self.session.get(f"{self.base_url}/booking", params=filters)
        response.raise_for_status()
        return response.json()

    @allure.step("Get booking by ID: {booking_id}")
    def get_booking(self, booking_id: int) -> dict[str, Any]:
        """
        Get a specific booking by ID.

        Args:
            booking_id: Booking ID

        Returns:
            Booking details
        """
        response = self.session.get(f"{self.base_url}/booking/{booking_id}")
        response.raise_for_status()
        return response.json()

    @allure.step("Create new booking")
    def create_booking(self, booking_data: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new booking.

        Args:
            booking_data: Booking details

        Returns:
            Created booking with bookingid
        """
        response = self.session.post(
            f"{self.base_url}/booking",
            json=booking_data
        )
        response.raise_for_status()
        result = response.json()

        allure.attach(
            str(result),
            name="Created Booking",
            attachment_type=allure.attachment_type.JSON
        )
        return result

    @allure.step("Update booking: {booking_id}")
    def update_booking(self, booking_id: int, booking_data: dict[str, Any]) -> dict[str, Any]:
        """
        Update an existing booking (PUT - full update).

        Args:
            booking_id: Booking ID
            booking_data: Complete booking details

        Returns:
            Updated booking details

        Raises:
            ValueError: If no token is set
        """
        if not self.token:
            raise ValueError("Token required for update. Call create_token() first.")

        response = self.session.put(
            f"{self.base_url}/booking/{booking_id}",
            json=booking_data,
            cookies={"token": self.token}
        )
        response.raise_for_status()
        return response.json()

    @allure.step("Partially update booking: {booking_id}")
    def partial_update_booking(self, booking_id: int, partial_data: dict[str, Any]) -> dict[str, Any]:
        """
        Partially update an existing booking (PATCH).

        Args:
            booking_id: Booking ID
            partial_data: Partial booking details to update

        Returns:
            Updated booking details

        Raises:
            ValueError: If no token is set
        """
        if not self.token:
            raise ValueError("Token required for update. Call create_token() first.")

        response = self.session.patch(
            f"{self.base_url}/booking/{booking_id}",
            json=partial_data,
            cookies={"token": self.token}
        )
        response.raise_for_status()
        return response.json()

    @allure.step("Delete booking: {booking_id}")
    def delete_booking(self, booking_id: int) -> bool:
        """
        Delete a booking.

        Args:
            booking_id: Booking ID

        Returns:
            True if deletion successful

        Raises:
            ValueError: If no token is set
        """
        if not self.token:
            raise ValueError("Token required for delete. Call create_token() first.")

        response = self.session.delete(
            f"{self.base_url}/booking/{booking_id}",
            cookies={"token": self.token}
        )

        return response.status_code == 201
