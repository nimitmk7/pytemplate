"""Unit tests for GeminiProvider."""

from unittest.mock import MagicMock

import pytest

from ai_conversation_client_impl.client import GeminiProvider


@pytest.fixture(autouse=True)
def patch_genai(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch genai functions globally for these tests."""
    # Patch genai.configure to do nothing
    monkeypatch.setattr(
        "ai_conversation_client_impl.client.genai.configure",
        lambda api_key: None,
    )
    # Patch genai.GenerativeModel to always return a mock model
    mock_gemini_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "mocked response"
    mock_gemini_model.generate_content.return_value = mock_response
    monkeypatch.setattr(
        "ai_conversation_client_impl.client.genai.GenerativeModel",
        lambda model_name: mock_gemini_model,
    )

def test_generate_response_returns_expected_text() -> None:
    """Test that GeminiProvider returns expected mocked response."""
    provider = GeminiProvider(available_models=["gemini-pro"], api_key="fake-api-key")
    response = provider.generate_response("gemini-pro", "Hello!")

    assert response == "mocked response"

def test_generate_response_raises_for_invalid_model() -> None:
    """Test that ValueError is raised for unavailable model."""
    provider = GeminiProvider(available_models=["gemini-pro"], api_key="fake-api-key")

    with pytest.raises(ValueError, match="Model gemini-1.5-pro is not available"):
        provider.generate_response("gemini-1.5-pro", "Hello!")
