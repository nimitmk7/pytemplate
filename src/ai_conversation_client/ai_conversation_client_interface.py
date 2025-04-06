from typing import Protocol, List, runtime_checkable


@runtime_checkable
class Thread(Protocol):
    """A conversation thread."""

    def post(self, model: str, message: str) -> str:
        """Post a message to the thread.

        The method returns the response of the AI Assistant.
        """
        raise NotImplementedError()
    
    def update_model(self, model: str) -> None:
        """Change the AI model used in the thread."""
        raise NotImplementedError()
    
    
@runtime_checkable
class AIConversationClient(Protocol):
    """An AI Assistant Client used to maintain conversation threads."""

    def __init__(self, api_key: str):
        """Initialize the AI Assistant Client with an API key."""
        raise NotImplementedError()
    
    def create_thread(self) -> Thread:
        """Create a new conversation thread."""
        raise NotImplementedError()
    
    def get_all_threads(self) -> List[Thread]:
        """View all conversation threads."""
        raise NotImplementedError()
    
    def fetch_available_models(self) -> List[str]:
        """Fetch all available models."""
        raise NotImplementedError()
    
    def delete_thread(self, thread_id: int) -> None:
        """Delete a conversation thread."""
        raise NotImplementedError()
    
    def upload_file(self, file_path: str) -> None:
        """Upload a file to the AI Assistant."""
        raise NotImplementedError()


def get_client() -> AIConversationClient:
    """Return an instance of a AI Assistant Client."""
    raise NotImplementedError()