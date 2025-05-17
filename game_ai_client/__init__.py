"""
Game AI Client package.
Provides functionality for connecting to a game server and implementing AI logic.
"""
from .connection import Connection
from .ai_client import AIClient

__all__ = ['Connection', 'AIClient']
