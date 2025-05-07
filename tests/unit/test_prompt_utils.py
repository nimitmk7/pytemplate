from mail_ai_app.prompt_utils import build_spam_check_prompt, parse_spam_probability


def test_build_spam_check_prompt() -> None:
    email_body = "This is a sample email."
    prompt = build_spam_check_prompt(email_body)
    assert "This is a sample email." in prompt
    assert "Respond ONLY with a single number between 0 and 1." in prompt


def test_parse_spam_probability_valid() -> None:
    response_text = "0.8"
    prob = parse_spam_probability(response_text)
    assert prob == 0.8


def test_parse_spam_probability_invalid() -> None:
    response_text = "I don't know"
    prob = parse_spam_probability(response_text)
    assert prob is None
