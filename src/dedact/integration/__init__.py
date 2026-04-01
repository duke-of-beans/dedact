"""
Integration Module
MCP integration and external database connectors
"""

from .mcp_integration import MCPIntegrator
from .external_db_connectors import ExternalDBConnector
from .entity_resolution import EntityResolver

__all__ = [
    'MCPIntegrator',
    'ExternalDBConnector',
    'EntityResolver'
]
