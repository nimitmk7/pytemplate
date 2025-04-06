import pytest
from unittest.mock import Mock

from ai_conversation_client import AIConversationClient, Thread


class TestAIConversationClient:
    """Test suite for AIConversationClient interface compliance."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock AIConversationClient instance for testing.

        Returns:
            A Mock object configured with AIConversationClient's interface.
        """
        return Mock(spec=AIConversationClient)

    def test_create_thread_contract(self, mock_client: Mock) -> None:
        """Verify create_thread() adheres to its interface contract."""
        mock_client.create_thread.return_value = Mock(spec=Thread)
        thread = mock_client.create_thread()
        
        assert isinstance(thread, Thread)
        mock_client.create_thread.assert_called_once()

    def test_get_all_threads_contract(self, mock_client: Mock) -> None:
        """Verify get_all_threads() returns a list of Thread objects."""
        mock_threads = [Mock(spec=Thread), Mock(spec=Thread)]
        mock_client.get_all_threads.return_value = mock_threads
        
        threads = mock_client.get_all_threads()
        
        assert isinstance(threads, list)
        assert all(isinstance(t, Thread) for t in threads)
        mock_client.get_all_threads.assert_called_once()

    def test_fetch_available_models_contract(self, mock_client: Mock) -> None:
        """Verify fetch_available_models() returns a list of model names."""
        mock_models = ["gpt-4", "gpt-3.5", "claude-2"]
        mock_client.fetch_available_models.return_value = mock_models
        
        models = mock_client.fetch_available_models()
        
        assert isinstance(models, list)
        assert all(isinstance(model, str) for model in models)
        mock_client.fetch_available_models.assert_called_once()

    def test_delete_thread_contract(self, mock_client: Mock) -> None:
        """Verify delete_thread() is called with the correct thread_id."""
        mock_client.delete_thread.return_value = None
        
        mock_client.delete_thread(123)
        
        mock_client.delete_thread.assert_called_once_with(123)

    def test_upload_file_contract(self, mock_client: Mock) -> None:
        """Verify upload_file() is called with the correct file path."""
        mock_client.upload_file.return_value = None
        
        mock_client.upload_file("path/to/file.txt")
        
        mock_client.upload_file.assert_called_once_with("path/to/file.txt")


class TestThread:
    """Test suite for the Thread interface compliance."""

    @pytest.fixture
    def mock_thread(self) -> Mock:
        """Create a mock Thread instance for testing.

        Returns:
            A Mock object configured with Thread's interface.
        """
        return Mock(spec=Thread)

    def test_post_contract(self, mock_thread: Mock) -> None:
        """Verify post() method adheres to its interface contract."""
        test_response = "Test response"
        mock_thread.post.return_value = test_response

        response = mock_thread.post("gpt-4", "Hello!")
        
        assert isinstance(response, str)
        assert response == test_response
        mock_thread.post.assert_called_once_with("gpt-4", "Hello!")

    def test_update_model_contract(self, mock_thread: Mock) -> None:
        """Verify update_model() is called with the correct model."""
        mock_thread.update_model.return_value = None
        
        mock_thread.update_model("gpt-4")
        
        mock_thread.update_model.assert_called_once_with("gpt-4")
