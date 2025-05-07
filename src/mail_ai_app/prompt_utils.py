"""Utilities for building prompts and parsing responses
for AI-based email spam probability detection.

This module contains:
- build_spam_check_prompt: Formats a prompt for the AI model given an email body.
- parse_spam_probability: Extracts and validates the spam probability
  from the AI model's response.
"""


def build_spam_check_prompt(email_body: str) -> str:
    """Builds a prompt to ask the AI to predict the spam probability for an email body.

    Args:
        email_body (str): The content of the email.

    Returns:
        str: The formatted prompt.
    """
    return (
        "You are an email spam detection expert.\n"
        "Given the following email, estimate the probability that it is spam.\n"
        "Respond ONLY with a single number between 0 and 1.\n\n"
        f"Email:\n{email_body}\n"
    )


def parse_spam_probability(ai_response: str) -> float | None:
    """Parses the AI response to extract a spam probability.

    Args:
        ai_response (str): The raw AI response.

    Returns:
        Optional[float]: The spam probability if valid, else None.
    """
    try:
        prob = float(ai_response.strip())
        if 0.0 <= prob <= 1.0:
            return prob
        else:
            return None
    except ValueError:
        return None
