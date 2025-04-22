"""Unit tests for OpenAIProvider."""

from unittest.mock import MagicMock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from ai_conversation_client_impl.client import OpenAIProvider


def test_generate_response_returns_expected_text(
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that OpenAIProvider returns expected mocked response."""
    mock_openai = MagicMock()
    mock_chat_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "mocked response"
    mock_chat_response.choices = [mock_choice]
    mock_openai.chat.completions.create.return_value = mock_chat_response

    monkeypatch.setattr(
        "ai_conversation_client_impl.client.OpenAI", lambda api_key: mock_openai
    )

    provider = OpenAIProvider(api_key="fake-key", available_models=["gpt-4"])
    response = provider.generate_response("gpt-4", "Hello!")

    assert response == "mocked response"


def test_generate_response_raises_for_invalid_model() -> None:
    """Test that ValueError is raised for unavailable model."""
    provider = OpenAIProvider(api_key="fake-key", available_models=["gpt-4"])

    with pytest.raises(ValueError, match="Model gpt-3.5-turbo is not available"):
        provider.generate_response("gpt-3.5-turbo", "Hello!")
