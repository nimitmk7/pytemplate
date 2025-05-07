"""Unit tests for the process_emails in main.py used in the Mail AI application."""
from unittest.mock import MagicMock, patch

import pytest

from mail_ai_app.main import process_emails


@pytest.fixture
def fake_gmail_messages() -> list[object]:
    """Fixture that returns fake Gmail messages."""

    class FakeMessage:
        """A fake message mimicking the real Gmail message object."""

        def __init__(self, id: str, body: str, subject: str, date: str) -> None:
            self.id = id
            self.body = body
            self.subject = subject
            self.date = date

    return [
        FakeMessage(
            id="id1",
            body="Fake email body 1",
            subject="Subject 1",
            date="2024-05-10",
        ),
        FakeMessage(
            id="id2",
            body="Fake email body 2",
            subject="Subject 2",
            date="2024-05-11",
        ),
    ]


@patch("mail_ai_app.main.input", return_value="2")
@patch("mail_ai_app.main.GmailClient")
@patch("mail_ai_app.main.ConcreteAIConversationClient")
def test_main_flow(
    mock_ai_client_cls: MagicMock,
    mock_gmail_client_cls: MagicMock,
    mock_input: MagicMock,
    fake_gmail_messages: list[object],
) -> None:
    """Test the main application flow with mocked dependencies."""
    # Mock Gmail client behavior
    mock_gmail_client = MagicMock()
    mock_gmail_client.get_messages.return_value = iter(fake_gmail_messages)
    mock_gmail_client_cls.return_value = mock_gmail_client

    # Mock AI conversation client behavior
    mock_ai_client = MagicMock()
    mock_ai_client.post_message_to_thread.return_value = "0.3"  # Fake AI response
    mock_ai_client_cls.return_value = mock_ai_client

    # Run main (no assertion needed if no exception is raised)
    process_emails()

    # Verify that Gmail messages were fetched
    mock_gmail_client.get_messages.assert_called_once()

    # Verify that AI model was called the expected number of times
    assert mock_ai_client.post_message_to_thread.call_count == 2
