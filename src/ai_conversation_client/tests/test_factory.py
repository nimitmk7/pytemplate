"""Unit tests for factory.py."""

import pytest

from ai_conversation_client.factory import create_client
from ai_conversation_client_impl.client import ConcreteAIConversationClient


@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fixture to ensure GEMINI_API_KEY is set during tests."""
    monkeypatch.setenv("GEMINI_API_KEY", "fake-api-key")


def test_create_client() -> None:
    """Test that create_client returns a ConcreteAIConversationClient."""
    client = create_client()
    assert isinstance(client, ConcreteAIConversationClient)

    models = client.fetch_available_models()
    assert "models/gemini-2.0-flash-lite" in models
