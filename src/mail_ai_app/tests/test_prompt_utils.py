from mail_ai_app.prompt_utils import build_spam_check_prompt, parse_spam_probability


def test_build_spam_check_prompt() -> None:
    email_body = "This is a sample email."
    prompt = build_spam_check_prompt(email_body)
    assert "This is a sample email." in prompt
    assert "Respond ONLY with a single number between 0 and 1." in prompt


def test_parse_spam_probability_valid() -> None:
    for response_text, expected in [
        ("0.8", 0.8), ("0.5", 0.5), ("1.0", 1.0), ("0.0", 0.0)
    ]:
        prob = parse_spam_probability(response_text)
        assert prob == expected


def test_parse_spam_probability_invalid() -> None:
    for response_text in ["I don't know", "fifty percent", "1.5", "-0.1", ""]:
        prob = parse_spam_probability(response_text)
        assert prob is None


def test_build_spam_check_prompt_structure() -> None:
    """Test that the spam check prompt has expected instructions and email format."""
    email_body = "Test content for spam detection."
    prompt = build_spam_check_prompt(email_body)
    assert "You are an email spam detection expert." in prompt
    assert (
        "Given the following email, estimate the probability that it is spam."
        in prompt
    )
    assert "Email:" in prompt
    assert "Test content for spam detection." in prompt


def test_parse_spam_probability_boundary_cases() -> None:
    """Test parse_spam_probability with exact boundary values."""
    assert parse_spam_probability("0") == 0.0
    assert parse_spam_probability("1") == 1.0


def test_parse_spam_probability_non_numeric() -> None:
    """Test parse_spam_probability with completely non-numeric input."""
    prob = parse_spam_probability("hello world")
    assert prob is None


def test_parse_spam_probability_partial_text() -> None:
    """Test parse_spam_probability where number appears inside text."""
    prob = parse_spam_probability("The probability is 0.3 according to analysis")
    assert prob is None  # Should be None because parse expects pure number only
