import os
from unittest.mock import MagicMock, patch

import pytest

from ai_conversation_client_impl.client import (
    ConcreteAIConversationClient,
    ConcreteThreadRepository,
    GeminiProvider,
)
from gmail.mail_gmail_impl.gmail_client import GmailClient


@pytest.fixture(scope="module")
def gmail_client() -> GmailClient:
    """Fixture to provide a Gmail client.

    Returns:
        GmailClient: Configured Gmail client instance.
    """
    credentials_file = os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
    token_file = os.getenv("GMAIL_TOKEN_FILE", "token.json")
    return GmailClient(credentials_file, token_file) # type: ignore


@pytest.fixture(scope="module")
def ai_client() -> ConcreteAIConversationClient:
    """Fixture to provide an AI conversation client.

    Returns:
        ConcreteAIConversationClient: Configured AI client instance.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY must be set")
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
    gmail_client: GmailClient,
    ai_client: ConcreteAIConversationClient,
) -> None:
    """End-to-end integration test from Gmail client to AI client.

    This test fetches an email via Gmail client, passes the email body to the AI client,
    and verifies that the AI client returns a valid response.

    Args:
        mock_post_message_to_thread (MagicMock): Mocked post_message_to_thread method.
        gmail_client (GmailClient): Gmail client fixture.
        ai_client (ConcreteAIConversationClient): AI conversation client fixture.
    """
    # Step 1: Fetch emails
    messages = list(gmail_client.get_messages())
    assert messages, "No messages found in Gmail account."

    # Step 2: Pick the first email body
    first_message = messages[0]
    email_body = first_message.body
    assert email_body, "First email body is empty."

    # Step 3: Pass email body to AI client
    thread = ai_client.create_thread()
    response_text = ai_client.post_message_to_thread(
        thread_id=thread.get_id(),
        message=email_body,
    )

    # Step 4: Check AI response
    assert response_text, "AI client returned no response."
