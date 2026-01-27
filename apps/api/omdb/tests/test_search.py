"""OMDb API - Search and Get Tests.

This test suite covers movie search operations including:
- Search movies by title
- Get movie details by IMDb ID
- Get movie details by title
- Error handling for non-existent movies

API Documentation: http://www.omdbapi.com/
"""

from __future__ import annotations

import pytest
import allure

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("OMDb API")
@allure.feature("Movie Search & Retrieval")
@allure.label("layer", "api")
@allure.label("type", "functional")
@pytest.mark.app("omdb")
@pytest.mark.api
class TestOmdbSearch:
    """Test suite for OMDb search operations."""

    @allure.story("Search Movies")
    @allure.title("Search for existing movie by title")
    @allure.description_html(markdown_to_html("""
    Verify that movies can be searched by title.

    **Test Coverage:**
    - Search by movie title
    - Response contains total results count
    - Search results include required fields (Title, Type, imdbID)

    **Business Value:**
    Core functionality for movie discovery and search.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("http://www.omdbapi.com/#parameters", name="API Docs")
    @pytest.mark.testcase("TC-OMD-001")
    @pytest.mark.requirement("US-SEARCH-001")
    @pytest.mark.smoke
    def test_search_movie(self, omdb_client):
        """Test searching for a known movie (Inception)."""
        with allure.step("Search for 'Inception'"):
            response = omdb_client.search(title="Inception", type="movie")

        with allure.step("Verify search results"):
            assert response["Response"] == "True"
            assert int(response["totalResults"]) > 0
            assert len(response["Search"]) > 0

        with allure.step("Verify first result structure"):
            first_match = response["Search"][0]
            assert "Inception" in first_match["Title"]
            assert first_match["Type"] == "movie"
            assert "imdbID" in first_match

    @allure.story("View Movie Details")
    @allure.title("Get movie by IMDb ID")
    @allure.description_html(markdown_to_html("""
    Verify that movie details can be retrieved by IMDb ID.

    **Test Coverage:**
    - Retrieve movie by IMDb ID
    - All movie fields are present
    - Data accuracy is maintained

    **Business Value:**
    Essential for viewing complete movie information.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.testcase("TC-OMD-020")
    @pytest.mark.requirement("US-SEARCH-002")
    def test_get_movie_by_id(self, omdb_client):
        """Test retrieving a movie by valid IMDb ID."""
        imdb_id = "tt0133093"  # The Matrix

        with allure.step(f"Get movie by IMDb ID: {imdb_id}"):
            response = omdb_client.get_by_id(imdb_id=imdb_id)

        with allure.step("Verify movie details"):
            assert response["Response"] == "True"
            assert response["Title"] == "The Matrix"
            assert response["Year"] == "1999"
            assert response["Director"] == "Lana Wachowski, Lilly Wachowski"

    @allure.story("View Movie Details")
    @allure.title("Get movie by exact title")
    @allure.description_html(markdown_to_html("""
    Verify that movie details can be retrieved by exact title.

    **Test Coverage:**
    - Retrieve movie by title and year
    - Response contains complete movie data
    - Data accuracy is maintained

    **Business Value:**
    Alternative method for accessing movie information.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-OMD-002")
    @pytest.mark.requirement("US-SEARCH-003")
    def test_get_movie_by_title(self, omdb_client):
        """Test retrieving a movie by exact title."""
        with allure.step("Get 'The Dark Knight' (2008)"):
            response = omdb_client.get_by_title(title="The Dark Knight", year="2008")

        with allure.step("Verify movie details"):
            assert response["Response"] == "True"
            assert response["Title"] == "The Dark Knight"
            assert response["Year"] == "2008"
            assert "Christopher Nolan" in response["Director"]

    @allure.story("Error Handling")
    @allure.title("Search for non-existent movie returns error")
    @allure.description_html(markdown_to_html("""
    Verify that searching for non-existent movie returns proper error.

    **Test Coverage:**
    - Non-existent movie handling
    - Error response structure
    - Error message clarity

    **Business Value:**
    Ensures graceful error handling for invalid searches.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-OMD-003")
    @pytest.mark.requirement("US-SEARCH-004")
    def test_search_nonexistent(self, omdb_client):
        """Test searching for a movie that doesn't exist."""
        with allure.step("Search for non-existent movie"):
            response = omdb_client.search(title="Askjdhasjkdhasjkdh123123")

        with allure.step("Verify error response"):
            assert response["Response"] == "False"
            assert response["Error"] == "Movie not found!"

    @allure.story("Error Handling")
    @allure.title("Get movie with invalid ID returns error")
    @allure.description_html(markdown_to_html("""
    Verify that retrieving with invalid IMDb ID returns proper error.

    **Test Coverage:**
    - Invalid IMDb ID handling
    - Error response structure

    **Business Value:**
    Ensures proper error handling for invalid requests.
    """))
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.testcase("TC-OMD-021")
    @pytest.mark.requirement("US-SEARCH-005")
    def test_invalid_id(self, omdb_client):
        """Test retrieving with invalid IMDb ID."""
        with allure.step("Attempt to get movie with invalid ID"):
            response = omdb_client.get_by_id(imdb_id="tt0000000000")

        with allure.step("Verify error response"):
            assert response["Response"] == "False"
            assert "Error" in response
