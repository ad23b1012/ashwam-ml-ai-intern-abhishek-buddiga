# Ashwam Exercise B — Run-to-Run Variance & Stability Analysis

## Overview

Large Language Model (LLM) outputs are inherently non-deterministic. Even with identical prompts and inputs, repeated runs may differ in phrasing, structure, or extracted attributes.

This exercise focuses on **measuring and reasoning about stability**, not correctness. There is **no gold reference**. Instead, consistency across multiple runs is used as a proxy for system reliability and safety.

The goal is to design a **deterministic stability evaluation framework** that quantifies run-to-run variance **without relying on canonical labels**, using **evidence spans** as the primary anchor.

---

## Key Principles

- No canonical vocabularies or label normalization  
- Evidence spans are the primary anchor for alignment  
- Stability is evaluated structurally, not textually  
- Deterministic evaluation despite non-deterministic generation  
- Safety-first framing, especially for polarity and negation  

---

## Data Description

The following inputs are provided:

- `data/journals.jsonl`  
  Five synthetic Ashwam journal entries.

- `data/llm_runs/`  
  For each journal, three LLM outputs generated from the same prompt, intentionally containing:
  - paraphrased evidence spans
  - missing objects in some runs
  - bucket drift (intensity / arousal / time)
  - a deliberate polarity flip on a negated emotion case (to test risk metrics)

There is **no gold annotation** in this exercise.

---

## Defining Stability

Two extracted objects from different runs are considered the **same semantic object** if:

1. They belong to the same domain (`symptom | food | emotion | mind`)  
2. Their `evidence_span` overlaps at the character level  

Textual paraphrases are allowed.  
Canonical labels and semantic similarity are not required.

This definition mirrors the evidence-grounded matching logic from Exercise A.

---

## Field Stability Expectations

### High-Risk Fields (Must Be Stable)

- Object presence / absence  
- `polarity` (`present ↔ absent ↔ uncertain`)

Polarity flips are treated as **critical safety failures**, especially for negated emotions or symptoms.

---

### Medium-Risk Fields (Limited Drift Allowed)

- `intensity_bucket`  
- `arousal_bucket`  
- `time_bucket`  

Minor drift is expected, but sustained disagreement indicates instability.

---

### Low-Risk Fields (Free Drift Allowed)

- Free-text descriptions  
- Ordering of extracted objects  
- Confidence scores (if present)

These do not affect system safety.

---

## Matching Algorithm

Objects are aligned across runs using a deterministic process:

- Primary signal: **evidence span overlap**  
- Secondary condition: **domain equality**

This alignment logic reuses the evidence-grounded matcher from Exercise A, ensuring consistency across evaluations.

Optional semantic similarity fallbacks may be added, but are not required.

---

## Stability Metrics

The system computes the following quantitative metrics:

### Agreement Rate

Measures how consistently objects appear across runs.

Defined as:

- intersection of matched objects across runs|

- union of all objects across runs

- High agreement indicates stable extraction behavior.

---

### Polarity Flip Rate (High-Risk Metric)

Measures how often polarity differs for matched objects across runs.

Even a small number of polarity flips is considered dangerous in a women’s health context.

---

### Bucket Drift Rate

Measures disagreement in intensity, arousal, or time buckets for matched objects.

Some drift is acceptable; frequent drift indicates model instability.

---

## Risk Framing

### Acceptable Variance

- Minor bucket changes  
- Occasional missing low-salience objects  
- Paraphrased evidence spans with correct grounding  

### Dangerous Variance

- Polarity flips  
- Negated emotions becoming present  
- Symptoms appearing in one run and disappearing in another  
- Inconsistent evidence grounding  

These failures directly impact user trust, safety, and auditability.

---

## Production Implications

Run-to-run instability affects:

- **Downstream nudges**  
  Conflicting recommendations confuse users.

- **User trust**  
  Inconsistent interpretations undermine credibility.

- **Auditability**  
  Systems must explain why outputs changed across identical inputs.

Stability analysis is therefore essential before deploying LLM-based health systems.

---

## Bonus: Stable Final Output (Optional)

As an optional extension, a single stable output can be produced from multiple runs:

- Majority vote for stable fields  
- Abstention or uncertainty marking on disagreements  
- Polarity disagreements always result in abstention  

This mirrors safe ensemble design in production systems.

---

## Outputs

The pipeline produces:

- `out/stability_summary.json`  
  Aggregate stability metrics across all journals.

- `out/per_journal_stability.jsonl`  
  Journal-level stability diagnostics.

- `out/stable_outputs.jsonl` (optional)  
  Consolidated stable outputs derived from multiple runs.

---

## What This Exercise Demonstrates

- Systems thinking under non-determinism  
- Safety-aware evaluation design  
- Practical ML judgment beyond accuracy  
- Clear separation between generation and evaluation  

---
