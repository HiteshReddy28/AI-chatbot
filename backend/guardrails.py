import re

# Basic profanity filter
PROFANITY_BLACKLIST = {"damn", "hell", "shit", "dumb", "idiot"}

# Suspicious prompt injection or manipulation keywords
INJECTION_PATTERNS = [
    r"(ignore\s+the\s+previous\s+message)",
    r"(override\s+instructions)",
    r"(jailbreak)",
    r"(reset\s+prompt)",
    r"(you\s+are\s+now\s+a\s+helpful\s+assistant)",
    r"(delete\s+all\s+rules)",
    r"(token\s+limit|greedy\s+factor)",
    r"(system:\s*)",
    r"(stop\s+being\s+a\s+bot)",
    r"(repeat\s+this\s+message)",
    r"(offer\s+me\s+plan\s+[a-z])",
]

BLOCKED_OUTPUT_PATTERNS = [
    r"greedy\s*factor",
    r"token\s*limit",
    r"as an ai",
    r"you are now",
    r"i have been instructed",
    r"previous prompt was",
    r"system message",
    r"temperature\s*setting",
    r"response format is",
    r"my prompt is",
    r"\{.*?\}",  # block raw JSON output
    r"<function>",  # invalid output leaking function names
]

# Invalid plans that shouldn't exist
DISALLOWED_PLAN_TERMS = [
    "plan b", "golden plan", "universal forgiveness", "plan override", "free plan",
]

# Profanity and toxic tone blacklist
TOXIC_PHRASES = {"damn", "shit", "hell", "dumb", "idiot"}

# Prompt flooding threshold
MAX_INPUT_LENGTH = 800

#Input filtering
def enforce_input_guardrails(user_input: str) -> bool:

    user_input = user_input.strip().lower()

    # Block empty or excessively long messages 
    if not user_input or len(user_input) > MAX_INPUT_LENGTH:
        return False

    # Block repeated phrases (prompt flooding)
    words = user_input.split()
    word_counts = {word: words.count(word) for word in set(words)}
    if any(count > 10 for count in word_counts.values()):
        return False

    # Block suspicious prompt injection patterns
    if any(re.search(pattern, user_input) for pattern in INJECTION_PATTERNS):
        return False

    # Block profanity
    if any(word in user_input.split() for word in PROFANITY_BLACKLIST):
        return False

    # Block code-like syntax
    if re.search(r"[<>{};]", user_input):
        return False

    return True

#Output filtering
def enforce_output_guardrails(ai_output: str) -> bool:
    text = ai_output.lower()

    # Basic sanity check
    if not text or len(text) < 10:
        return False

    # Block any disallowed plan references
    if any(plan in text for plan in DISALLOWED_PLAN_TERMS):
        return False

    # Block internal or meta-response patterns
    if any(re.search(p, text) for p in BLOCKED_OUTPUT_PATTERNS):
        return False

    # Block profanity or repeated aggression
    if any(word in text.split() for word in TOXIC_PHRASES):
        return False

    # Block model "role redefining" outputs
    if "you are now a helpful assistant" in text:
        return False

    return True
