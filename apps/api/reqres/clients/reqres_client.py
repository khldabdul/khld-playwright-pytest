"""ReqRes API Client.

This module provides a client for interacting with the ReqRes API.
"""

from __future__ import annotations

from typing import Any

import allure
import requests


class ReqResClient:
    """Client for ReqRes API operations."""

    def __init__(self, base_url: str, api_key: str | None = None):
        """
        Initialize the ReqRes API client.

        Args:
            base_url: Base URL for the API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        
        # Add API key if provided
        if api_key:
            headers["x-api-key"] = api_key
            
        self.session.headers.update(headers)

    @allure.step("Get users list (page: {page})")
    def get_users(self, page: int = 1) -> dict[str, Any]:
        """
        Get paginated list of users.

        Args:
            page: Page number

        Returns:
            Response with users list and pagination info
        """
        response = self.session.get(f"{self.base_url}/api/users", params={"page": page})
        response.raise_for_status()
        return response.json()

    @allure.step("Get single user: {user_id}")
    def get_user(self, user_id: int) -> dict[str, Any]:
        """
        Get a single user by ID.

        Args:
            user_id: User ID

        Returns:
            User data
        """
        response = self.session.get(f"{self.base_url}/api/users/{user_id}")
        response.raise_for_status()
        return response.json()

    @allure.step("Create user")
    def create_user(self, name: str, job: str) -> dict[str, Any]:
        """
        Create a new user.

        Args:
            name: User name
            job: User job title

        Returns:
            Created user with id and createdAt
        """
        response = self.session.post(
            f"{self.base_url}/api/users",
            json={"name": name, "job": job}
        )
        response.raise_for_status()
        result = response.json()

        allure.attach(
            str(result),
            name="Created User",
            attachment_type=allure.attachment_type.JSON
        )
        return result

    @allure.step("Update user: {user_id}")
    def update_user(self, user_id: int, name: str, job: str) -> dict[str, Any]:
        """
        Update a user (PUT).

        Args:
            user_id: User ID
            name: Updated name
            job: Updated job

        Returns:
            Updated user data
        """
        response = self.session.put(
            f"{self.base_url}/api/users/{user_id}",
            json={"name": name, "job": job}
        )
        response.raise_for_status()
        return response.json()

    @allure.step("Partially update user: {user_id}")
    def patch_user(self, user_id: int, **fields) -> dict[str, Any]:
        """
        Partially update a user (PATCH).

        Args:
            user_id: User ID
            **fields: Fields to update

        Returns:
            Updated user data
        """
        response = self.session.patch(
            f"{self.base_url}/api/users/{user_id}",
            json=fields
        )
        response.raise_for_status()
        return response.json()

    @allure.step("Delete user: {user_id}")
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID

        Returns:
            True if successful
        """
        response = self.session.delete(f"{self.base_url}/api/users/{user_id}")
        return response.status_code == 204

    @allure.step("Register user")
    def register(self, email: str, password: str) -> dict[str, Any]:
        """
        Register a new user.

        Args:
            email: User email
            password: User password

        Returns:
            Registration response with id and token

        Raises:
            requests.HTTPError: If registration fails
        """
        response = self.session.post(
            f"{self.base_url}/api/register",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()

    @allure.step("Login user")
    def login(self, email: str, password: str) -> dict[str, Any]:
        """
        Login a user.

        Args:
            email: User email
            password: User password

        Returns:
            Login response with token

        Raises:
            requests.HTTPError: If login fails
        """
        response = self.session.post(
            f"{self.base_url}/api/login",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()

    @allure.step("Get resources list")
    def get_resources(self) -> dict[str, Any]:
        """
        Get list of resources.

        Returns:
            Response with resources list
        """
        response = self.session.get(f"{self.base_url}/api/unknown")
        response.raise_for_status()
        return response.json()

    @allure.step("Get single resource: {resource_id}")
    def get_resource(self, resource_id: int) -> dict[str, Any]:
        """
        Get a single resource by ID.

        Args:
            resource_id: Resource ID

        Returns:
            Resource data
        """
        response = self.session.get(f"{self.base_url}/api/unknown/{resource_id}")
        response.raise_for_status()
        return response.json()
