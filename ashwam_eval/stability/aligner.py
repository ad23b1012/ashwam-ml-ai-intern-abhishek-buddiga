# stability/aligner.py
# Aligns semantic objects across multiple LLM runs using evidence overlap

from typing import Dict, List
from ashwam_eval.matcher import spans_overlap


def align_runs(
    runs: Dict[str, List[dict]]
) -> List[Dict[str, dict]]:
    """
    Align objects across multiple runs for a single journal.

    Args:
        runs:
            A dictionary mapping run_id -> list of extracted items
            Example:
            {
                "run1": [item1, item2, ...],
                "run2": [itemA, itemB, ...],
                "run3": [...]
            }

    Returns:
        A list of clusters.
        Each cluster is a dict mapping run_id -> item (or missing if not present).

        Example:
        [
            {
                "run1": {...},
                "run2": {...},
                "run3": {...}
            },
            {
                "run1": {...},
                "run2": {...}
            }
        ]
    """

    clusters: List[Dict[str, dict]] = []

    for run_id, items in runs.items():
        for item in items:
            matched_cluster = None

            for cluster in clusters:
                for existing_item in cluster.values():
                    if existing_item.get("domain") != item.get("domain"):
                        continue

                    span_a = existing_item.get("evidence_span")
                    span_b = item.get("evidence_span")

                    if spans_overlap(span_a, span_b):
                        matched_cluster = cluster
                        break

                if matched_cluster is not None:
                    break

            if matched_cluster is not None:
                matched_cluster[run_id] = item
            else:
                clusters.append({run_id: item})

    return clusters
