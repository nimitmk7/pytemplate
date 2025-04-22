"""Implementation of the AI Conversation Client."""

import enum
import uuid
from dataclasses import dataclass
from typing import cast

from openai import OpenAI

from ai_conversation_client import (
    AIConversationClient as AIConversationClientInterface,
)
from ai_conversation_client import (
    ModelProvider as ModelProviderInterface,
)
from ai_conversation_client import (
    Thread as ThreadInterface,
)
from ai_conversation_client import (
    ThreadRepository as ThreadRepositoryInterface,
)


class Role(enum.StrEnum):
    """Represents the role of a participant in the conversation."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """A message exchanged in a thread."""
    role: Role
    content: str


class OpenAIProvider(ModelProviderInterface):
    """Provides access to OpenAI models and responses."""

    def __init__(self, api_key: str, available_models: list[str]) -> None:
        """Initialize the OpenAI provider."""
        self.open_ai_client = OpenAI(api_key=api_key)
        self.available_models = available_models
        self.default_model = available_models[0] if available_models else "gpt-4o"

    def get_available_models(self) -> list[str]:
        """Return the list of available model names."""
        return self.available_models

    def generate_response(
        self,
        model_name: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Generate a response using the specified model."""
        if model_name not in self.available_models:
            msg = f"Model {model_name} is not available."
            raise ValueError(msg)

        chat_response = self.open_ai_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return cast(str, chat_response.choices[0].message.content).strip()

    def get_default_model(self) -> str:
        """Return the default model name."""
        return self.default_model


class ConcreteThread(ThreadInterface):
    """Concrete implementation of a conversation thread."""

    def __init__(
        self,
        model_provider: ModelProviderInterface,
        message: str = "Hello!",
    ) -> None:
        """Initialize the thread with system message."""
        self.thread_id = str(uuid.uuid4())
        self.model_provider = model_provider
        self.model_name = model_provider.get_default_model()
        self.history: list[Message] = [Message(Role.SYSTEM, message)]

    def post(
        self,
        message: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Post a message and return the AI response."""
        self.history.append(Message(Role.USER, message))
        response = self.model_provider.generate_response(
            self.model_name,
            message,
            temperature,
            max_tokens,
        )
        self.history.append(Message(Role.ASSISTANT, response))
        return self.history[-1].content

    def get_id(self) -> str:
        """Return the thread's unique identifier."""
        return self.thread_id

    def update_model(self, model_name: str) -> None:
        """Update the AI model used in this thread."""
        if model_name not in self.model_provider.get_available_models():
            msg = f"Model {model_name} is not available."
            raise ValueError(msg)
        self.model_name = model_name


class ConcreteThreadRepository(ThreadRepositoryInterface):
    """In-memory repository for managing threads."""

    def __init__(self) -> None:
        """Initialize the thread repository."""
        self.threads: dict[str, ThreadInterface] = {}

    def save(self, thread: ThreadInterface) -> None:
        """Save a thread to the repository."""
        self.threads[thread.get_id()] = thread

    def get_by_id(self, thread_id: str) -> ThreadInterface:
        """Retrieve a thread by ID."""
        if thread_id not in self.threads:
            msg = f"Thread with ID {thread_id} not found."
            raise ValueError(msg)
        return self.threads[thread_id]

    def get_all(self) -> list[ThreadInterface]:
        """Return all stored threads."""
        return list(self.threads.values())

    def delete(self, thread_id: str) -> None:
        """Delete a thread by ID."""
        if thread_id not in self.threads:
            msg = f"Thread with ID {thread_id} not found."
            raise ValueError(msg)
        del self.threads[thread_id]


class ConcreteAIConversationClient(AIConversationClientInterface):
    """Client for managing AI conversation threads."""

    def __init__(
        self,
        model_provider: ModelProviderInterface,
        thread_repository: ThreadRepositoryInterface,
    ) -> None:
        """Initialize the conversation client."""
        self.model_provider = model_provider
        self.thread_repository = thread_repository

    def create_thread(self) -> ThreadInterface:
        """Create and store a new thread."""
        thread = ConcreteThread(self.model_provider)
        self.thread_repository.save(thread)
        return thread

    def get_thread(self, thread_id: str) -> ThreadInterface:
        """Get a thread by ID."""
        return self.thread_repository.get_by_id(thread_id)

    def get_all_threads(self) -> list[ThreadInterface]:
        """Get all threads."""
        return self.thread_repository.get_all()

    def update_thread_model(self, thread_id: str, model_name: str) -> None:
        """Update the model for a given thread."""
        thread = self.thread_repository.get_by_id(thread_id)
        thread.update_model(model_name)
        self.thread_repository.save(thread)

    def post_message_to_thread(
        self,
        thread_id: str,
        message: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Post a message to a thread and get the response."""
        thread = self.thread_repository.get_by_id(thread_id)
        return thread.post(message, temperature, max_tokens)

    def delete_thread(self, thread_id: str) -> None:
        """Delete a thread."""
        self.thread_repository.delete(thread_id)

    def fetch_available_models(self) -> list[str]:
        """List available models from the provider."""
        return self.model_provider.get_available_models()
