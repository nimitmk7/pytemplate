#!/bin/bash
# Script to create a test repository for E2E testing with coverage scenarios
# Run this once to create the test repository structure

REPO_DIR="tests/e2e/test_repo/"

# Clean up if exists
rm -rf "$REPO_DIR"
mkdir -p "$REPO_DIR"
cd "$REPO_DIR"

# Initialize git repo
git init
git config user.name "Test User"
git config user.email "test@example.com"

# --- Main branch: initial code and partial tests (coverage < 100%) ---
mkdir -p myproject
echo "# Test Project" > README.md

# Create module with core palindrome functions
cat > myproject/palindrome.py << 'EOF'
"""Palindrome utility functions."""

def is_palindrome(text):
    """Check if a text is a palindrome."""
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]

def reverse_string(text):
    """Reverse a string."""
    return text[::-1]

def get_longest_palindrome(text):
    """Get the longest palindromic substring."""
    if not text:
        return ""
    longest = ""
    for i in range(len(text)):
        for j in range(i + 1, len(text) + 1):
            substring = text[i:j]
            if is_palindrome(substring) and len(substring) > len(longest):
                longest = substring
    return longest
EOF

# Create tests directory with initial tests for only first two functions
mkdir -p tests
cat > tests/test_palindrome.py << 'EOF'
"""Tests for palindrome module."""
from myproject.palindrome import is_palindrome, reverse_string

def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False

def test_reverse_string():
    assert reverse_string("abc") == "cba"
    assert reverse_string("") == ""
EOF

# Create pyproject.toml for pytest configuration
cat > pyproject.toml << 'EOF'
[project]
name = "myproject"
version = "0.1.0"

[tool.pytest.ini_options]
pythonpath = ["."]
EOF

# Initial commit on main branch
git add .
git commit -m "Initial commit: palindrome functions with partial tests"
git branch -M main
MAIN_SHA=$(git rev-parse HEAD)

echo "Main branch created: coverage < 100% (only core tests)"

# --- Feature branch: add validators (coverage decreases further) ---
git checkout -b feature/add-validators main

cat >> myproject/palindrome.py << 'EOF'

def is_valid_palindrome(text):
    """Check if text is a valid palindrome (alphanumeric only)."""
    import re
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    return cleaned == cleaned[::-1]

def find_all_palindromes(text, min_length=3):
    """Find all palindromic substrings of minimum length."""
    palindromes = set()
    for i in range(len(text)):
        for j in range(i + min_length, len(text) + 1):
            substring = text[i:j]
            if is_palindrome(substring):
                palindromes.add(substring)
    return sorted(palindromes)

def has_palindrome_pattern(text):
    """Check if text contains any palindrome of length 3 or more."""
    return len(find_all_palindromes(text, min_length=3)) > 0
EOF

# Add partial tests for new validators only
git checkout tests/test_palindrome.py
cat >> tests/test_palindrome.py << 'EOF'

from myproject.palindrome import is_valid_palindrome

def test_is_valid_palindrome():
    assert is_valid_palindrome("A1B2B1A") is True
    assert is_valid_palindrome("Race a car!") is False
EOF

git add myproject/palindrome.py tests/test_palindrome.py
git commit -m "Add validator functions with partial tests"
FEATURE_SHA=$(git rev-parse HEAD)

echo "Feature add-validators branch created: coverage drops further"

# --- Feature branch: add comprehensive tests (coverage restored to 100%) ---
# Branch off feature/add-validators
git checkout -b feature/improve-tests feature/add-validators

# Overwrite tests to cover all functions
cat > tests/test_palindrome.py << 'EOF'
"""Comprehensive tests for palindrome module including validators."""
from myproject.palindrome import (
    is_palindrome,
    reverse_string,
    get_longest_palindrome,
    is_valid_palindrome,
    find_all_palindromes,
    has_palindrome_pattern,
)

def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("") is True

def test_reverse_string():
    assert reverse_string("abc") == "cba"
    assert reverse_string("") == ""

def test_get_longest_palindrome():
    assert get_longest_palindrome("babad") in {"bab", "aba"}
    assert get_longest_palindrome("") == ""

def test_is_valid_palindrome():
    assert is_valid_palindrome("A1B2B1A") is True
    assert is_valid_palindrome("Race a car!") is False

def test_find_all_palindromes():
    pals = find_all_palindromes("ababa")
    assert "aba" in pals and "bab" in pals

def test_has_palindrome_pattern():
    assert has_palindrome_pattern("xyzaba") is True
    assert has_palindrome_pattern("xyz") is False
EOF

git add tests/test_palindrome.py
git commit -m "Add comprehensive tests for all palindrome functions"
IMPROVE_SHA=$(git rev-parse HEAD)

echo "Feature improve-tests branch created: coverage restored to 100%"

# Record metadata
cat > .test_metadata.json << EOF
{
    "main_sha": "${MAIN_SHA}",
    "feature_sha": "${FEATURE_SHA}",
    "improve_sha": "${IMPROVE_SHA}"
}
EOF

echo "Test repository created successfully at $REPO_DIR"
