"""Session-scoped fixtures for test automation framework."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_env_config(env: str = "dev") -> dict[str, Any]:
    """
    Load environment configuration from YAML file.

    Args:
        env: Environment name (dev, staging, production)

    Returns:
        Dictionary containing environment configuration
    """
    config_path = Path(__file__).parent.parent.parent / "config" / "environments.yml"

    if not config_path.exists():
        raise FileNotFoundError(f"Environment config not found: {config_path}")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    env_config = config.get("environments", {}).get(env, {})
    env_config["name"] = env
    env_config["browsers"] = config.get("browsers", {})
    env_config["viewports"] = config.get("viewports", {})

    return env_config


def load_test_data() -> dict[str, Any]:
    """
    Load test data from YAML file.

    Returns:
        Dictionary containing test data
    """
    config_path = Path(__file__).parent.parent.parent / "config" / "test_data.yml"

    if not config_path.exists():
        return {}

    with open(config_path) as f:
        return yaml.safe_load(f) or {}


@pytest.fixture(scope="session")
def environment(pytestconfig) -> str:
    """Get the current test environment from CLI or default to 'dev'."""
    return pytestconfig.getoption("--env", default="dev")


@pytest.fixture(scope="session")
def env_config(environment: str) -> dict[str, Any]:
    """
    Load environment configuration.

    This fixture loads the environment-specific settings from environments.yml.
    """
    return load_env_config(environment)


@pytest.fixture(scope="session")
def test_data() -> dict[str, Any]:
    """
    Load test data from configuration.

    This fixture loads shared test data from test_data.yml.
    """
    return load_test_data()


@pytest.fixture(scope="session")
def test_results_dir() -> Path:
    """
    Provide path to test results directory.

    Creates the directory if it doesn't exist.
    """
    results_dir = Path("test-results")
    results_dir.mkdir(exist_ok=True)
    return results_dir


@pytest.fixture(scope="session")
def screenshots_dir(test_results_dir: Path) -> Path:
    """
    Provide path to screenshots directory.

    Creates the directory if it doesn't exist.
    """
    screenshots = test_results_dir / "screenshots"
    screenshots.mkdir(exist_ok=True)
    return screenshots


@pytest.fixture(scope="session")
def traces_dir(test_results_dir: Path) -> Path:
    """
    Provide path to traces directory.

    Creates the directory if it doesn't exist.
    """
    traces = test_results_dir / "traces"
    traces.mkdir(exist_ok=True)
    return traces


@pytest.fixture(scope="session")
def videos_dir(test_results_dir: Path) -> Path:
    """
    Provide path to videos directory.

    Creates the directory if it doesn't exist.
    """
    videos = test_results_dir / "videos"
    videos.mkdir(exist_ok=True)
    return videos


def get_env_variable(name: str, default: str | None = None) -> str | None:
    """
    Get environment variable with optional default.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Environment variable value or default
    """
    return os.environ.get(name, default)


@pytest.fixture(scope="session")
def run_id() -> str:
    """
    Generate a unique run ID for this test session.

    Used for tracking test history in Allure reports.
    The run ID is based on timestamp and includes environment info.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"run_{timestamp}"
