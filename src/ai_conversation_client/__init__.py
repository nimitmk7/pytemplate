"""AI conversation client package.

This package provides interfaces for interacting with AI conversation services.
"""
# Keeping __init__.py minimal to avoid slowing down imports

from .interfaces import (
    AIConversationClient,
    ModelProvider,
    Thread,
    ThreadRepository,
)

__all__ = [
    "Thread",
    "ModelProvider",
    "ThreadRepository",
    "AIConversationClient",
]
