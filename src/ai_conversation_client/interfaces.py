"""Interfaces for the AI conversation client.

This module defines the abstract base classes for the AI conversation client,
following dependency injection principles.
"""

from abc import ABC, abstractmethod


class Thread(ABC):
    """A conversation thread between a user and an AI assistant."""

    @abstractmethod
    def post(self, message: str) -> str:
        """Post a message to the thread and get the AI's response.

        Args:
            message: The user's message to send to the AI.

        Returns:
            The AI assistant's response.
        """
        pass

    @abstractmethod
    def update_model(self, model_name: str) -> None:
        """Change the AI model used in this thread.

        Args:
            model_name: The name of the model to use.
        """
        pass

    @abstractmethod
    def get_id(self) -> str:
        """Get the unique identifier for this thread.

        Returns:
            The thread's unique ID.
        """
        pass


class ModelProvider(ABC):
    """Provider for AI model capabilities."""

    @abstractmethod
    def get_available_models(self) -> list[str]:
        """Get a list of available AI models.

        Returns:
            A list of model names as strings.
        """
        pass

    @abstractmethod
    def generate_response(self, model_name: str, prompt: str) -> str:
        """Generate a response using the specified model.

        Args:
            model_name: The name of the model to use.
            prompt: The prompt to send to the model.

        Returns:
            The generated response.
        """
        pass


class ThreadRepository(ABC):
    """Repository for storing and retrieving conversation threads."""

    @abstractmethod
    def save(self, thread: Thread) -> None:
        """Save a thread to the repository.

        Args:
            thread: The thread to save.
        """
        pass

    @abstractmethod
    def get_by_id(self, thread_id: str) -> Thread:
        """Get a thread by its ID.

        Args:
            thread_id: The ID of the thread to retrieve.

        Returns:
            The thread with the specified ID.

        Raises:
            ValueError: If no thread with the specified ID exists.
        """
        pass

    @abstractmethod
    def get_all(self) -> list[Thread]:
        """Get all threads.

        Returns:
            A list of all threads.
        """
        pass

    @abstractmethod
    def delete(self, thread_id: str) -> None:
        """Delete a thread.

        Args:
            thread_id: The ID of the thread to delete.

        Raises:
            ValueError: If no thread with the specified ID exists.
        """
        pass


class AIConversationClient(ABC):
    """Client for managing AI conversations."""

    @abstractmethod
    def __init__(
        self, model_provider: ModelProvider, thread_repository: ThreadRepository
    ) -> None:
        """Initialize the client with its dependencies.

        Args:
            model_provider: Provider for AI model capabilities.
            thread_repository: Repository for storing and retrieving threads.
        """
        pass

    @abstractmethod
    def create_thread(self) -> Thread:
        """Create a new conversation thread.

        Returns:
            A new thread.
        """
        pass

    @abstractmethod
    def get_thread(self, thread_id: str) -> Thread:
        """Get a thread by its ID.

        Args:
            thread_id: The ID of the thread to retrieve.

        Returns:
            The thread with the specified ID.

        Raises:
            ValueError: If no thread with the specified ID exists.
        """
        pass

    @abstractmethod
    def get_all_threads(self) -> list[Thread]:
        """Get all threads.

        Returns:
            A list of all threads.
        """
        pass

    @abstractmethod
    def delete_thread(self, thread_id: str) -> None:
        """Delete a thread.

        Args:
            thread_id: The ID of the thread to delete.

        Raises:
            ValueError: If no thread with the specified ID exists.
        """
        pass

    @abstractmethod
    def fetch_available_models(self) -> list[str]:
        """Get a list of available AI models.

        Returns:
            A list of model names.
        """
        pass
