"""Unit tests for ConcreteThreadRepository."""

import pytest

from ai_conversation_client.interfaces import ModelProvider
from ai_conversation_client_impl.client import (
    ConcreteThread,
    ConcreteThreadRepository,
)


class DummyModelProvider(ModelProvider):
    """Dummy model provider used for thread construction."""

    def __init__(self) -> None:
        """Initialize the dummy provider with mock models and response."""
        self._models = ["gpt-4"]
        self._response = "mocked response"

    def get_available_models(self) -> list[str]:
        """Return a list of available dummy model names."""
        return self._models

    def generate_response(
        self,
        model_name: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Return a mocked response string regardless of input."""
        return self._response

    def get_default_model(self) -> str:
        """Return the default model name."""
        return self._models[0]


@pytest.fixture
def model_provider() -> DummyModelProvider:
    return DummyModelProvider()


@pytest.fixture
def thread(model_provider: DummyModelProvider) -> ConcreteThread:
    return ConcreteThread(model_provider)


@pytest.fixture
def thread_repo() -> ConcreteThreadRepository:
    return ConcreteThreadRepository()


def test_save_and_get_by_id(
    thread_repo: ConcreteThreadRepository,
    thread: ConcreteThread,
) -> None:
    """Test saving and retrieving a thread by ID."""
    thread_repo.save(thread)
    retrieved = thread_repo.get_by_id(thread.get_id())
    assert retrieved is thread


def test_get_all_returns_all_threads(
    thread_repo: ConcreteThreadRepository,
    thread: ConcreteThread,
) -> None:
    """Test get_all returns all saved threads."""
    thread_repo.save(thread)
    all_threads = thread_repo.get_all()
    assert thread in all_threads


def test_delete_existing_thread(
    thread_repo: ConcreteThreadRepository,
    thread: ConcreteThread,
) -> None:
    """Test deleting an existing thread."""
    thread_repo.save(thread)
    thread_repo.delete(thread.get_id())
    assert thread.get_id() not in [t.get_id() for t in thread_repo.get_all()]


def test_delete_nonexistent_thread_raises(
    thread_repo: ConcreteThreadRepository,
) -> None:
    """Test deleting a non-existent thread raises ValueError."""
    with pytest.raises(ValueError):
        thread_repo.delete("nonexistent-id")


def test_get_by_id_invalid_id_raises(
    thread_repo: ConcreteThreadRepository,
) -> None:
    """Test retrieving a thread by invalid ID raises ValueError."""
    with pytest.raises(ValueError):
        thread_repo.get_by_id("invalid-id")
