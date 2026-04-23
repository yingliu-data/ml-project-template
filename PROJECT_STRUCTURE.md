# Project Structure

```
<PROJECT_NAME>/
├── .agent/                            # Agent configuration
│   └── dev/
│       └── SKILL.md                   # Full project guide (config, workflow, cloud, checklists)
│
├── configs/                           # All configuration files (4-tier system)
│   ├── default.yaml                   # Tier 1: base defaults (model, augmentation, viz)
│   ├── data/                          # Tier 2: per-dataset configs
│   │   └── _example.yaml             # Template for new datasets
│   ├── feature/                       # Tier 3: feature engineering configs
│   │   └── _example.yaml             # Template for new feature methods
│   └── train/                         # Tier 4: experiment configs (refs data + feature)
│       ├── _example.yaml             # Template for new experiments
│       └── _example_cont.yaml        # Template for continuation runs (different optimizer/LR)
│
├── <PACKAGE_NAME>/                    # Core Python package (all code lives here)
│   ├── __init__.py
│   ├── config.py                      # 4-tier YAML config loader with deep merge
│   ├── data/
│   │   ├── __init__.py
│   │   └── dataset.py                 # Dataset loading, splits, preprocessing
│   ├── features/
│   │   ├── __init__.py
│   │   └── engineering.py             # Feature extraction and transformation
│   ├── modeling/
│   │   ├── __init__.py
│   │   └── model_builder.py           # Model factory: build model from config
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── metrics.py                 # Loss/metric curve plotting (auto after train)
│   │   ├── comparison.py              # Multi-run comparison plots
│   │   └── samples.py                 # Input/output sample preview (auto after train)
│   ├── training/                      # Entry-point scripts (run on VM)
│   │   ├── __init__.py
│   │   ├── train.py                   # Main training + auto-plot + auto-sample + auto-log
│   │   ├── evaluate.py                # Evaluate a checkpoint on val/test set
│   │   ├── evaluate_all.py            # Cross-dataset evaluation (multiple datasets at once)
│   │   ├── visualize.py               # Generate prediction visualizations
│   │   ├── plot_metrics.py            # Single-run or --compare multi-run plotting
│   │   └── check_convergence.py       # Check if run converged (exit code 0/1 for scripting)
│   └── cloud/                         # Cloud VM management scripts
│       ├── __init__.py
│       ├── setup_vm.sh                # One-time VM setup (mount disk, symlinks, deps)
│       ├── run_training.sh            # Wrapper: tmux + train.py + tee log + auto-shutdown
│       └── run_pipeline.sh            # Multi-step pipeline: train → check convergence → eval
│
├── checkpoints/                       # All training outputs (on data disk via symlink)
│   └── <run_id>/                      # Self-contained run directory (folder name = config run_id)
│       ├── weights/
│       │   ├── best.pt               # Best checkpoint
│       │   └── last.pt               # Latest checkpoint
│       ├── config_snapshot.yaml       # Frozen merged config at training time
│       ├── results.csv                # Per-epoch metrics
│       ├── training_metrics.png       # Loss + metric curves
│       ├── sample_train_{0,1,2}.png  # Train sample previews (input/GT/prediction)
│       ├── sample_test_{0,1,2}.png   # Test sample previews (input/GT/prediction)
│       └── ...                        # Any other per-run outputs (PR curves, confusion matrices, etc.)
│
├── data/                              # Datasets (on data disk via symlink)
│   ├── raw/                           # Unprocessed source data
│   └── processed/                     # Feature-engineered / preprocessed data
│
├── logs/                              # Execution logs (on data disk via symlink)
│   ├── training/                      # Training run stdout/stderr
│   ├── feature/                       # Feature engineering run logs
│   ├── evaluation/                    # Evaluation run logs
│   ├── data/                          # Data conversion/processing logs
│   └── cloud/                         # VM setup, mount, sync, GPU change logs
│
├── .mutagen.yml                       # Mutagen sync ignore rules
├── README.md                          # Project overview and usage
├── PROJECT_STRUCTURE.md               # This file
├── ASSETS.md                          # Datasets, backbones, checkpoints
├── CHANGELOG.md                       # Code change history
├── TRAINLOG.md                        # Training run log with config links
└── IO.md                              # Input/output format reference
```

## Remote-Only Directories (on VM data disk, symlinked into project)

These directories live on the detachable data disk (`/mnt/data/<PROJECT_NAME>/`) and are symlinked into the project tree so scripts use relative paths.

```
/mnt/data/<PROJECT_NAME>/
├── data/                   # Large datasets (raw + processed)
├── checkpoints/            # Training outputs (weights, config, results, plots)
└── logs/                   # All execution logs
```

## Symlinks (VM)

| Project Path | Data Disk Target |
|-------------|------------------|
| `data/` | `/mnt/data/<PROJECT_NAME>/data/` |
| `checkpoints/` | `/mnt/data/<PROJECT_NAME>/checkpoints/` |
| `logs/` | `/mnt/data/<PROJECT_NAME>/logs/` |
