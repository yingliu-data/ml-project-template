"""Training Metrics Plotting CLI.

Two modes:
1. Single run: plot loss/metric curves for one training run
2. Comparison: overlay curves from multiple runs for side-by-side comparison

Usage:
    # Single run
    python -m <PACKAGE_NAME>.training.plot_metrics --run_dir checkpoints/<run_id>

    # Compare multiple runs
    python -m <PACKAGE_NAME>.training.plot_metrics --compare checkpoints/run_001 checkpoints/run_002 checkpoints/run_003

    # Custom output location
    python -m <PACKAGE_NAME>.training.plot_metrics --run_dir checkpoints/<run_id> --output checkpoints/custom/
"""


def parse_args():
    """Parse command-line arguments.

    Mutually exclusive modes:
    - --run_dir: single run mode (generates training_metrics.png)
    - --compare: comparison mode (generates comparison_<timestamp>.png)

    Returns:
        Namespace with:
        - run_dir: path to single run directory (or None)
        - compare: list of paths to run directories (or None)
        - output: custom output directory (optional)
        - dpi: plot resolution (default: 150)
    """
    raise NotImplementedError(
        "Implement: argparse with mutually exclusive --run_dir and --compare"
    )


if __name__ == "__main__":
    """Entry point: parse args → dispatch to single or comparison mode.

    Single mode:
        visualization.metrics.plot_single_run(run_dir, output_dir)

    Comparison mode:
        visualization.comparison.plot_comparison(run_dirs, output_dir)
    """
    raise NotImplementedError(
        "Implement:\n"
        "  args = parse_args()\n"
        "  if args.run_dir:\n"
        "      plot_single_run(args.run_dir, output_dir)\n"
        "  elif args.compare:\n"
        "      plot_comparison(args.compare, output_dir)"
    )
