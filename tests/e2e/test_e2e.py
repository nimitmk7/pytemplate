"""End-to-end test for Gmail client and AI conversation client integration.

This test uses real credentials to verify the actual integration between
the Gmail client and AI conversation client. It's primarily intended for
local development and verification, and will be skipped if credentials
are not available.

Note: These tests make actual API calls to Gmail and Gemini services,
which may incur costs or affect API quotas.
"""

import csv
import os
import re

import pytest

pytestmark = pytest.mark.skipif(
    not os.path.exists("credentials.json"),
    reason="Credentials for Gmail and/or GEMINI_API_KEY not found"
)

print("Starting e2e test...")

def test_email_analysis_workflow() -> None:
    """Test the full workflow of analyzing emails for spam using the AI model."""
    from mail_gmail_impl import get_gmail_client

    from ai_conversation_client.factory import create_client

    gmail_client = get_gmail_client(credentials_file="credentials.json")
    ai_client = create_client()

    try:
        emails = list(gmail_client.get_messages())[:3]
        results = []

        if not emails:
            pytest.skip("No emails available for testing")

        print(f"Processing {len(emails)} emails...")

        for i, email in enumerate(emails):
            print(f"Email {i+1}: {email.subject[:30]}...")

            # Create a new thread for each email
            thread = ai_client.create_thread()

            # Create the prompt for spam analysis
            prompt = f"""
            Analyze this email and determine if it's spam.
            Respond with a single number between 0 and 100 representing the percentage
            probability that this email is spam.

            From: {email.from_}
            Subject: {email.subject}
            Body: {email.body[:1000]}
            Percentage (0-100):
            """

            response = ai_client.post_message_to_thread(thread.get_id(), prompt)
            print(f"  Response received: {response[:50]}...")

            try:
                spam_pct_match = re.search(r'(\d+)(?:\.\d+)?', response)
                spam_pct = int(spam_pct_match.group(1)) if spam_pct_match else 0
                print(f"  Extracted spam percentage: {spam_pct}%")
            except Exception as e:
                print(f"  Failed to extract percentage: {e}")
                spam_pct = 0

            results.append({
                "mail_id": email.id,
                "from": email.from_,
                "subject": email.subject,
                "pct_spam": spam_pct
            })

        # Write results to a CSV file
        output_path = "email_analysis_results.csv"
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['mail_id', 'from', 'subject', 'pct_spam']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)

        print(f"Results written to {output_path}")

        assert os.path.exists(output_path)

        # Read back and verify the CSV
        with open(output_path) as csvfile:
            reader = csv.DictReader(csvfile)
            csv_rows = list(reader)
            assert len(csv_rows) == len(results)
            assert all(row['mail_id'] for row in csv_rows)
            assert all(row['pct_spam'] for row in csv_rows)

        # Clean up
        os.remove(output_path)
        print("Test completed successfully")

    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        pytest.fail(f"E2E test failed: {e}")
