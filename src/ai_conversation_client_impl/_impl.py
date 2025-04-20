from ai_conversation_client import AIConversationClient, ModelProvider, Thread, ThreadRepository
from openai import OpenAI
import uuid

class OpenAIProvider(ModelProvider):
    def __init__(self, api_key: str, available_models: list[str]):
        self.open_ai_client = OpenAI(api_key=api_key)
        self.available_models = available_models
        self.default_model = available_models[0] if available_models else "gpt-4o"
    
    def get_available_models(self) -> list[str]:
        """Return a list of available AI model names.

        Returns:
            list[str]: A list containing the names of available models.
        """
        return self.available_models
    
    def generate_response(self, model_name: str, prompt: str, temperature:float = 0.7, max_tokens:int= 500) -> str:
        if model_name not in self.available_models:
            raise ValueError(f"Model {model_name} is not available.")

        chat_response = self.open_ai_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return chat_response.choices[0].message.content.strip()
    
    def get_default_model(self) -> str:
        return self.default_model
    
class Thread(Thread):
    def __init__(self, model_provider: ModelProvider):
        self.thread_id = str(uuid.uuid4())
        self.model_provider = model_provider
        self.model_name = model_provider.get_default_model()

    def post(self, message: str) -> str:
        """Post a message to the thread and get the AI's response.
        
        Args:
            message (str): The user's message to send to the AI.
        
        Returns:
            str: The AI assistant's response.
        """
        return self.model_provider.generate_response(self.model_name, message)

    def get_id(self) -> str:
        """Get the unique identifier for this thread.

        Returns:
            str: The unique thread ID.
        """
        return self.thread_id
    
    def update_model(self, model_name: str) -> None:
        """Update the model used in this thread.
        Args:
            model_name (str): The name of the model to use.
        """
        if model_name not in self.model_provider.get_available_models():
            raise ValueError(f"Model {model_name} is not available.")
        self.model_name = model_name

class ThreadRepository(ThreadRepository):
    def __init__(self):
        self.threads = {}

    def save(self, thread: Thread):
        """Save a thread to the repository.
        
        Args:
            thread (Thread): The thread to save.
        """
        self.threads[thread.get_id()] = thread

    def get_by_id(self, thread_id: str) -> Thread:
        """Get a thread by its ID.
        
        Args:
            thread_id (str): The ID of the thread to retrieve.
        
        Returns:
            Thread: The thread with the specified ID.
        """
        if thread_id not in self.threads:
            raise ValueError(f"Thread with ID {thread_id} not found.")
        return self.threads[thread_id]

    def get_all(self) -> list[Thread]:
        """Get all threads in the repository.
        
        Returns:
            list[Thread]: A list of all threads.
        """
        return list(self.threads.values())

class AIConversationClient(AIConversationClient):
    def __init__(self, model_provider: ModelProvider, thread_repository):
        self.model_provider = model_provider
        self.thread_repository = thread_repository

    def create_thread(self) -> Thread:
        thread = Thread(self.model_provider)
        self.thread_repository.save(thread)
        return thread
    
    def get_thread(self, thread_id: str) -> Thread:
        return self.thread_repository.get_by_id(thread_id)
    
    def get_all_threads(self) -> list[Thread]:
        return self.thread_repository.get_all()
    
    def delete_thread(self, thread_id: str) -> None:
        self.thread_repository.delete(thread_id)

    def fetch_available_models(self) -> list[str]:
        return self.model_provider.get_available_models()
    
    
    

    



        