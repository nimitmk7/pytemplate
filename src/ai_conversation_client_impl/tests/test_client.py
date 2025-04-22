import pytest

from ai_conversation_client.interfaces import ModelProvider
from ai_conversation_client_impl.client import (
    ConcreteAIConversationClient,
    ConcreteThread,
    ConcreteThreadRepository,
)


class DummyModelProvider(ModelProvider):
    def __init__(self, available_models: list[str]):
        self._models = available_models

    def get_available_models(self) -> list[str]:
        return self._models

    def generate_response(
        self,
        model_name: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        return f"[{model_name}] {prompt}"

    def get_default_model(self) -> str:
        return self._models[0]


@pytest.fixture
def available_models() -> list[str]:
    return ["gpt-4", "gpt-3.5-turbo"]


@pytest.fixture
def model_provider(available_models: list[str]) -> DummyModelProvider:
    return DummyModelProvider(available_models)


@pytest.fixture
def thread_repository() -> ConcreteThreadRepository:
    return ConcreteThreadRepository()


@pytest.fixture
def client(
    model_provider: DummyModelProvider,
    thread_repository: ConcreteThreadRepository,
) -> ConcreteAIConversationClient:
    return ConcreteAIConversationClient(model_provider, thread_repository)


def test_create_thread(client: ConcreteAIConversationClient) -> None:
    thread = client.create_thread()
    assert isinstance(thread, ConcreteThread)
    assert thread.get_id() in client.thread_repository.threads


def test_post_message(client: ConcreteAIConversationClient) -> None:
    thread = client.create_thread()
    response = client.post_message_to_thread(thread.get_id(), "Hello!")
    assert "[gpt-4] Hello!" in response


def test_update_thread_model(
    client: ConcreteAIConversationClient, available_models: list[str]
) -> None:
    thread = client.create_thread()
    client.update_thread_model(thread.get_id(), available_models[1])
    assert thread.model_name == available_models[1]


def test_get_thread(client: ConcreteAIConversationClient) -> None:
    thread = client.create_thread()
    retrieved = client.get_thread(thread.get_id())
    assert retrieved is thread


def test_get_all_threads(client: ConcreteAIConversationClient) -> None:
    client.create_thread()
    client.create_thread()
    threads = client.get_all_threads()
    assert len(threads) == 2


def test_delete_thread(client: ConcreteAIConversationClient) -> None:
    thread = client.create_thread()
    client.delete_thread(thread.get_id())
    assert thread.get_id() not in client.thread_repository.threads


def test_fetch_available_models(
    client: ConcreteAIConversationClient, available_models: list[str]
) -> None:
    models = client.fetch_available_models()
    assert models == available_models
