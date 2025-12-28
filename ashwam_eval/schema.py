# schema.py
# Defines allowed values and validation logic for extracted semantic objects

ALLOWED_DOMAINS = {"symptom", "food", "emotion", "mind"}
ALLOWED_POLARITY = {"present", "absent", "uncertain"}
ALLOWED_BUCKETS = {"low", "medium", "high", "unknown"}
ALLOWED_TIME_BUCKETS = {"today", "last_night", "past_week", "unknown"}


def is_valid_evidence_span(evidence_span: str, journal_text: str) -> bool:
    """
    Check whether the evidence span appears verbatim in the journal text.
    """
    if not isinstance(evidence_span, str):
        return False
    return evidence_span in journal_text


def validate_item(item: dict, journal_text: str) -> bool:
    """
    Validate a single extracted item against the schema rules.
    Returns True if valid, False otherwise.
    """

    if not isinstance(item, dict):
        return False

    domain = item.get("domain")
    polarity = item.get("polarity")
    evidence_span = item.get("evidence_span")
    time_bucket = item.get("time_bucket")

    if domain not in ALLOWED_DOMAINS:
        return False

    if polarity not in ALLOWED_POLARITY:
        return False

    if time_bucket not in ALLOWED_TIME_BUCKETS:
        return False

    if not is_valid_evidence_span(evidence_span, journal_text):
        return False

    if domain == "emotion":
        arousal_bucket = item.get("arousal_bucket")
        if arousal_bucket not in ALLOWED_BUCKETS:
            return False
    else:
        intensity_bucket = item.get("intensity_bucket")
        if intensity_bucket not in ALLOWED_BUCKETS:
            return False

    return True


def validate_items(items: list, journal_text: str) -> list:
    """
    Validate a list of extracted items.
    Returns only the valid items.
    """
    valid_items = []
    for item in items:
        if validate_item(item, journal_text):
            valid_items.append(item)
    return valid_items
