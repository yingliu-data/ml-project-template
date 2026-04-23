"""Input/Output Sample Preview Visualization.

Auto-called by training/train.py after each training run completes.
Randomly selects samples from train and test sets, runs inference,
and generates side-by-side comparison images.

Output:
    checkpoints/<run_id>/sample_train_0.png
    checkpoints/<run_id>/sample_train_1.png
    checkpoints/<run_id>/sample_train_2.png
    checkpoints/<run_id>/sample_test_0.png
    checkpoints/<run_id>/sample_test_1.png
    checkpoints/<run_id>/sample_test_2.png

Each image shows: input | ground truth | model prediction

Usage:
    from <PACKAGE_NAME>.visualization.samples import plot_samples

    plot_samples(model, train_data, test_data, "checkpoints/baseline_v1/")
"""

import random


def plot_samples(
    model,
    train_data,
    test_data,
    output_dir: str,
    n_train: int = 3,
    n_test: int = 3,
    seed: int = 42,
    dpi: int = 150,
) -> list:
    """Generate input/output sample preview images.

    For each selected sample, creates a figure showing:
    - Row 1 (train samples): input, ground truth, model prediction
    - Row 2 (test samples): input, ground truth, model prediction

    Samples are randomly selected (with fixed seed for reproducibility).

    Args:
        model: Trained model for running inference.
        train_data: Training dataset (from dataset.load_dataset()).
        test_data: Test/validation dataset.
        output_dir: Path to save sample images
                    (e.g., 'checkpoints/<run_id>/').
        n_train: Number of random train samples to visualize.
        n_test: Number of random test samples to visualize.
        seed: Random seed for sample selection.
        dpi: Plot resolution.

    Returns:
        List of paths to saved sample images.
    """
    raise NotImplementedError(
        "Implement: select random samples, run inference, "
        "create side-by-side figures (input | GT | prediction), save"
    )
