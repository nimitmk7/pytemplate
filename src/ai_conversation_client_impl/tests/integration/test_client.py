"""Tests for ConcreteAIConversationClient and related classes."""

from typing import cast
from unittest.mock import patch

import pytest

from ai_conversation_client_impl.client import (
    ConcreteAIConversationClient,
    ConcreteThread,
    ConcreteThreadRepository,
    OpenAIProvider,
)


@pytest.fixture
def available_models() -> list[str]:
    """Fixture for available models."""
    return ["gpt-4", "gpt-3.5-turbo"]


@pytest.fixture
def model_provider(available_models: list[str]) -> OpenAIProvider:
    """Fixture for OpenAIProvider with mocked API key."""
    return OpenAIProvider(api_key="fake-api-key", available_models=available_models)


@pytest.fixture
def thread_repository() -> ConcreteThreadRepository:
    """Fixture for thread repository."""
    return ConcreteThreadRepository()


@pytest.fixture
def client(
    model_provider: OpenAIProvider,
    thread_repository: ConcreteThreadRepository,
) -> ConcreteAIConversationClient:
    """Fixture for AI conversation client."""
    return ConcreteAIConversationClient(model_provider, thread_repository)


def test_create_thread(client: ConcreteAIConversationClient) -> None:
    """Test creating a thread stores it in the repository."""
    thread = client.create_thread()
    repo = cast(ConcreteThreadRepository, client.thread_repository)
    assert thread.get_id() in repo.threads


@patch.object(OpenAIProvider, "generate_response", return_value="[gpt-4] Hello!")
def test_post_message(
    mock_generate_response: object, client: ConcreteAIConversationClient
) -> None:
    """Test posting a message returns the mocked response."""
    thread = client.create_thread()
    response = client.post_message_to_thread(thread.get_id(), "Hello!")
    assert "[gpt-4] Hello!" in response


def test_update_thread_model(
    client: ConcreteAIConversationClient, available_models: list[str]
) -> None:
    """Test updating the thread's model name."""
    thread = client.create_thread()
    client.update_thread_model(thread.get_id(), available_models[1])
    concrete_thread = thread  # already ConcreteThread
    assert isinstance(concrete_thread, ConcreteThread)
    assert concrete_thread.model_name == available_models[1]


def test_get_thread(client: ConcreteAIConversationClient) -> None:
    """Test retrieving a specific thread by ID."""
    thread = client.create_thread()
    retrieved = client.get_thread(thread.get_id())
    assert retrieved is thread


def test_get_all_threads(client: ConcreteAIConversationClient) -> None:
    """Test getting all stored threads."""
    client.create_thread()
    client.create_thread()
    threads = client.get_all_threads()
    assert len(threads) == 2


def test_delete_thread(client: ConcreteAIConversationClient) -> None:
    """Test deleting a thread removes it from the repository."""
    thread = client.create_thread()
    client.delete_thread(thread.get_id())
    repo = cast(ConcreteThreadRepository, client.thread_repository)
    assert thread.get_id() not in repo.threads


def test_fetch_available_models(
    client: ConcreteAIConversationClient,
    available_models: list[str],
) -> None:
    """Test listing available models."""
    models = client.fetch_available_models()
    assert models == available_models
