"""App Factory pattern for multi-app testing architecture."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest
import yaml
from playwright.sync_api import Page


@dataclass
class AppConfig:
    """Configuration for a single web application."""

    name: str
    display_name: str
    base_url: str
    auth_required: bool = True
    default_timeout: int = 30000
    screenshot_on_failure: bool = True
    storage_state_path: str | None = None
    viewport: dict[str, int] = field(default_factory=lambda: {"width": 1920, "height": 1080})
    auth_config: dict[str, Any] = field(default_factory=dict)
    test_users: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, config_path: Path, environment: str) -> "AppConfig":
        """
        Load AppConfig from YAML file.

        Args:
            config_path: Path to the app configuration YAML file
            environment: Current environment (dev, staging, production)

        Returns:
            AppConfig instance
        """
        if not config_path.exists():
            raise FileNotFoundError(f"App config not found: {config_path}")

        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Get base URL for the current environment
        base_urls = config.get("base_urls", {})
        base_url = base_urls.get(environment, base_urls.get("dev", "http://localhost:3000"))

        # Get settings
        settings = config.get("settings", {})

        return cls(
            name=config.get("name", "unknown"),
            display_name=config.get("display_name", config.get("name", "Unknown App")),
            base_url=base_url,
            auth_required=config.get("auth", {}).get("type") is not None,
            default_timeout=settings.get("default_timeout", 30000),
            screenshot_on_failure=settings.get("screenshot_on_failure", True),
            storage_state_path=config.get("auth", {}).get("storage_state_path"),
            viewport=settings.get("viewport", {"width": 1920, "height": 1080}),
            auth_config=config.get("auth", {}),
            test_users=config.get("test_users", {}),
        )


class AppInstance:
    """
    Runtime instance of an app for a single test.

    Provides access to app-specific pages, configuration, and utilities.
    """

    def __init__(self, config: AppConfig, page: Page):
        """
        Initialize AppInstance.

        Args:
            config: App configuration
            page: Playwright page instance
        """
        self.config = config
        self.page = page
        self._pages_module = None

    @property
    def name(self) -> str:
        """Get app name."""
        return self.config.name

    @property
    def base_url(self) -> str:
        """Get app base URL."""
        return self.config.base_url

    @property
    def timeout(self) -> int:
        """Get default timeout for this app."""
        return self.config.default_timeout

    def navigate(self, path: str = "") -> None:
        """
        Navigate to a path in this app.

        Args:
            path: Path to navigate to (appended to base_url)
        """
        url = self.config.base_url.rstrip("/") + "/" + path.lstrip("/")
        self.page.goto(url, timeout=self.config.default_timeout)

    def wait_for_load_state(self, state: str = "load") -> None:
        """
        Wait for specified load state.

        Args:
            state: Load state to wait for (load, domcontentloaded, networkidle)
        """
        self.page.wait_for_load_state(state, timeout=self.config.default_timeout)

    def get_test_user(self, user_type: str) -> dict[str, str]:
        """
        Get test user credentials.

        Args:
            user_type: Type of user (e.g., "admin", "customer")

        Returns:
            Dictionary with username/email and password
        """
        user_config = self.config.test_users.get(user_type, {})
        password_env = user_config.get("password_env", "")

        return {
            "username": user_config.get("username", user_config.get("email", "")),
            "email": user_config.get("email", user_config.get("username", "")),
            "password": os.environ.get(password_env, ""),
            "role": user_config.get("role", ""),
        }

    def take_screenshot(self, name: str, full_page: bool = True) -> Path:
        """
        Take a screenshot.

        Args:
            name: Screenshot name
            full_page: Whether to capture full page

        Returns:
            Path to the screenshot file
        """
        screenshot_dir = Path("test-results/screenshots") / self.config.name
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        screenshot_path = screenshot_dir / f"{name}.png"
        self.page.screenshot(path=str(screenshot_path), full_page=full_page)

        return screenshot_path


def load_app_configs(environment: str) -> dict[str, AppConfig]:
    """
    Load all app configurations.

    Args:
        environment: Current environment (dev, staging, production)

    Returns:
        Dictionary mapping app names to AppConfig instances
    """
    apps_config_dir = Path(__file__).parent.parent.parent / "config" / "apps"
    configs = {}

    if apps_config_dir.exists():
        for config_file in apps_config_dir.glob("*_config.yml"):
            try:
                app_config = AppConfig.from_yaml(config_file, environment)
                configs[app_config.name] = app_config
            except Exception as e:
                print(f"Warning: Failed to load app config {config_file}: {e}")

    return configs


@pytest.fixture(scope="session")
def app_configs(environment: str) -> dict[str, AppConfig]:
    """
    Load all app configurations.

    This fixture loads app configurations from YAML files in config/apps/.
    """
    return load_app_configs(environment)


@pytest.fixture
def current_app(request, app_configs: dict[str, AppConfig], page: Page) -> AppInstance:
    """
    Get the app instance for the current test.

    Usage:
        @pytest.mark.app("admin_portal")
        def test_admin_login(current_app):
            current_app.navigate("/login")
            ...

    Raises:
        pytest.fail: If test doesn't have @pytest.mark.app marker or app not found
    """
    marker = request.node.get_closest_marker("app")

    if not marker:
        pytest.fail(
            "Test must specify @pytest.mark.app('app_name'). "
            f"Available apps: {list(app_configs.keys())}"
        )

    app_name = marker.args[0]

    if app_name not in app_configs:
        pytest.fail(
            f"Unknown app: {app_name}. Available apps: {list(app_configs.keys())}"
        )

    config = app_configs[app_name]
    return AppInstance(config, page)
