# <PROJECT_NAME>

<One-line description of what this project trains.>

## Environment

| | Path |
|---|---|
| **Local** | `<LOCAL_PATH>` |
| **Remote VM** | `<VM_NAME>.<ZONE>.<GCP_PROJECT>:~/<PROJECT_NAME>` |
| **Sync (code)** | Mutagen two-way (`<PROJECT_NAME>` session) |
| **Sync (outputs)** | Mutagen one-way remote→local (`<PROJECT_NAME>-output` session) |

## Quick Start

### Set up the environment

The project is uv-managed; `uv sync` creates `.venv/` from `uv.lock` with the interpreter pinned by `.python-version`.

```bash
# Install uv once (skip if already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# From the project root
uv sync
uv run pytest
```

### SSH into VM

```bash
gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT>
cd ~/<PROJECT_NAME>
uv sync   # first time on the VM
```

### Train

```bash
# Smoke test (1 epoch, verify pipeline works)
uv run python -m <PACKAGE_NAME>.training.train --config configs/train/smoke_test.yaml

# Full training run
uv run python -m <PACKAGE_NAME>.training.train --config configs/train/<EXPERIMENT>.yaml

# Continue from a previous run's checkpoint (different optimizer/LR)
uv run python -m <PACKAGE_NAME>.training.train --config configs/train/<EXPERIMENT>_cont.yaml

# Resume from last checkpoint (same config, pick up where it left off)
uv run python -m <PACKAGE_NAME>.training.train --config configs/train/<EXPERIMENT>.yaml --resume
```

### Evaluate

```bash
# Single dataset
uv run python -m <PACKAGE_NAME>.training.evaluate \
    --config configs/train/<EXPERIMENT>.yaml \
    --checkpoint checkpoints/<RUN_ID>/weights/best.pt

# Cross-dataset evaluation
uv run python -m <PACKAGE_NAME>.training.evaluate_all \
    --checkpoint checkpoints/<RUN_ID>/weights/best.pt \
    --datasets <dataset1> <dataset2> \
    --batch 64
```

### Plot Metrics

```bash
# Single run
uv run python -m <PACKAGE_NAME>.training.plot_metrics --run_dir checkpoints/<RUN_ID>

# Compare multiple runs
uv run python -m <PACKAGE_NAME>.training.plot_metrics --compare checkpoints/run_001 checkpoints/run_002
```

### Visualize Predictions

```bash
uv run python -m <PACKAGE_NAME>.training.visualize \
    --config configs/train/<EXPERIMENT>.yaml \
    --checkpoint checkpoints/<RUN_ID>/weights/best.pt \
    --num_samples 16
```

### Check Convergence

```bash
# Returns exit code 0 if converged, 1 if still improving
uv run python -m <PACKAGE_NAME>.training.check_convergence checkpoints/<RUN_ID>
```

## Configuration

4-tier YAML config system (merged in order, later tiers override earlier):

1. `configs/default.yaml` — base defaults (model architecture, augmentation, visualization)
2. `configs/data/<dataset>.yaml` — input dataset paths and properties
3. `configs/feature/<method>.yaml` — feature engineering pipeline
4. `configs/train/<experiment>.yaml` — model + training hyperparameters (references data + feature configs)

### Adding a New Experiment

1. (If needed) Create `configs/data/<your_dataset>.yaml` from `configs/data/_example.yaml`
2. (If needed) Create `configs/feature/<your_method>.yaml` from `configs/feature/_example.yaml`
3. Create `configs/train/<your_experiment>.yaml` from `configs/train/_example.yaml`
   - Set `data_config: <your_dataset>` and `feature_config: <your_method>`
   - Set a unique `run_id` — this becomes the folder name under `checkpoints/`
4. Add a "Planned" entry in `TRAINLOG.md` describing what you intend to test
5. Run training — results are auto-logged

### Continuing a Run

When a run is interrupted or you want to try different optimizer/LR from a checkpoint:

1. Create `configs/train/<experiment>_cont.yaml` with:
   - `checkpoint_path` pointing to the previous run's `best.pt`
   - New optimizer, LR, or epoch count as needed
2. Run training with the new config

## Documentation Guide

| File | What It Tracks | When to Update |
|------|----------------|----------------|
| `README.md` | This file — project overview and usage | When setup or commands change |
| `.agent/dev/SKILL.md` | Full project guide — config system, workflow, cloud, checklists | When conventions or infra changes |
| `PROJECT_STRUCTURE.md` | Directory tree and file descriptions | When files/folders are added or removed |
| `ASSETS.md` | Datasets, model backbones, checkpoints, outputs | When new data or models are added |
| `CHANGELOG.md` | Code changes by date | After every code change |
| `TRAINLOG.md` | Training runs — planned + completed with config links | Before and after every training run |
| `IO.md` | Input/output formats with actual data examples | When data pipeline changes |

## Environment

`pyproject.toml` is the single source of truth for dependencies; `uv.lock` pins exact versions; `.python-version` pins the interpreter.

```bash
uv sync                              # create .venv/ from uv.lock
uv add <package>                     # add a runtime dep
uv add --group dev <package>         # add a dev-only dep
uv lock --upgrade-package <package>  # bump one package
uv run pytest                        # run tests in the project env
```

Python range: `>=3.10,<3.13`. Do not use `pip` or `requirements.txt` — they bypass the lockfile and cause drift between local and VM.

## Model

- **Architecture:** `<MODEL_ARCHITECTURE>`
- **Input:** `<INPUT_DESCRIPTION>`
- **Output:** `<OUTPUT_DESCRIPTION>`
- **Pretrained weights:** `<WEIGHTS_SOURCE>`
- **Target deployment:** `<DEPLOYMENT_TARGET>`
