"""OMDb API Client.

This module provides a client for interacting with the OMDb API.
"""

from __future__ import annotations

from typing import Any

import allure
import requests


class OmdbClient:
    """Client for OMDb API operations."""

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the OMDb API client.

        Args:
            base_url: Base URL for the API
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _get(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Internal GET method that injects API key.

        Args:
            params: Query parameters

        Returns:
            JSON response
        """
        # Inject API key
        params["apikey"] = self.api_key
        
        response = self.session.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    @allure.step("Search movies by title: {title}")
    def search(self, title: str, type: str | None = None, year: str | None = None, page: int = 1) -> dict[str, Any]:
        """
        Search for movies/series.

        Args:
            title: Title to search for (s parameter)
            type: Type of result to return (movie, series, episode)
            year: Year of release (y parameter)
            page: Page number to return (1-100)

        Returns:
            Search results
        """
        params = {"s": title, "page": page}
        if type:
            params["type"] = type
        if year:
            params["y"] = year
            
        return self._get(params)

    @allure.step("Get by ID: {imdb_id}")
    def get_by_id(self, imdb_id: str, plot: str = "short") -> dict[str, Any]:
        """
        Get movie/series by IMDb ID.

        Args:
            imdb_id: A valid IMDb ID (e.g. tt1285016)
            plot: Plot length (short, full)

        Returns:
            Movie details
        """
        return self._get({"i": imdb_id, "plot": plot})

    @allure.step("Get by Title: {title}")
    def get_by_title(self, title: str, type: str | None = None, year: str | None = None, plot: str = "short") -> dict[str, Any]:
        """
        Get movie/series by exact title.

        Args:
            title: Title to look up (t parameter)
            type: Type of result (movie, series, episode)
            year: Year of release
            plot: Plot length (short, full)

        Returns:
            Movie details
        """
        params = {"t": title, "plot": plot}
        if type:
            params["type"] = type
        if year:
            params["y"] = year
            
        return self._get(params)
