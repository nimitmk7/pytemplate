"""Tests for the AI conversation client interfaces."""

import uuid

import pytest

from ai_conversation_client.interfaces import (
    AIConversationClient,
    ModelProvider,
    Thread,
    ThreadRepository,
)


# Dummy implementation for Thread
class DummyThread(Thread):
    """A dummy implementation of Thread for testing."""

<<<<<<< HEAD
    def __init__(self, thread_id: str, model_name: str = "default-model"):
        self._id = thread_id
        self._model_name = model_name
        self._messages = []
=======
    def __init__(self, thread_id: str, model_name: str = "default-model") -> None:
        self._id = thread_id
        self._model_name = model_name
        self._messages: list[str] = []
>>>>>>> interface-definition

    def post(self, message: str) -> str:
        """Post a message and get a dummy response."""
        self._messages.append(message)
        return f"Response to: {message}"

    def update_model(self, model_name: str) -> None:
        """Update the model name."""
        self._model_name = model_name

    def get_id(self) -> str:
        """Get the thread ID."""
        return self._id


# Dummy implementation for ModelProvider
class DummyModelProvider(ModelProvider):
    """A dummy implementation of ModelProvider for testing."""

<<<<<<< HEAD
    def __init__(self):
=======
    def __init__(self) -> None:
>>>>>>> interface-definition
        self._models = ["model-1", "model-2", "model-3"]

    def get_available_models(self) -> list[str]:
        """Get available models."""
        return self._models

    def generate_response(self, model_name: str, prompt: str) -> str:
        """Generate a dummy response."""
        if model_name not in self._models:
            msg = f"Model {model_name} not available"
            raise ValueError(msg)
        return f"Response from {model_name}: {prompt}"

    def get_default_model(self) -> str:
        """Get the default model name."""
        return self._models[0]


# Dummy implementation for ThreadRepository
class DummyThreadRepository(ThreadRepository):
    """A dummy implementation of ThreadRepository for testing."""

<<<<<<< HEAD
    def __init__(self):
=======
    def __init__(self) -> None:
>>>>>>> interface-definition
        self._threads: dict[str, Thread] = {}

    def save(self, thread: Thread) -> None:
        """Save a thread."""
        self._threads[thread.get_id()] = thread

    def get_by_id(self, thread_id: str) -> Thread:
        """Get a thread by ID."""
        if thread_id not in self._threads:
            msg = f"Thread {thread_id} not found"
            raise ValueError(msg)
        return self._threads[thread_id]

    def get_all(self) -> list[Thread]:
        """Get all threads."""
        return list(self._threads.values())

    def delete(self, thread_id: str) -> None:
        """Delete a thread."""
        if thread_id not in self._threads:
            msg = f"Thread {thread_id} not found"
            raise ValueError(msg)
        del self._threads[thread_id]


# Dummy implementation for AIConversationClient
class DummyAIConversationClient(AIConversationClient):
    """A dummy implementation of AIConversationClient for testing."""

<<<<<<< HEAD
    def __init__(self, model_provider: ModelProvider, thread_repository: ThreadRepository):
=======
    def __init__(
        self, model_provider: ModelProvider, thread_repository: ThreadRepository
    ) -> None:
>>>>>>> interface-definition
        self._model_provider = model_provider
        self._thread_repository = thread_repository

    def create_thread(self) -> Thread:
        """Create a new thread."""
        thread_id = str(uuid.uuid4())
        thread = DummyThread(thread_id)
        self._thread_repository.save(thread)
        return thread

    def get_thread(self, thread_id: str) -> Thread:
        """Get a thread by ID."""
        return self._thread_repository.get_by_id(thread_id)

    def get_all_threads(self) -> list[Thread]:
        """Get all threads."""
        return self._thread_repository.get_all()

    def delete_thread(self, thread_id: str) -> None:
        """Delete a thread."""
        self._thread_repository.delete(thread_id)

    def fetch_available_models(self) -> list[str]:
        """Get available models."""
        return self._model_provider.get_available_models()


# Tests for Thread interface
class TestThread:
    """Tests for the Thread interface."""

    @pytest.fixture
    def thread(self) -> Thread:
        """Create a dummy thread for testing."""
        return DummyThread("test-thread-id")

    def test_post_returns_response(self, thread: Thread) -> None:
        """Test that post() returns a response string."""
        response = thread.post("Hello")
        assert isinstance(response, str)
        assert "Hello" in response

    def test_update_model_changes_model(self, thread: Thread) -> None:
        """Test that update_model() works correctly."""
        # This test verifies the method doesn't raise an exception
        thread.update_model("new-model")

    def test_get_id_returns_string(self, thread: Thread) -> None:
        """Test that get_id() returns a string ID."""
        thread_id = thread.get_id()
        assert isinstance(thread_id, str)
        assert thread_id == "test-thread-id"


# Tests for AIConversationClient interface
class TestAIConversationClient:
    """Tests for the AIConversationClient interface."""

    @pytest.fixture
    def client(self) -> AIConversationClient:
        """Create a dummy client for testing."""
        model_provider = DummyModelProvider()
        thread_repository = DummyThreadRepository()
        return DummyAIConversationClient(model_provider, thread_repository)

    def test_create_thread_returns_thread(self, client: AIConversationClient) -> None:
        """Test that create_thread() returns a Thread object."""
        thread = client.create_thread()
        assert isinstance(thread, Thread)

    def test_get_thread_returns_thread(self, client: AIConversationClient) -> None:
        """Test that get_thread() returns a Thread object."""
        # Create a thread first
        thread = client.create_thread()
        thread_id = thread.get_id()

        # Now get it
        retrieved_thread = client.get_thread(thread_id)
        assert isinstance(retrieved_thread, Thread)
        assert retrieved_thread.get_id() == thread_id

    def test_get_all_threads_returns_list(self, client: AIConversationClient) -> None:
        """Test that get_all_threads() returns a list of Thread objects."""
        # Create some threads
        thread1 = client.create_thread()
        thread2 = client.create_thread()

        # Get all threads
        threads = client.get_all_threads()
        assert isinstance(threads, list)
        assert all(isinstance(t, Thread) for t in threads)
        thread_ids = [t.get_id() for t in threads]
        assert thread1.get_id() in thread_ids
        assert thread2.get_id() in thread_ids

    def test_delete_thread_removes_thread(self, client: AIConversationClient) -> None:
        """Test that delete_thread() removes a thread."""
        # Create a thread
        thread = client.create_thread()
        thread_id = thread.get_id()

        # Delete it
        client.delete_thread(thread_id)

        # Verify it's gone
        with pytest.raises(ValueError):
            client.get_thread(thread_id)

<<<<<<< HEAD
    def test_fetch_available_models_returns_list(self, client: AIConversationClient) -> None:
=======
    def test_fetch_available_models_returns_list(
        self, client: AIConversationClient
    ) -> None:
>>>>>>> interface-definition
        """Test that fetch_available_models() returns a list of model names."""
        models = client.fetch_available_models()
        assert isinstance(models, list)
        assert all(isinstance(model, str) for model in models)
        assert len(models) > 0
