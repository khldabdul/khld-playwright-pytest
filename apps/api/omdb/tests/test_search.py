"""OMDb API - Search and Get Tests."""

import pytest
import allure

@allure.feature("OMDb API")
@allure.story("Search and Retrieval")
@pytest.mark.app("omdb")
@pytest.mark.api
class TestOmdbSearch:
    """Test suite for OMDb search operations."""

    @allure.title("Search for existing movie")
    def test_search_movie(self, omdb_client):
        """Test searching for a known movie (Inception)."""
        response = omdb_client.search(title="Inception", type="movie")
        
        assert response["Response"] == "True"
        assert int(response["totalResults"]) > 0
        assert len(response["Search"]) > 0
        
        # Verify first result
        first_match = response["Search"][0]
        assert "Inception" in first_match["Title"]
        assert first_match["Type"] == "movie"
        assert "imdbID" in first_match

    @allure.title("Get movie by ID")
    def test_get_movie_by_id(self, omdb_client):
        """Test retrieving a movie by valid IMDb ID."""
        # The Matrix
        imdb_id = "tt0133093"
        response = omdb_client.get_by_id(imdb_id=imdb_id)
        
        assert response["Response"] == "True"
        assert response["Title"] == "The Matrix"
        assert response["Year"] == "1999"
        assert response["Director"] == "Lana Wachowski, Lilly Wachowski"

    @allure.title("Get movie by Title")
    def test_get_movie_by_title(self, omdb_client):
        """Test retrieving a movie by exact title."""
        response = omdb_client.get_by_title(title="The Dark Knight", year="2008")
        
        assert response["Response"] == "True"
        assert response["Title"] == "The Dark Knight"
        assert response["Year"] == "2008"
        assert "Christopher Nolan" in response["Director"]

    @allure.title("Search non-existent movie")
    def test_search_nonexistent(self, omdb_client):
        """Test searching for a movie that doesn't exist."""
        # Random string unlikely to be a movie
        response = omdb_client.search(title="Askjdhasjkdhasjkdh123123")
        
        assert response["Response"] == "False"
        assert response["Error"] == "Movie not found!"

    @allure.title("Get with invalid ID")
    def test_invalid_id(self, omdb_client):
        """Test retrieving with invalid IMDb ID."""
        response = omdb_client.get_by_id(imdb_id="tt0000000000")
        
        assert response["Response"] == "False"
        assert "Error" in response
