"""Data loader utilities for loading test data from various sources."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


class DataLoader:
    """Utility class for loading test data from files."""

    def __init__(self, base_path: Path | str | None = None):
        """
        Initialize DataLoader.

        Args:
            base_path: Base path for relative file lookups. Defaults to config/
        """
        if base_path is None:
            base_path = Path(__file__).parent.parent.parent / "config"
        self.base_path = Path(base_path)

    def load_yaml(self, file_path: str | Path) -> dict[str, Any]:
        """
        Load data from YAML file.

        Args:
            file_path: Path to YAML file (absolute or relative to base_path)

        Returns:
            Dictionary containing YAML data
        """
        path = self._resolve_path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"YAML file not found: {path}")

        with open(path) as f:
            return yaml.safe_load(f) or {}

    def load_json(self, file_path: str | Path) -> dict[str, Any]:
        """
        Load data from JSON file.

        Args:
            file_path: Path to JSON file (absolute or relative to base_path)

        Returns:
            Dictionary containing JSON data
        """
        path = self._resolve_path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {path}")

        with open(path) as f:
            return json.load(f)

    def load_test_data(self, app_name: str | None = None) -> dict[str, Any]:
        """
        Load test data, optionally filtered by app.

        Args:
            app_name: App name to filter data for

        Returns:
            Test data dictionary
        """
        data = self.load_yaml("test_data.yml")

        if app_name:
            app_data = data.get(app_name, {})
            common_data = data.get("common", {})
            return {**common_data, **app_data}

        return data

    def load_app_config(self, app_name: str, environment: str = "dev") -> dict[str, Any]:
        """
        Load app configuration.

        Args:
            app_name: Name of the app
            environment: Environment to load config for

        Returns:
            App configuration dictionary
        """
        config_path = self.base_path / "apps" / f"{app_name}_config.yml"
        config = self.load_yaml(config_path)

        # Resolve base URL for environment
        base_urls = config.get("base_urls", {})
        config["base_url"] = base_urls.get(environment, base_urls.get("dev", ""))

        return config

    def _resolve_path(self, file_path: str | Path) -> Path:
        """
        Resolve file path.

        Args:
            file_path: Path to resolve

        Returns:
            Resolved absolute path
        """
        path = Path(file_path)
        if not path.is_absolute():
            path = self.base_path / path
        return path


# Convenience functions
def load_yaml(file_path: str | Path) -> dict[str, Any]:
    """Load YAML file from default config path."""
    return DataLoader().load_yaml(file_path)


def load_json(file_path: str | Path) -> dict[str, Any]:
    """Load JSON file from default config path."""
    return DataLoader().load_json(file_path)


def load_test_data(app_name: str | None = None) -> dict[str, Any]:
    """Load test data from default location."""
    return DataLoader().load_test_data(app_name)
