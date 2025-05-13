from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

import ai_conversation_client.api as api_module


@pytest.fixture
def mock_client() -> Generator[MagicMock, None, None]:
    with patch.object(api_module, "_client") as mock:
        yield mock

def test_create_thread(mock_client: MagicMock) -> None:
    mock_thread = MagicMock()
    mock_thread.get_id.return_value = "mocked-thread-id"
    mock_client.create_thread.return_value = mock_thread

    thread_id = api_module.create_thread()

    mock_client.create_thread.assert_called_once()
    assert thread_id == "mocked-thread-id"

def test_post_message(mock_client: MagicMock) -> None:
    mock_client.post_message_to_thread.return_value = "Mocked response"

    response = api_module.post_message("thread-id", "Hello!")

    mock_client.post_message_to_thread.assert_called_once_with("thread-id", "Hello!")
    assert response == "Mocked response"

def test_update_model(mock_client: MagicMock) -> None:
    api_module.update_model("thread-id", "new-model")
    mock_client.update_thread_model.assert_called_once_with("thread-id", "new-model")

def test_get_thread(mock_client: MagicMock) -> None:
    mock_thread = MagicMock()
    mock_client.get_thread.return_value = mock_thread

    thread = api_module.get_thread("thread-id")

    mock_client.get_thread.assert_called_once_with("thread-id")
    assert thread is mock_thread

def test_delete_thread(mock_client: MagicMock) -> None:
    api_module.delete_thread("thread-id")
    mock_client.delete_thread.assert_called_once_with("thread-id")

def test_list_models(mock_client: MagicMock) -> None:
    mock_client.fetch_available_models.return_value = ["model-1", "model-2"]

    models = api_module.list_models()

    mock_client.fetch_available_models.assert_called_once()
    assert models == ["model-1", "model-2"]
