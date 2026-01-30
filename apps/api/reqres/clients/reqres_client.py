"""ReqRes API Client.

This module provides a client for interacting with the ReqRes API.
Enhanced with Allure reporting for request/response logging and performance tracking.
"""

from __future__ import annotations

from typing import Any

import allure

from infrastructure.utils.base_api_client import BaseAPIClient


class ReqResClient(BaseAPIClient):
    """Client for ReqRes API operations with Allure reporting."""

    # Performance thresholds for ReqRes API (very fast, so lower thresholds)
    DEFAULT_THRESHOLD_MS = 500
    SLOW_THRESHOLD_MS = 1000

    @allure.step("Get users list (page: {page})")
    def get_users(self, page: int = 1) -> dict[str, Any]:
        """
        Get paginated list of users.

        Args:
            page: Page number

        Returns:
            Response with users list and pagination info
        """
        return self.get(
            "/api/users",
            params={"page": page},
            description="Get paginated users list",
        )

    @allure.step("Get single user: {user_id}")
    def get_user(self, user_id: int) -> dict[str, Any]:
        """
        Get a single user by ID.

        Args:
            user_id: User ID

        Returns:
            User data
        """
        return self.get(
            f"/api/users/{user_id}",
            description=f"Get user details for ID {user_id}",
        )

    @allure.step("Create user: {name}")
    def create_user(self, name: str, job: str) -> dict[str, Any]:
        """
        Create a new user.

        Args:
            name: User name
            job: User job title

        Returns:
            Created user with id and createdAt
        """
        return self.post(
            "/api/users",
            json={"name": name, "job": job},
            description=f"Create new user '{name}' with job '{job}'",
        )

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
        return self.put(
            f"/api/users/{user_id}",
            json={"name": name, "job": job},
            description=f"Update user {user_id} (full update)",
        )

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
        return self.patch(
            f"/api/users/{user_id}",
            json=fields,
            description=f"Partially update user {user_id}",
        )

    @allure.step("Delete user: {user_id}")
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID

        Returns:
            True if successful (204 status)
        """
        result = self.delete(
            f"/api/users/{user_id}",
            description=f"Delete user {user_id}",
        )
        return True

    @allure.step("Register user: {email}")
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
        return self.post(
            "/api/register",
            json={"email": email, "password": password},
            description=f"Register new user with email {email}",
        )

    @allure.step("Login user: {email}")
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
        return self.post(
            "/api/login",
            json={"email": email, "password": password},
            description=f"Login user {email}",
        )

    @allure.step("Get resources list")
    def get_resources(self) -> dict[str, Any]:
        """
        Get list of resources.

        Returns:
            Response with resources list
        """
        return self.get(
            "/api/unknown",
            description="Get all resources",
        )

    @allure.step("Get single resource: {resource_id}")
    def get_resource(self, resource_id: int) -> dict[str, Any]:
        """
        Get a single resource by ID.

        Args:
            resource_id: Resource ID

        Returns:
            Resource data
        """
        return self.get(
            f"/api/unknown/{resource_id}",
            description=f"Get resource {resource_id}",
        )
