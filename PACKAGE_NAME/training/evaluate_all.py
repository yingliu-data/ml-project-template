"""Cross-Dataset Evaluation Script.

Evaluates a single checkpoint across multiple datasets and prints a comparison table.
Useful for generalist models trained on mixed datasets.

Usage:
    python -m <PACKAGE_NAME>.training.evaluate_all \
        --checkpoint checkpoints/<run_id>/weights/best.pt \
        --datasets coco2017 mpii crowdpose \
        --batch 64
"""


def parse_args():
    """Parse command-line arguments.

    Returns:
        Namespace with:
        - checkpoint: path to model checkpoint
        - datasets: list of dataset config names
        - batch: batch size for evaluation
    """
    raise NotImplementedError("Implement: argparse with --checkpoint, --datasets, --batch")


def evaluate_all(checkpoint_path: str, dataset_names: list, batch_size: int):
    """Evaluate a checkpoint on multiple datasets.

    For each dataset:
    1. Load dataset config from configs/data/<name>.yaml
    2. Build dataset and dataloader
    3. Run inference and compute metrics
    4. Collect results

    Args:
        checkpoint_path: Path to model checkpoint file.
        dataset_names: List of dataset config names.
        batch_size: Batch size for evaluation.

    Returns:
        Dict mapping dataset_name → metrics dict.
    """
    raise NotImplementedError(
        "Implement:\n"
        "  1. Load model from checkpoint\n"
        "  2. For each dataset: load config, build dataloader, evaluate\n"
        "  3. Print comparison table\n"
        "  4. Return results dict"
    )


if __name__ == "__main__":
    args = parse_args()
    results = evaluate_all(args.checkpoint, args.datasets, args.batch)
