"""Restful Booker API app fixtures."""

import pytest

from apps.api.restful_booker.clients import RestfulBookerClient


@pytest.fixture(scope="session")
def restful_booker_config(app_configs):
    """Get Restful Booker configuration."""
    config = app_configs.get("restful_booker")
    if not config:
        pytest.skip("Restful Booker not configured")
    return config


@pytest.fixture
def restful_booker_client(restful_booker_config):
    """
    Create a Restful Booker API client instance.

    This fixture provides a fresh client for each test.
    """
    return RestfulBookerClient(base_url=restful_booker_config.base_url)


@pytest.fixture
def authenticated_client(restful_booker_client):
    """
    Create an authenticated Restful Booker client.

    This fixture creates a token automatically.
    """
    restful_booker_client.create_token()
    return restful_booker_client
