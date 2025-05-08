import os
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

from ai_conversation_client_impl.client import (
    ConcreteAIConversationClient,
    ConcreteThreadRepository,
    GeminiProvider,
)

if TYPE_CHECKING:
    from gmail.mail_gmail_impl.gmail_client import GmailClient


class FakeEmailMessage:
    """A simple fake email message object for testing."""
    def __init__(self, body: str, id: str, subject: str, date: str) -> None:
        self.body = body
        self.id = id
        self.subject = subject
        self.date = date


@pytest.fixture(scope="module")
def gmail_client() -> "GmailClient":
    """Fixture to provide a mocked Gmail client."""
    mock_client = MagicMock()
    mock_client.get_messages.return_value = [
        FakeEmailMessage(
            body="This is a test email body.",
            id="fake-id-123",
            subject="Test Subject",
            date="2024-05-10",
        )
    ]
    return mock_client


@pytest.fixture(scope="module")
def ai_client() -> ConcreteAIConversationClient:
    """Fixture to provide an AI conversation client."""
    api_key = os.getenv("GEMINI_API_KEY", "fake-api-key")
    provider = GeminiProvider(
        available_models=["models/gemini-1.5-pro-latest"],
        api_key=api_key,
    )
    repository = ConcreteThreadRepository()
    return ConcreteAIConversationClient(provider, repository)


@patch(
    "ai_conversation_client_impl.client.ConcreteAIConversationClient.post_message_to_thread",
    return_value="Mocked AI response",
)
def test_gmail_to_ai_integration(
    mock_post_message_to_thread: MagicMock,
    gmail_client: "GmailClient",
    ai_client: ConcreteAIConversationClient,
) -> None:
    """End-to-end integration test from Gmail client to AI client."""
    messages = list(gmail_client.get_messages())
    assert messages, "No messages found in Gmail account."

    first_message = messages[0]
    email_body = first_message.body
    assert email_body, "First email body is empty."

    thread = ai_client.create_thread()
    response_text = ai_client.post_message_to_thread(
        thread_id=thread.get_id(),
        message=email_body,
    )

    assert response_text, "AI client returned no response."
