# cli.py
# CLI entrypoint for Exercise B: Run-to-Run Stability Analysis

import argparse
import json
import os
from collections import defaultdict

from ashwam_eval.stability.aligner import align_runs
from ashwam_eval.stability.metrics import (
    compute_agreement_rate,
    compute_polarity_flip_rate,
    compute_bucket_drift_rate,
)
from ashwam_eval.stability.aggregator import aggregate_clusters


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_journals(path):
    journals = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            journals[obj["journal_id"]] = obj
    return journals


def main():
    parser = argparse.ArgumentParser(description="Ashwam Exercise B — Stability Analysis")
    parser.add_argument("--data", required=True, help="Path to data directory")
    parser.add_argument("--out", required=True, help="Path to output directory")
    args = parser.parse_args()

    data_dir = args.data
    out_dir = args.out
    os.makedirs(out_dir, exist_ok=True)

    journals = load_journals(os.path.join(data_dir, "journals.jsonl"))

    runs_dir = os.path.join(data_dir, "llm_runs")

    runs_by_journal = defaultdict(dict)

    for fname in os.listdir(runs_dir):
        if not fname.endswith(".json"):
            continue

        parts = fname.split(".")
        journal_id = parts[0]
        run_id = parts[1]

        path = os.path.join(runs_dir, fname)
        data = load_json(path)

        runs_by_journal[journal_id][run_id] = data["items"]

    per_journal_results = []
    global_clusters = 0
    global_stable_clusters = 0
    global_polarity_flips = 0
    global_bucket_drifts = 0

    for journal_id, runs in runs_by_journal.items():
        clusters = align_runs(runs)

        total_runs = len(runs)

        agreement = compute_agreement_rate(clusters, total_runs)
        polarity_flip = compute_polarity_flip_rate(clusters)
        bucket_drift = compute_bucket_drift_rate(clusters)

        stable_count = sum(1 for c in clusters if len(c) == total_runs)

        global_clusters += len(clusters)
        global_stable_clusters += stable_count
        global_polarity_flips += int(polarity_flip * len(clusters))
        global_bucket_drifts += int(bucket_drift * len(clusters))

        per_journal_results.append({
            "journal_id": journal_id,
            "agreement_rate": agreement,
            "polarity_flip_rate": polarity_flip,
            "bucket_drift_rate": bucket_drift,
            "total_clusters": len(clusters),
            "stable_clusters": stable_count,
        })

        stable_items = aggregate_clusters(clusters)
        with open(
            os.path.join(out_dir, "stable_outputs.jsonl"),
            "a",
            encoding="utf-8"
        ) as f:
            f.write(json.dumps({
                "journal_id": journal_id,
                "items": stable_items
            }) + "\n")

    stability_summary = {
        "total_clusters": global_clusters,
        "stable_clusters": global_stable_clusters,
        "overall_agreement_rate": round(
            global_stable_clusters / global_clusters, 4
        ) if global_clusters > 0 else 0.0,
        "polarity_flip_events": global_polarity_flips,
        "bucket_drift_events": global_bucket_drifts,
    }

    with open(os.path.join(out_dir, "stability_summary.json"), "w", encoding="utf-8") as f:
        json.dump(stability_summary, f, indent=2)

    with open(os.path.join(out_dir, "per_journal_stability.jsonl"), "w", encoding="utf-8") as f:
        for row in per_journal_results:
            f.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    main()
