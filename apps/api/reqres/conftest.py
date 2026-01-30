"""ReqRes API app fixtures."""

import pytest

from apps.api.reqres.clients import ReqResClient


@pytest.fixture(scope="session")
def reqres_config(app_configs):
    """Get ReqRes configuration."""
    config = app_configs.get("reqres")
    if not config:
        pytest.skip("ReqRes not configured")
    return config


@pytest.fixture
def reqres_client(reqres_config):
    """
    Create a ReqRes API client instance.

    This fixture provides a fresh client for each test.
    """
    # Get API key from extra_config (handling potential double-nesting)
    api_key = None
    if hasattr(reqres_config, 'extra_config') and reqres_config.extra_config:
        # Check if extra_config is double-nested
        if 'extra_config' in reqres_config.extra_config:
            api_key = reqres_config.extra_config['extra_config'].get('api_key')
        else:
            api_key = reqres_config.extra_config.get('api_key')
    
    return ReqResClient(base_url=reqres_config.base_url, api_key=api_key)
