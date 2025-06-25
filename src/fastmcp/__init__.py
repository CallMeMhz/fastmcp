"""FastMCP - An ergonomic MCP interface."""

from importlib.metadata import version

from fastmcp.server.server import FastMCP
from fastmcp.server.context import Context
from fastmcp.server.router import APIRouter
import fastmcp.server

from fastmcp.client import Client
from fastmcp.utilities.types import Image
from . import client, settings

__version__ = version("fastmcp")
__all__ = [
    "FastMCP",
    "APIRouter",
    "Context",
    "client",
    "Client",
    "settings",
    "Image",
]
