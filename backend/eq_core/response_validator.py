"""
Validation Engine — Ensures user responses are high quality before sending to NLP models.
"""
from .definitions import (
    MIN_RESPONSE_LENGTH,
    MAX_RESPONSE_LENGTH,
    MIN_WORD_COUNT,
    SPAM_PATTERNS,
)


def validate_response(text: str) -> tuple[bool, str]:
    """
    Validates a user's text response.
    Returns: (is_valid: bool, validation_message: str)
    """
    if not text or not text.strip():
        return False, "Response cannot be empty."

    text = text.strip()
    
    # 1. Length checks
    if len(text) < MIN_RESPONSE_LENGTH:
        return False, f"Response is too short. Please provide at least {MIN_RESPONSE_LENGTH} characters to allow for accurate emotional analysis."
        
    if len(text) > MAX_RESPONSE_LENGTH:
        return False, f"Response is too long. Please keep it under {MAX_RESPONSE_LENGTH} characters."

    # 2. Word count check
    words = text.split()
    if len(words) < MIN_WORD_COUNT:
        return False, f"Please write at least {MIN_WORD_COUNT} words to properly explain your thought process."

    # 3. Spam / Gibberish detection
    text_lower = text.lower()
    
    # Check exact match against spam patterns (e.g. "idk", "n/a")
    if text_lower in SPAM_PATTERNS:
        return False, "This response appears to be a placeholder or unhelpful. Please provide a genuine answer."
        
    # Check for repeating characters (e.g. "aaaaa")
    if len(set(text_lower.replace(" ", ""))) < 3 and len(text) > 10:
        return False, "Response contains excessive repeating characters. Please provide a meaningful answer."

    # 4. Basic coherence (check if it's just numbers)
    if text.replace(" ", "").isdigit():
        return False, "Response cannot be entirely numeric. Please explain using words."

    # Passed all checks
    return True, ""
