from ai_conversation_client_impl.client import (
    ConcreteAIConversationClient,
    ConcreteThreadRepository,
    GeminiProvider,
)

_client = None  # type: ConcreteAIConversationClient | None

def _get_client() -> ConcreteAIConversationClient:
    """Lazy initialization of the AI conversation client."""
    global _client
    if _client is None:
        _client = ConcreteAIConversationClient(
            GeminiProvider(available_models=["models/gemini-1.5-pro-latest"]),
            ConcreteThreadRepository(),
        )
    return _client

def create_thread() -> str:
    """Create a new thread."""
    thread = _get_client().create_thread()
    return thread.get_id()

def post_message(thread_id: str, message: str) -> str:
    """Post a message to a thread."""
    return _get_client().post_message_to_thread(thread_id, message)

def update_model(thread_id: str, model_name: str) -> None:
    """Update the model for a given thread."""
    _get_client().update_thread_model(thread_id, model_name)

def get_thread(thread_id: str) -> object:
    """Retrieve a thread by ID."""
    return _get_client().get_thread(thread_id)

def delete_thread(thread_id: str) -> None:
    """Delete a thread by ID."""
    _get_client().delete_thread(thread_id)

def list_models() -> list[str]:
    """List available models."""
    return _get_client().fetch_available_models()
