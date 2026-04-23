"""Generate Prediction Visualizations.

Loads a trained checkpoint and generates visual comparisons of
model predictions against ground truth on selected samples.

Usage:
    python -m <PACKAGE_NAME>.training.visualize \
        --config configs/train/<experiment>.yaml \
        --checkpoint checkpoints/<run_id>/weights/best.pt \
        --num_samples 16

    python -m <PACKAGE_NAME>.training.visualize \
        --config configs/train/<experiment>.yaml \
        --checkpoint checkpoints/<run_id>/weights/best.pt \
        --output_dir checkpoints/<run_id>/custom/
"""


def parse_args():
    """Parse command-line arguments.

    Returns:
        Namespace with:
        - config: path to train config YAML (required)
        - checkpoint: path to model checkpoint (required)
        - num_samples: number of samples to visualize (default: 16)
        - output_dir: custom output directory (default: checkpoints/<run_id>/)
        - split: which split to sample from — 'val' (default) or 'test'
        - seed: random seed for sample selection (default: 42)
    """
    raise NotImplementedError(
        "Implement: argparse with --config, --checkpoint, --num_samples, "
        "--output_dir, --split, --seed"
    )


def visualize(config: dict, checkpoint_path: str, num_samples: int = 16,
              output_dir: str = None, split: str = "val", seed: int = 42):
    """Generate prediction visualization images.

    For each selected sample, creates a figure showing the input,
    ground truth, and model prediction side by side.

    Args:
        config: Fully merged config dict.
        checkpoint_path: Path to the model checkpoint.
        num_samples: Number of samples to visualize.
        output_dir: Directory to save visualizations.
        split: Which split to sample from.
        seed: Random seed for reproducible sample selection.
    """
    raise NotImplementedError(
        "Implement: load model, select samples, run inference, "
        "generate comparison figures, save"
    )


if __name__ == "__main__":
    """Entry point: parse args → load config → visualize."""
    raise NotImplementedError(
        "Implement:\n"
        "  args = parse_args()\n"
        "  config = load_config(args.config)\n"
        "  visualize(config, args.checkpoint, ...)"
    )
