"""Main application script for integrating Gmail client and AI conversation client.

This script:
- Crawls a Gmail inbox for emails.
- Sends email bodies to an AI model to determine the probability of being spam.
- Saves the results into a CSV file with columns: mail_id, Pct_spam, subject, and date.
"""

import csv
import os
import sys

from ai_conversation_client_impl.client import (
    ConcreteAIConversationClient,
    ConcreteThreadRepository,
    GeminiProvider,
)
from gmail.mail_gmail_impl.gmail_client import GmailClient
from mail_ai_app.prompt_utils import build_spam_check_prompt, parse_spam_probability


def _raise_positive_integer_error() -> None:
    raise ValueError("The number of emails must be a positive integer.")


def process_emails(
    gmail_client: GmailClient | None = None,
    ai_client: ConcreteAIConversationClient | None = None,
    max_emails: int | None = None,
) -> None:
    """Crawls mailbox using GmailClient, sends each email body to AIConversationClient
    with a spam-checking prompt, parses the AI's response for spam probability,
    and outputs a CSV with mail_id, Pct_spam, subject, and date columns.
    """
    print("Starting email processing...")

    # Initialize Gmail client (using credentials.json, token.json) if not provided
    if gmail_client is None:
        try:
            gmail_client = GmailClient()  # type: ignore
        except Exception as e:
            print(f"Failed to initialize Gmail client: {e}", file=sys.stderr)
            sys.exit(1)

    # Initialize AI conversation client using Gemini if not provided
    if ai_client is None:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key is None:
            error_msg = "Error: GEMINI_API_KEY must be set in environment variables."
            print(error_msg, file=sys.stderr)
            sys.exit(1)

        model_provider = GeminiProvider(
            available_models=["gemini-2.0-flash"],
            api_key=gemini_api_key,
        )
        thread_repository = ConcreteThreadRepository()
        ai_client = ConcreteAIConversationClient(
            model_provider=model_provider,
            thread_repository=thread_repository,
        )

    # Ask user how many emails to process if not provided
    if max_emails is None:
        try:
            max_emails_input = input("Enter the number of emails to process: ")
            max_emails = int(max_emails_input)
            if max_emails <= 0:
                _raise_positive_integer_error()
        except ValueError:
            error_msg = (
                "Please enter a valid positive integer for the number of emails."
            )
            print(error_msg, file=sys.stderr)
            sys.exit(1)

    results: list[dict[str, str]] = []

    # Fetch emails from mailbox
    for idx, email in enumerate(gmail_client.get_messages()):
        if idx >= max_emails:
            break

        print(f"Processing email {idx + 1}/{max_emails}...")

        mail_id: str = email.id
        body: str = email.body
        subject: str = email.subject
        date: str = email.date

        # Build spam-checking prompt
        prompt = build_spam_check_prompt(body)

        # Send prompt to AI client
        thread = ai_client.create_thread()
        response_text = ai_client.post_message_to_thread(
            thread_id=thread.get_id(),
            message=prompt,
        )

        # Parse spam probability
        pct_spam = parse_spam_probability(response_text) or 0.5

        # Use subject as snippet (since body might contain images or markup)
        snippet = subject.strip()

        results.append(
            {
                "mail_id": mail_id,
                "Pct_spam": str(pct_spam),
                "subject": snippet,
                "date": date,
            }
        )

    output_filename = "email_spam_analysis.csv"
    # Output results to CSV
    try:
        with open(
            output_filename,
            mode="w",
            newline="",
            encoding="utf-8",
        ) as csvfile:
            fieldnames = ["mail_id", "Pct_spam", "subject", "date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    except Exception as e:
        print(f"Failed to write CSV file: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Processing complete. Results saved to '{output_filename}'.")


if __name__ == "__main__":
    process_emails()
