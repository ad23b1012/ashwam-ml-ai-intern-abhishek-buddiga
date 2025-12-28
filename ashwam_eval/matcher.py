# matcher.py
# Implements evidence-grounded matching between predicted and gold items

from typing import List, Tuple


def spans_overlap(span_a: str, span_b: str) -> bool:
    """
    Returns True if two evidence spans overlap at the character level.
    Overlap is defined as one span being a substring of the other.
    """
    if not isinstance(span_a, str) or not isinstance(span_b, str):
        return False
    return span_a in span_b or span_b in span_a


def match_items(
    gold_items: List[dict],
    pred_items: List[dict]
) -> Tuple[List[Tuple[dict, dict]], List[dict], List[dict]]:
    """
    Match predicted items to gold items using domain + evidence span overlap.

    Returns:
    - matched_pairs: list of (gold_item, pred_item)
    - false_negatives: gold items with no matching prediction
    - false_positives: predicted items with no matching gold
    """

    matched_pairs = []
    used_gold = set()
    used_pred = set()

    for gi, gold in enumerate(gold_items):
        best_match_index = None

        for pi, pred in enumerate(pred_items):
            if pi in used_pred:
                continue

            if gold.get("domain") != pred.get("domain"):
                continue

            gold_span = gold.get("evidence_span")
            pred_span = pred.get("evidence_span")

            if spans_overlap(gold_span, pred_span):
                best_match_index = pi
                break

        if best_match_index is not None:
            matched_pairs.append((gold, pred_items[best_match_index]))
            used_gold.add(gi)
            used_pred.add(best_match_index)

    false_negatives = [
        gold_items[i] for i in range(len(gold_items)) if i not in used_gold
    ]

    false_positives = [
        pred_items[i] for i in range(len(pred_items)) if i not in used_pred
    ]

    return matched_pairs, false_negatives, false_positives
