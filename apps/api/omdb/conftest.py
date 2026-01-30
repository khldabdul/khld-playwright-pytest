"""OMDb API app fixtures."""

import os
import pytest

from apps.api.omdb.clients import OmdbClient


@pytest.fixture(scope="session")
def omdb_config(app_configs):
    """Get OMDb configuration."""
    config = app_configs.get("omdb")
    if not config:
        pytest.skip("OMDb not configured")
    return config


@pytest.fixture
def omdb_api_key(omdb_config):
    """Get OMDb API key from environment."""
    env_var = omdb_config.auth_config.get("value_env", "OMDB_API_KEY")
    api_key = os.environ.get(env_var)
    
    if not api_key:
        pytest.skip(f"OMDb API key not found in environment variable: {env_var}")
        
    return api_key


@pytest.fixture
def omdb_client(omdb_config, omdb_api_key):
    """
    Create an OMDb API client instance.

    This fixture provides a fresh client for each test.
    """
    return OmdbClient(base_url=omdb_config.base_url, api_key=omdb_api_key)
