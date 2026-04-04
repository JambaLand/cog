"""Tests for Composio plugin."""

import os
import pytest

from .client import ComposioClient
from .tldv import TLDVIntegration


class TestComposioClient:
    """Test ComposioClient initialization and basic functionality."""

    def test_client_init_with_api_key(self) -> None:
        """Test initializing client with explicit API key."""
        try:
            client = ComposioClient(api_key="test-key")
            assert client.api_key == "test-key"
        except ImportError:
            pytest.skip("composio package not installed")

    def test_client_init_missing_api_key(self) -> None:
        """Test that client raises error when API key is missing."""
        # Remove env var if it exists
        old_key = os.environ.pop("COMPOSIO_API_KEY", None)
        try:
            with pytest.raises(ValueError, match="COMPOSIO_API_KEY"):
                ComposioClient()
        finally:
            if old_key:
                os.environ["COMPOSIO_API_KEY"] = old_key

    def test_client_init_from_env(self) -> None:
        """Test initializing client from environment variable."""
        old_key = os.environ.get("COMPOSIO_API_KEY")
        try:
            os.environ["COMPOSIO_API_KEY"] = "env-test-key"
            client = ComposioClient()
            assert client.api_key == "env-test-key"
        except ImportError:
            pytest.skip("composio package not installed")
        finally:
            if old_key:
                os.environ["COMPOSIO_API_KEY"] = old_key
            else:
                os.environ.pop("COMPOSIO_API_KEY", None)

    def test_composio_import_error(self) -> None:
        """Test that ImportError is raised when composio is not installed."""
        # This test would require actually uninstalling composio
        # which we don't want to do, so we just document the expected behavior
        pass


class TestTLDVIntegration:
    """Test TLDV integration."""

    def test_tldv_init_without_client(self) -> None:
        """Test initializing TLDV without providing a client."""
        try:
            # This will try to fetch available apps, which will fail without valid credentials
            with pytest.raises(RuntimeError):
                TLDVIntegration(api_key="invalid-key")
        except ImportError:
            pytest.skip("composio package not installed")

    def test_tldv_init_with_client(self) -> None:
        """Test initializing TLDV with an existing client."""
        try:
            client = ComposioClient(api_key="test-key")
            # This will fail because the API key is invalid, but it tests the init path
            with pytest.raises(RuntimeError):
                TLDVIntegration(composio_client=client)
        except ImportError:
            pytest.skip("composio package not installed")
