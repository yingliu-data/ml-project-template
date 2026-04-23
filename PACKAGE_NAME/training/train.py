"""Main Training Script.

Loads config, builds model, runs training, then auto-generates:
1. config_snapshot.yaml   → checkpoints/<run_id>/
2. training_metrics.png   → checkpoints/<run_id>/
3. sample previews        → checkpoints/<run_id>/sample_*.png
4. TRAINLOG.md entry      → appended to TRAINLOG.md

Usage:
    python -m <PACKAGE_NAME>.training.train --config configs/train/<experiment>.yaml
    python -m <PACKAGE_NAME>.training.train --config configs/train/<experiment>.yaml --resume

On VM with auto-shutdown:
    python -m <PACKAGE_NAME>.training.train --config configs/train/baseline_v1.yaml \
        2>&1 | tee logs/training/baseline_v1.log && sudo shutdown -h now
"""

import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
TRAINLOG_PATH = PROJECT_ROOT / "TRAINLOG.md"


def parse_args():
    """Parse command-line arguments.

    Returns:
        Namespace with:
        - config: path to train config YAML (required)
        - resume: bool, resume from last checkpoint
    """
    raise NotImplementedError("Implement: argparse with --config and --resume")


def train(config: dict):
    """Run the full training pipeline.

    Steps:
    1. Load and preprocess data (via dataset.load_dataset)
    2. Apply feature engineering (via features.engineering.apply_features)
    3. Build model (via modeling.model_builder.build_model)
    4. Train for config['training']['epochs'] with early stopping
    5. Save best and last checkpoints to checkpoints/<run_id>/

    Args:
        config: Fully merged config dict from config.load_config().

    Returns:
        Dict with training results:
        - best_epoch: int
        - total_epochs: int
        - best_metrics: dict of metric_name → value
        - final_metrics: dict of metric_name → value
        - duration: training time in seconds
    """
    raise NotImplementedError("Implement: full training loop")


def post_training(config: dict, results: dict):
    """Auto-generate artifacts after training completes.

    Called automatically after train() finishes. Generates:
    1. Config snapshot (frozen merged config)
    2. Training metrics plot
    3. Sample preview images (3 train + 3 test)
    4. TRAINLOG.md entry

    Args:
        config: Fully merged config dict.
        results: Training results dict from train().
    """
    raise NotImplementedError(
        "Implement:\n"
        "  1. config.save_config_snapshot(config, run_dir)\n"
        "  2. visualization.metrics.plot_single_run(run_dir)\n"
        "  3. visualization.samples.plot_samples(model, train_data, test_data, run_dir)\n"
        "  4. append_trainlog(config, results)"
    )


def _get_next_run_number():
    """Parse TRAINLOG.md to find the next run number."""
    if not TRAINLOG_PATH.exists():
        return 1
    text = TRAINLOG_PATH.read_text()
    runs = re.findall(r"^## Run (\d+)", text, re.MULTILINE)
    if not runs:
        return 1
    return max(int(r) for r in runs) + 1


def _read_best_metrics(results_path: Path) -> dict:
    """Read results from a training run and extract best-epoch metrics.

    Override this function based on your results format (CSV, JSON, etc.).

    Args:
        results_path: Path to results file (e.g., results.csv).

    Returns:
        Dict with:
        - total_epochs: int
        - best_epoch: int
        - <metric_name>: float (for each tracked metric)
        - train_time_s: float (total training time in seconds)
        Or None if results can't be read.
    """
    raise NotImplementedError(
        "Implement: read results file, find best epoch by primary metric, "
        "return dict of metrics"
    )


def _format_duration(seconds):
    """Format seconds into human-readable duration."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def append_trainlog(config: dict, results: dict):
    """Append a structured entry to TRAINLOG.md.

    Writes a markdown entry with:
    - Run metadata (experiment name, date, configs, init weights)
    - Best metrics
    - Pointers to saved model, visualization, log
    - Improvement over previous run (if continuation)

    Args:
        config: Fully merged config dict.
        results: Training results dict from train().
    """
    raise NotImplementedError(
        "Implement:\n"
        "  1. _get_next_run_number() for run ID\n"
        "  2. Format entry with config references and metrics\n"
        "  3. Include init weights path (checkpoint_path from config)\n"
        "  4. Insert before template comment in TRAINLOG.md"
    )


if __name__ == "__main__":
    """Entry point: parse args → load config → train → post-training."""
    raise NotImplementedError(
        "Implement:\n"
        "  args = parse_args()\n"
        "  config = load_config(args.config)\n"
        "  if args.resume:\n"
        "      config['training']['resume'] = True\n"
        "  results = train(config)\n"
        "  post_training(config, results)"
    )
