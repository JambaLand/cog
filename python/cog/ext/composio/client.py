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
            toolkits_response = self.client.toolkits.list()
            return [toolkit.name for toolkit in toolkits_response.items]
        except Exception as e:
            raise RuntimeError(f"Failed to fetch available apps: {e}")

    def get_app_slug(self, app_name: str) -> Optional[str]:
        """
        Get the slug for an app by name.

        Args:
            app_name: Name of the app (e.g., "TLDV" or "tldv").

        Returns:
            The slug for the app, or None if not found.
        """
        try:
            toolkits_response = self.client.toolkits.list()
            app_name_lower = app_name.lower()
            for toolkit in toolkits_response.items:
                if (
                    toolkit.name.lower() == app_name_lower
                    or toolkit.slug.lower() == app_name_lower
                ):
                    return toolkit.slug
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to fetch app slug for {app_name}: {e}")

    def get_app_tools(self, app_slug: str) -> list[str]:
        """
        Get available tools/actions for a specific app.

        Args:
            app_slug: Slug of the app (e.g., "tldv").

        Returns:
            List of available tool names.
        """
        try:
            tools = self.client.tools.get_raw_composio_tools(
                toolkits=[app_slug]
            )
            return [tool.name for tool in tools]
        except Exception as e:
            raise RuntimeError(f"Failed to fetch tools for {app_slug}: {e}")

    def authenticate_app(
        self, app_slug: str, credentials: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Authenticate with a specific app.

        Args:
            app_slug: Slug of the app (e.g., "tldv").
            credentials: Credentials for the app.

        Returns:
            Authentication response.
        """
        try:
            response = self.client.toolkits.authorize(
                app_slug, request_data=credentials
            )
            return response.model_dump() if hasattr(response, "model_dump") else response
        except Exception as e:
            raise RuntimeError(f"Failed to authenticate with {app_slug}: {e}")

    def execute_action(
        self, app_slug: str, action_name: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute an action in a specific app.

        Args:
            app_slug: Slug of the app (e.g., "tldv").
            action_name: Name of the action to execute.
            params: Parameters for the action.

        Returns:
            Action execution response.
        """
        try:
            # Get the tool by slug and action name
            action_id = f"{app_slug}.{action_name}"
            result = self.client.tools.execute(
                action=action_id, params=params
            )
            return result
        except Exception as e:
            raise RuntimeError(
                f"Failed to execute action {action_name} on {app_slug}: {e}"
            )
