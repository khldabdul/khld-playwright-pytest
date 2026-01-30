"""
Base API Client with Allure integration.

This module provides a base class for API clients that automatically
logs HTTP requests, responses, and performance metrics to Allure.
"""

from __future__ import annotations

from typing import Any

import requests

from infrastructure.utils.allure_helpers import (
    attach_http_request,
    attach_http_response,
    attach_performance_metric,
)


class BaseAPIClient:
    """
    Base API client with automatic Allure reporting.

    This class provides common functionality for all API clients:
    - Automatic request/response logging to Allure
    - Performance tracking for all API calls
    - Consistent error handling
    """

    # Performance thresholds (in milliseconds) - override in subclasses
    DEFAULT_THRESHOLD_MS = 1000
    SLOW_THRESHOLD_MS = 2000

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        default_headers: dict[str, str] | None = None,
    ):
        """
        Initialize the base API client.

        Args:
            base_url: Base URL for the API
            api_key: Optional API key for authentication
            default_headers: Default headers to include with all requests
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Playwright-Pytest-Framework/1.0",
        }

        if default_headers:
            headers.update(default_headers)

        # Add API key if provided (subclasses can override the header name)
        if api_key:
            headers["x-api-key"] = api_key

        self.session.headers.update(headers)

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict | None = None,
        json: dict | None = None,
        data: Any = None,
        headers: dict | None = None,
        description: str | None = None,
        threshold_ms: int | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Make an HTTP request with Allure reporting.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (will be appended to base_url)
            params: Query parameters
            json: JSON request body
            data: Raw request data
            headers: Additional headers for this request
            description: Optional description for Allure
            threshold_ms: Performance threshold for this request
            **kwargs: Additional arguments passed to requests

        Returns:
            Parsed JSON response

        Raises:
            requests.HTTPError: If the request fails
        """
        import time

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)

        # Attach request to Allure
        attach_http_request(
            method=method,
            url=url,
            headers=request_headers,
            body=json or data,
            description=description,
        )

        # Make request and measure time
        start_time = time.time()
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            data=data,
            headers=request_headers,
            **kwargs,
        )
        elapsed_ms = int((time.time() - start_time) * 1000)

        # Parse response body
        response_body = None
        try:
            response_body = response.json() if response.text else None
        except ValueError:
            response_body = response.text

        # Attach response to Allure
        attach_http_response(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=response_body,
            response_time_ms=elapsed_ms,
        )

        # Check performance
        threshold = threshold_ms or self.DEFAULT_THRESHOLD_MS
        attach_performance_metric(
            operation=f"{method.upper()} {endpoint}",
            duration_ms=elapsed_ms,
            threshold_ms=threshold,
        )

        # Raise error if needed
        response.raise_for_status()

        return response_body if response_body is not None else {}

    def get(self, endpoint: str, **kwargs) -> dict[str, Any]:
        """Make a GET request."""
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, json: dict | None = None, **kwargs) -> dict[str, Any]:
        """Make a POST request."""
        return self._request("POST", endpoint, json=json, **kwargs)

    def put(self, endpoint: str, json: dict | None = None, **kwargs) -> dict[str, Any]:
        """Make a PUT request."""
        return self._request("PUT", endpoint, json=json, **kwargs)

    def patch(self, endpoint: str, json: dict | None = None, **kwargs) -> dict[str, Any]:
        """Make a PATCH request."""
        return self._request("PATCH", endpoint, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> dict[str, Any]:
        """Make a DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)
