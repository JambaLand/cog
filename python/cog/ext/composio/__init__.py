"""
Composio plugin for Cog - Integrates with 1000+ apps including TLDV.

This plugin provides seamless integration between Cog and Composio,
enabling access to a wide range of third-party services.
"""

from .client import ComposioClient
from .tldv import TLDVIntegration

__all__ = [
    "ComposioClient",
    "TLDVIntegration",
]

__version__ = "0.1.0"
