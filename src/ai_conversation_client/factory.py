"""Factory for creating a ConcreteAIConversationClient."""

import os

from ai_conversation_client_impl.client import (
    ConcreteAIConversationClient,
    ConcreteThreadRepository,
    GeminiProvider,
)


def create_client() -> ConcreteAIConversationClient:
    """Factory to create a ConcreteAIConversationClient."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in the environment")

    available_models = ["models/gemini-1.5-pro-latest"]  # or other valid models

    provider = GeminiProvider(available_models=available_models, api_key=api_key)
    repository = ConcreteThreadRepository()
    client = ConcreteAIConversationClient(provider, repository)
    return client
