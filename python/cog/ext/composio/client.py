"""Composio client for Cog integration."""

import os
from typing import Any, Dict, Optional

try:
    import composio
except ImportError:
    composio = None


class ComposioClient:
    """Client for Composio API integration."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.composio.dev",
    ) -> None:
        """
        Initialize Composio client.

        Args:
            api_key: Composio API key. Defaults to COMPOSIO_API_KEY env var.
            base_url: Base URL for Composio API.

        Raises:
            ImportError: If composio package is not installed.
            ValueError: If API key is not provided or found.
        """
        if composio is None:
            raise ImportError(
                "composio package is required. Install it with: pip install composio"
            )

        self.api_key = api_key or os.getenv("COMPOSIO_API_KEY")
        if not self.api_key:
            raise ValueError(
                "COMPOSIO_API_KEY not provided. Set it via argument or environment variable."
            )

        self.base_url = base_url
        self._client: Optional[Any] = None

    @property
    def client(self) -> Any:
        """Get or initialize the Composio client."""
        if self._client is None:
            self._client = composio.Composio(api_key=self.api_key)
        return self._client

    def get_available_apps(self) -> list[str]:
        """Get list of available apps from Composio."""
        try:
            apps = self.client.get_apps()
            return [app.name for app in apps]
        except Exception as e:
            raise RuntimeError(f"Failed to fetch available apps: {e}")

    def authenticate_app(
        self, app_name: str, credentials: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Authenticate with a specific app.

        Args:
            app_name: Name of the app to authenticate with.
            credentials: Credentials for the app.

        Returns:
            Authentication response.
        """
        try:
            response = self.client.authenticate_app(app_name, credentials)
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to authenticate with {app_name}: {e}")

    def execute_action(
        self, app_name: str, action: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute an action in a specific app.

        Args:
            app_name: Name of the app.
            action: Name of the action to execute.
            params: Parameters for the action.

        Returns:
            Action execution response.
        """
        try:
            response = self.client.execute_action(app_name, action, params)
            return response
        except Exception as e:
            raise RuntimeError(
                f"Failed to execute action {action} on {app_name}: {e}"
            )

    def get_app_actions(self, app_name: str) -> list[str]:
        """
        Get available actions for a specific app.

        Args:
            app_name: Name of the app.

        Returns:
            List of available actions.
        """
        try:
            app = self.client.get_app(app_name)
            actions = app.get_actions()
            return [action.name for action in actions]
        except Exception as e:
            raise RuntimeError(f"Failed to fetch actions for {app_name}: {e}")
