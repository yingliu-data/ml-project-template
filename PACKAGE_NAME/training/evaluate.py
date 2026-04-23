"""Evaluate a Trained Checkpoint.

Loads a trained model checkpoint and evaluates it on the validation or test set.
Prints metrics to stdout and optionally logs to evaluation log file.

Usage:
    python -m <PACKAGE_NAME>.training.evaluate \
        --config configs/train/<experiment>.yaml \
        --checkpoint checkpoints/<run_id>/weights/best.pt

    python -m <PACKAGE_NAME>.training.evaluate \
        --config configs/train/<experiment>.yaml \
        --checkpoint checkpoints/<run_id>/weights/best.pt \
        --split test
"""


def parse_args():
    """Parse command-line arguments.

    Returns:
        Namespace with:
        - config: path to train config YAML (required)
        - checkpoint: path to model checkpoint (required)
        - split: evaluation split — 'val' (default) or 'test'
    """
    raise NotImplementedError("Implement: argparse with --config, --checkpoint, --split")


def evaluate(config: dict, checkpoint_path: str, split: str = "val") -> dict:
    """Evaluate a checkpoint on a dataset split.

    Steps:
    1. Load dataset (via dataset.load_dataset)
    2. Apply feature engineering (via features.engineering)
    3. Build model and load checkpoint
    4. Run inference on the specified split
    5. Compute and return metrics

    Args:
        config: Fully merged config dict.
        checkpoint_path: Path to the model checkpoint.
        split: Which split to evaluate on ('val' or 'test').

    Returns:
        Dict of metric_name → value.
    """
    raise NotImplementedError("Implement: load model, run eval, compute metrics")


if __name__ == "__main__":
    """Entry point: parse args → load config → evaluate → print metrics."""
    raise NotImplementedError(
        "Implement:\n"
        "  args = parse_args()\n"
        "  config = load_config(args.config)\n"
        "  metrics = evaluate(config, args.checkpoint, args.split)\n"
        "  print(metrics)"
    )
