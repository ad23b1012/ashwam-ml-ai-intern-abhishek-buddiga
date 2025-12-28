# stability/metrics.py
# Computes run-to-run stability metrics for aligned clusters

from typing import Dict, List


def compute_agreement_rate(
    clusters: List[Dict[str, dict]],
    total_runs: int
) -> float:
    """
    Agreement rate:
    Fraction of clusters that appear in all runs.
    """
    if not clusters:
        return 0.0

    stable = 0
    for cluster in clusters:
        if len(cluster) == total_runs:
            stable += 1

    return round(stable / len(clusters), 4)


def compute_polarity_flip_rate(
    clusters: List[Dict[str, dict]]
) -> float:
    """
    Polarity flip rate:
    Fraction of clusters where polarity differs across runs.
    """
    if not clusters:
        return 0.0

    flips = 0
    evaluated = 0

    for cluster in clusters:
        polarities = set()
        for item in cluster.values():
            polarity = item.get("polarity")
            if polarity is not None:
                polarities.add(polarity)

        if len(polarities) > 1:
            flips += 1

        if len(polarities) > 0:
            evaluated += 1

    if evaluated == 0:
        return 0.0

    return round(flips / evaluated, 4)


def compute_bucket_drift_rate(
    clusters: List[Dict[str, dict]]
) -> float:
    """
    Bucket drift rate:
    Fraction of clusters with disagreement in intensity/arousal/time buckets.
    """
    if not clusters:
        return 0.0

    drift = 0
    evaluated = 0

    for cluster in clusters:
        intensity = set()
        arousal = set()
        time = set()

        for item in cluster.values():
            if item.get("domain") == "emotion":
                arousal.add(item.get("arousal_bucket"))
            else:
                intensity.add(item.get("intensity_bucket"))

            time.add(item.get("time_bucket"))

        has_drift = False

        if len(intensity) > 1:
            has_drift = True
        if len(arousal) > 1:
            has_drift = True
        if len(time) > 1:
            has_drift = True

        if has_drift:
            drift += 1

        if len(cluster) > 0:
            evaluated += 1

    if evaluated == 0:
        return 0.0

    return round(drift / evaluated, 4)
