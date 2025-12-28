# stability/aggregator.py
# Produces a single stable output from multiple runs using majority vote + abstention

from typing import Dict, List
from collections import Counter


def majority_vote(values: List[str]) -> str:
    """
    Return the majority value if it exists, otherwise 'uncertain'.
    """
    if not values:
        return "uncertain"

    counts = Counter(values)
    most_common, freq = counts.most_common(1)[0]

    if freq > len(values) / 2:
        return most_common

    return "uncertain"


def aggregate_cluster(
    cluster: Dict[str, dict]
) -> dict:
    """
    Aggregate a single aligned cluster into a stable object.
    """

    items = list(cluster.values())
    base = items[0].copy()

    polarities = [item.get("polarity") for item in items if item.get("polarity") is not None]
    base["polarity"] = majority_vote(polarities)

    if base.get("domain") == "emotion":
        arousal = [item.get("arousal_bucket") for item in items if item.get("arousal_bucket") is not None]
        base["arousal_bucket"] = majority_vote(arousal)
    else:
        intensity = [item.get("intensity_bucket") for item in items if item.get("intensity_bucket") is not None]
        base["intensity_bucket"] = majority_vote(intensity)

    time_buckets = [item.get("time_bucket") for item in items if item.get("time_bucket") is not None]
    base["time_bucket"] = majority_vote(time_buckets)

    return base


def aggregate_clusters(
    clusters: List[Dict[str, dict]]
) -> List[dict]:
    """
    Aggregate all clusters into stable semantic objects.
    """
    stable_items = []
    for cluster in clusters:
        stable_items.append(aggregate_cluster(cluster))
    return stable_items
