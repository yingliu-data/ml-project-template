"""Multi-Run Comparison Visualization.

Called on-demand via training/plot_metrics.py --compare to overlay
loss/metric curves from multiple training runs.

Output: checkpoints/comparison/comparison_<timestamp>.png

Usage:
    from <PACKAGE_NAME>.visualization.comparison import plot_comparison

    plot_comparison(
        ["checkpoints/run_001/", "checkpoints/run_002/"],
        "checkpoints/comparison/"
    )
"""

from typing import List


def plot_comparison(run_dirs: List[str], output_dir: str, dpi: int = 150) -> str:
    """Generate comparison plot across multiple training runs.

    Overlays loss and metric curves from multiple runs on the same axes
    for easy visual comparison. Each run is labeled by its run_id.

    Creates a multi-panel figure with:
    - Training loss comparison
    - Validation loss comparison
    - Primary metric comparison
    - Summary table of best metrics per run

    Args:
        run_dirs: List of paths to run directories
                  (e.g., ['checkpoints/run_001/', 'checkpoints/run_002/']).
        output_dir: Path to save the comparison plot
                    (e.g., 'checkpoints/comparison/').
        dpi: Plot resolution.

    Returns:
        Path to the saved comparison_<timestamp>.png file.
    """
    raise NotImplementedError(
        "Implement: read results from each run_dir, overlay on same axes, save"
    )
