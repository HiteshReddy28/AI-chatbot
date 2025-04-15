import re

class ValidationError(Exception):
    """Custom exception raised when validation fails."""
    pass

def validate_not_empty(text, metadata=None):
    if not text or not text.strip():
        raise ValidationError("Input/output is empty.")

def validate_no_pii(text, metadata=None):
    # to detect an email address
    if re.search(r'\S+@\S+\.\S+', text):
        raise ValidationError("Input contains an email address, which might be sensitive.")
    # to detect a phone number
    if re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text):
        raise ValidationError("Input contains a phone number, which might be sensitive.")

def validate_not_gibberish(text, metadata=None):
    # gibberish check: ensure text is long enough and contains vowels.
    vowels = set("aeiouAEIOU")
    if len(text.strip()) < 5 or not any(char in vowels for char in text):
        raise ValidationError("Input appears to be gibberish.")



def validate_no_toxic_language(text, metadata=None):
    # for  toxic words
    toxic_words = ["damn", "shit", "fuck", "bitch"]
    for word in toxic_words:
        if word in text.lower():
            raise ValidationError("Output contains toxic language.")

def validate_responsiveness(text, metadata=None):
    # If metadata includes a query, check that at least one word from the query appears in the response
    if metadata and "query" in metadata:
        query_words = set(metadata["query"].lower().split())
        response_words = set(text.lower().split())
        if not query_words.intersection(response_words):
            raise ValidationError("The response does not address the query.")

def validate_single_plan(text, metadata=None):
    # Check that only one negotiation plan is mentioned.
    plan_keywords = [
        "Refinance Step Down", 
        "Refinance Step Up", 
        "Refinance Step Same", 
        "Extended Payment Plan", 
        "Settlement Plan"
    ]
    count = 0
    for kw in plan_keywords:
        if kw.lower() in text.lower():
            count += 1
    if count > 1:
        raise ValidationError("Multiple plans are mentioned in the output; only one plan should be offered.")

def validate_strict_greeting_first_response(text, metadata=None):
    # If metadata indicates this is the first response, enforce the exact greeting.
    if metadata and metadata.get("is_first_response", False):
        expected = "Hello, how may I assist you today?"
        if text.strip() != expected:
            raise ValidationError("The first response must be exactly: 'Hello, how may I assist you today?'")


# Define lists of validators for input and output.
INPUT_VALIDATORS = [
    validate_not_empty,
    validate_no_pii,
    validate_not_gibberish
]

OUTPUT_VALIDATORS = [
    validate_not_empty,
    validate_no_toxic_language,
    validate_responsiveness,
    validate_single_plan,
    validate_strict_greeting_first_response
]

def validate_input(text, metadata=None):
    """
    Runs all input validators.
    Raises ValidationError if any check fails.
    """
    for validator in INPUT_VALIDATORS:
        validator(text, metadata)
    return text

def validate_output(text, metadata=None):
    """
    Runs all output validators.
    If metadata is provided (e.g., indicating the query or first response), uses it.
    Raises ValidationError if any check fails.
    """
    for validator in OUTPUT_VALIDATORS:
        validator(text, metadata)
    return text
