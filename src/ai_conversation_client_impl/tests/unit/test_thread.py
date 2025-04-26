"""Unit tests for ConcreteThread class."""

import pytest

from ai_conversation_client.interfaces import ModelProvider
from ai_conversation_client_impl.client import ConcreteThread, Role


class MockModelProvider(ModelProvider):
    def __init__(self) -> None:
        self._models = ["gpt-4", "gpt-3.5"]
        self._response = "Mocked response"

    def get_available_models(self) -> list[str]:
        """Return a list of available mock model names."""
        return self._models

    def generate_response(
        self,
        model_name: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Return a fixed mock response string."""
        return self._response

    def get_default_model(self) -> str:
        """Return the first mock model name as the default."""
        return self._models[0]


@pytest.fixture
def thread() -> ConcreteThread:
    return ConcreteThread(MockModelProvider())


def test_thread_initializes_with_system_message(thread: ConcreteThread) -> None:
    assert len(thread.history) == 1
    assert thread.history[0].role == Role.SYSTEM


def test_thread_post_appends_user_and_response(thread: ConcreteThread) -> None:
    result = thread.post("Hello")
    assert result == "Mocked response"
    assert thread.history[-2].role == Role.USER
    assert thread.history[-2].content == "Hello"
    assert thread.history[-1].role == Role.ASSISTANT
    assert thread.history[-1].content == "Mocked response"


def test_thread_get_id_returns_valid_uuid(thread: ConcreteThread) -> None:
    thread_id = thread.get_id()
    assert isinstance(thread_id, str)
    assert len(thread_id) > 0


def test_thread_update_model_success(thread: ConcreteThread) -> None:
    thread.update_model("gpt-3.5")
    assert thread.model_name == "gpt-3.5"


def test_thread_update_model_invalid_raises(thread: ConcreteThread) -> None:
    with pytest.raises(ValueError, match="Model invalid-model is not available"):
        thread.update_model("invalid-model")
