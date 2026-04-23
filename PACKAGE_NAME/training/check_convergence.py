"""Check if a training run has converged.

Reads results from a run directory and determines if training converged
(early stopping triggered) or if the model was still improving.

Exit codes:
    0 = converged (safe to stop)
    1 = not converged (still improving, consider continuing)

Usage:
    python -m <PACKAGE_NAME>.training.check_convergence checkpoints/<run_id>

In a pipeline script:
    while ! python -m <PACKAGE_NAME>.training.check_convergence checkpoints/<run_id>; do
        echo "Not converged, resuming..."
        python -m <PACKAGE_NAME>.training.train --config configs/train/<experiment>.yaml --resume
    done
"""

import sys
from pathlib import Path


def check_convergence(run_dir: str) -> bool:
    """Check if training has converged by comparing best epoch vs total epochs.

    If best_epoch < total_epochs, patience triggered early stopping → converged.
    If best_epoch == total_epochs, model was still improving → not converged.

    Args:
        run_dir: Path to the run directory containing results (e.g., results.csv).

    Returns:
        True if converged, False if still improving.
    """
    raise NotImplementedError(
        "Implement:\n"
        "  1. Read results.csv (or equivalent) from run_dir\n"
        "  2. Find the primary metric column\n"
        "  3. Determine best_epoch and total_epochs\n"
        "  4. If best_epoch < total_epochs: converged (patience stopped it)\n"
        "  5. If best_epoch == total_epochs: NOT converged (still improving)\n"
        "  6. Also check fitness (weighted metric combo) not just single metric\n"
        "  7. Print status: 'Converged at epoch X (best: Y)' or\n"
        "     'Not converged: best at epoch X of Y, recent gain: +Z over last 10 epochs'"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <run_dir>")
        sys.exit(2)

    run_dir = sys.argv[1]
    if not Path(run_dir).exists():
        print(f"ERROR: Run directory not found: {run_dir}")
        sys.exit(2)

    converged = check_convergence(run_dir)
    sys.exit(0 if converged else 1)
