"""Petstore API app fixtures."""

import pytest

from apps.api.petstore.clients import PetstoreClient


@pytest.fixture(scope="session")
def petstore_config(app_configs):
    """Get Petstore configuration."""
    config = app_configs.get("petstore")
    if not config:
        pytest.skip("Petstore not configured")
    return config


@pytest.fixture
def petstore_client(petstore_config):
    """
    Create a Petstore API client instance.

    This fixture provides a fresh client for each test.
    """
    return PetstoreClient(
        base_url=petstore_config.base_url,
        api_key=petstore_config.auth_config.get("api_key")
    )
