# Training Log

## Overview

### All Runs

| Run | Experiment | Dataset | Init Weights | Status | <METRIC_1> | <METRIC_2> |
|-----|-----------|---------|-------------|--------|:----------:|:----------:|
| 1 | `<experiment_name>` | `<dataset>` | `<pretrained>.pt` (fresh) | Planned | — | — |

<!-- Keep this table updated. One row per run. Status: Planned, Training (<VM>), Complete, Interrupted, Failed. -->

### Checkpoint Lineage

- **Run 1:** Starting from pretrained weights `<pretrained>.pt`.
- *(Update this section as runs build on each other's checkpoints)*

---

## Planned: Run 1

- **Goal:** <what this run aims to test or establish — e.g., baseline performance>
- **Configs:**
  - Data: `configs/data/<dataset>.yaml`
  - Feature: `configs/feature/<method>.yaml`
  - Train: `configs/train/<experiment>.yaml`
- **Changes from previous:** N/A (first run)
- **Hypothesis:** <what you expect to see and why>

---

<!-- Template for completed runs:

## Run <N> — <YYYY-MM-DD>

- **Experiment:** `<experiment_name>`
- **Config:** `configs/train/<experiment>.yaml`
- **Model:** <architecture name>
- **Init weights:** `<path to checkpoint this run started from>`
- **Dataset:** <dataset name>
- **Epochs:** <total> (best: <best_epoch>). <Early-stopped / Interrupted / Ran to completion>.
- **Batch size:** <N>
- **Optimizer:** <name> (lr=<value>)
- **Key metrics (best epoch):**
  - <Metric 1>: <value>
  - <Metric 2>: <value>
- **Duration:** <time>
- **Checkpoint:** `checkpoints/<run_id>/`
- **VM:** `<vm_name>` (<GPU count>x <GPU type>)
- **Notes:** <observations, what worked, what to try next>

-->

<!-- Template for continuation runs:

## Run <N> — <YYYY-MM-DD> — <Status> (<VM>)

- **Experiment:** `<experiment>_cont`
- **Config:** `configs/train/<experiment>_cont.yaml`
- **Model:** <architecture name> (from Run <N-1> best checkpoint)
- **Init weights:** `checkpoints/<prev_run_id>/weights/best.pt`
- **Dataset:** <dataset name>
- **Epochs:** <total> (patience <N>)
- **Batch size:** <N>
- **Optimizer:** <new_optimizer> (lr=<value>) — changed from <old_optimizer>
- **Rationale:** <why continuing — e.g., model still improving, trying different optimizer>
- **Key metrics (best epoch):**
  - <Metric 1>: <value>
  - <Metric 2>: <value>
- **Improvement over Run <N-1>:** <metric> <old> → <new> (+<delta>)
- **VM:** `<vm_name>` (<GPU count>x <GPU type>, auto-shutdown)
- **Checkpoint:** `checkpoints/<run_id>/`

-->

<!-- Template for planned runs:

## Planned: Run <N+1>

- **Goal:** <what this run aims to test/improve>
- **Configs:**
  - Data: `configs/data/<dataset>.yaml`
  - Feature: `configs/feature/<method>.yaml`
  - Train: `configs/train/<experiment>.yaml`
- **Changes from previous:** <what is different and why>
- **Hypothesis:** <what you expect to see>

-->
