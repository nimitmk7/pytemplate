"""Factory module for creating a ConcreteAIConversationClient instance.

This module provides a function to instantiate a ConcreteAIConversationClient
using a GeminiProvider and a ConcreteThreadRepository. It retrieves the required
API key from environment variables and prepares the AI models for the provider.
"""

import os

from ai_conversation_client_impl.client import (
    ConcreteAIConversationClient,
    ConcreteThreadRepository,
    GeminiProvider,
)


def create_client() -> ConcreteAIConversationClient:
    """Create and return a configured ConcreteAIConversationClient.

    This function initializes the underlying GeminiProvider and ConcreteThreadRepository,
    and binds them together to form a ConcreteAIConversationClient instance.

    Returns:
        ConcreteAIConversationClient: The client ready for use.

    Raises:
        ValueError: If the GEMINI_API_KEY environment variable is not set.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in the environment")

    available_models = ["models/gemini-1.5-pro-latest"]  # or other valid models

    provider = GeminiProvider(available_models=available_models, api_key=api_key)
    repository = ConcreteThreadRepository()
    client = ConcreteAIConversationClient(provider, repository)
    return client
