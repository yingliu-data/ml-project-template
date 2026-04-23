"""Training Metrics Visualization — Single Run.

Auto-called by training/train.py after each training run completes.
Reads the training log (CSV, TensorBoard, or framework-specific format)
and generates loss/metric curve plots.

Output: checkpoints/<run_id>/training_metrics.png

Usage:
    from <PACKAGE_NAME>.visualization.metrics import plot_single_run

    plot_single_run("checkpoints/baseline_v1/")
"""


def plot_single_run(run_dir: str, output_dir: str = None, dpi: int = 150) -> str:
    """Generate training metrics plot for a single run.

    Reads training results (loss curves, metric curves) from the run directory
    and creates a multi-panel figure with:
    - Training loss curve
    - Validation loss curve
    - Primary metric(s) over epochs
    - Secondary metric(s) over epochs (if available)

    Args:
        run_dir: Path to the run's checkpoint directory
                 (e.g., 'checkpoints/<run_id>/').
                 Expected to contain results.csv or equivalent.
        output_dir: Path to save the plot. Defaults to run_dir itself.
        dpi: Plot resolution.

    Returns:
        Path to the saved training_metrics.png file.
    """
    raise NotImplementedError(
        "Implement: read results from run_dir, create matplotlib figure, save to output_dir or run_dir"
    )
