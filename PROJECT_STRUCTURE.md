# Project Structure

General-purpose ML system template. A human sets the task; the scaffold covers the six canonical stages end-to-end:

**data → features → modeling → training → evaluation → visualization**

Each stage lives under `PACKAGE_NAME/`. Some modules ship as *building blocks* (ready to import), others as *scaffolds* (stubs you fill in per project). Preprocessing and postprocessing are deliberately pluggable — one concrete codec is provided as an example of the axis, not as the answer. The whole project is **uv-managed** and **pytest-covered**.

## Layout

```
<PROJECT_NAME>/
├── .agent/dev/SKILL.md                 # docs — full project guide (conventions, cloud, checklists)
├── .python-version                     # tooling — pinned Python (uv reads this)
├── .gitignore                          # tooling — excludes .venv, caches, per-run artifacts
├── pyproject.toml                      # tooling — single source of truth for deps
├── uv.lock                             # tooling — committed lockfile (reproducible env)
├── .mutagen.yml                        # orchestration — Mutagen sync ignore rules
│
├── PACKAGE_NAME/                       # all Python code lives here
│   ├── __init__.py
│   ├── config.py                       # scaffold — 4-tier YAML config loader with deep merge
│   │
│   ├── utils/                          # building blocks — domain-neutral plumbing
│   │   ├── attrdict.py                 #   dict with attribute access + nested conversion
│   │   ├── errors.py                   #   CustomException wrapping file/line in the message
│   │   ├── io.py                       #   yaml/pickle/csv reader/writer dispatch
│   │   └── logging.py                  #   configurable file + stream logger
│   │
│   ├── data/                           # scaffold — dataset loading, splits, raw preprocessing
│   │   └── dataset.py
│   ├── features/                       # scaffold — feature extraction / transformation
│   │   └── engineering.py
│   │
│   ├── preprocessing/                  # building blocks — input-side transforms (pluggable axis)
│   │   ├── heatmap_encoder.py          #   KeypointToHeatmap (example: pose → 3D Gaussian volume)
│   │   └── keypoint_normalizer.py      #   symmetric range normaliser / denormaliser
│   ├── postprocessing/                 # building blocks — output-side transforms (pluggable axis)
│   │   └── heatmap_decoder.py          #   HeatmapToKeypoint (inverse of heatmap_encoder)
│   │
│   ├── modeling/                       # scaffold — model factory
│   │   └── model_builder.py
│   │
│   ├── training/                       # mix — entry-point scripts + reusable loop pieces
│   │   ├── train.py                    #   scaffold — main training entry point
│   │   ├── evaluate.py                 #   scaffold — single-dataset checkpoint eval
│   │   ├── evaluate_all.py             #   scaffold — cross-dataset eval
│   │   ├── visualize.py                #   scaffold — prediction visualization entry
│   │   ├── plot_metrics.py             #   scaffold — single-run / --compare multi-run plotting
│   │   ├── check_convergence.py        #   scaffold — converged/not-converged exit code
│   │   ├── callbacks.py                #   building block — EarlyStopping
│   │   └── train_loop.py               #   building blocks — train_one_epoch, evaluate_one_epoch
│   │
│   ├── visualization/                  # scaffold — plotting utilities
│   │   ├── metrics.py                  #   loss / metric curves
│   │   ├── comparison.py               #   multi-run comparison
│   │   └── samples.py                  #   per-sample input / GT / prediction previews
│   │
│   ├── quantization/                   # scaffold — quantization hooks (empty placeholder)
│   │
│   └── cloud/                          # orchestration — optional VM workflow
│       ├── setup_vm.sh                 #   one-time VM setup (mount, symlinks, uv sync)
│       ├── run_training.sh             #   tmux + tee log + auto-shutdown wrapper
│       └── run_pipeline.sh             #   train → check convergence → eval loop
│
├── configs/                            # config — 4-tier YAML system (merged in order)
│   ├── default.yaml                    #   tier 1: base defaults
│   ├── data/_example.yaml              #   tier 2: per-dataset template
│   ├── feature/_example.yaml           #   tier 3: feature-engineering template
│   └── train/
│       ├── _example.yaml               #   tier 4: experiment template
│       └── _example_cont.yaml          #   tier 4: continuation-from-checkpoint template
│
├── tests/                              # pytest suite covering every building block
│   ├── conftest.py                     #   shared fixtures (rng, synthetic keypoints, tensor ds)
│   ├── test_attrdict.py
│   ├── test_io.py
│   ├── test_early_stopping.py
│   ├── test_keypoint_normalizer.py
│   ├── test_heatmap_roundtrip.py
│   └── test_train_loop_smoke.py
│
├── checkpoints/                        # per-run outputs (gitignored; populated at train time)
│   └── <run_id>/
│       ├── weights/{best,last}.pt
│       ├── config_snapshot.yaml
│       ├── results.csv
│       ├── training_metrics.png
│       └── sample_{train,test}_{0,1,2}.png
├── data/{raw,processed}/               # datasets (gitignored; optionally symlinked on VM)
├── logs/                               # execution logs (gitignored)
│
├── README.md                           # docs — quick start, commands, environment
├── ASSETS.md                           # docs — dataset / backbone / checkpoint registry
├── CHANGELOG.md                        # docs — code change history
├── TRAINLOG.md                         # docs — training runs (planned + completed)
└── IO.md                               # docs — input / output format reference
```

## Module Reference

| Subpackage | Role | Status |
|---|---|---|
| `utils/` | attrdict, errors, logging, yaml/pickle/csv I/O | building block |
| `data/` | dataset loading, splits | scaffold |
| `features/` | feature extraction / transformation | scaffold |
| `preprocessing/` | input-side transforms (heatmap_encoder + keypoint_normalizer are one example of the axis) | building block |
| `postprocessing/` | output-side transforms (heatmap_decoder mirrors the example above) | building block |
| `modeling/` | model factory from merged config | scaffold |
| `training/` | `train.py`/`evaluate.py`/… entry points are scaffolds; `callbacks.py` + `train_loop.py` are building blocks | mixed |
| `visualization/` | metric curves, multi-run comparison, sample previews | scaffold |
| `quantization/` | quantization hooks | scaffold (empty placeholder) |
| `cloud/` | optional VM provisioning, tmux-wrapped runs, convergence-driven pipeline | orchestration |

## Tooling & Dev Loop

The template is uv-managed end-to-end. Dependencies live in `pyproject.toml`; `uv.lock` is the committed lockfile; `.python-version` pins the interpreter (currently `3.12`, range `>=3.10,<3.13`).

```bash
# One-time setup in a fresh clone — creates .venv/ from uv.lock
uv sync

# Run the test suite
uv run pytest

# Run a training job
uv run python -m PACKAGE_NAME.training.train --config configs/train/<EXPERIMENT>.yaml

# Add a dependency
uv add <package>

# Add a dev-only dependency
uv add --group dev <package>
```

Never use `pip install` / `requirements.txt` in this project — they would bypass the lockfile and produce drift between local and VM.

## Tests

`tests/` runs under `uv run pytest` and covers every building block:

| File | Covers |
|---|---|
| `conftest.py` | shared fixtures: `rng`, `synthetic_keypoints`, `synthetic_tensor_dataset` |
| `test_attrdict.py` | attribute access + nested dict conversion |
| `test_io.py` | yaml / pickle roundtrip, unknown-extension error |
| `test_early_stopping.py` | counter reset, patience trigger, min_delta semantics |
| `test_keypoint_normalizer.py` | scale ratio, normalise↔denormalise roundtrip, NaN/inf handling |
| `test_heatmap_roundtrip.py` | encode→decode recovers centered keypoints, softmax sums to 1 |
| `test_train_loop_smoke.py` | 2-epoch PyTorch run on a synthetic `TensorDataset` |

## Top-Level Docs

| File | Purpose |
|---|---|
| `README.md` | overview, environment setup, quick-start commands |
| `.agent/dev/SKILL.md` | full project guide: conventions, config system, cloud workflow, checklists |
| `ASSETS.md` | datasets, backbones, checkpoints, outputs |
| `CHANGELOG.md` | code change history |
| `TRAINLOG.md` | training runs — planned + completed with config links |
| `IO.md` | input / output format reference with real examples |

## Cloud / VM (Optional)

If you deploy to a VM with a detachable data disk, `PACKAGE_NAME/cloud/setup_vm.sh` mounts `/mnt/data/<PROJECT_NAME>/` and symlinks three directories into the project tree so all scripts keep using relative paths. The data disk holds everything that would otherwise bloat the git repo.

```
/mnt/data/<PROJECT_NAME>/
├── data/              # raw + processed datasets
├── checkpoints/       # training outputs (weights, config snapshot, results, plots)
└── logs/              # all execution logs
```

| Project path | Data disk target |
|---|---|
| `data/` | `/mnt/data/<PROJECT_NAME>/data/` |
| `checkpoints/` | `/mnt/data/<PROJECT_NAME>/checkpoints/` |
| `logs/` | `/mnt/data/<PROJECT_NAME>/logs/` |

This layout is optional — the template runs locally without any of it.
