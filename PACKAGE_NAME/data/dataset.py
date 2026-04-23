"""Dataset Loading and Preprocessing.

Loads datasets based on the data config (configs/data/<name>.yaml)
and returns train/val/test splits ready for the feature engineering pipeline.

Usage:
    from <PACKAGE_NAME>.data.dataset import load_dataset

    train_data, val_data, test_data = load_dataset(config)
"""


def load_dataset(config: dict):
    """Load dataset based on the merged config.

    Reads raw data from the paths specified in the data config tier,
    applies basic preprocessing (e.g., format parsing, filtering),
    and returns train/val/test splits.

    Args:
        config: Merged config dict from config.load_config().
            Uses keys from configs/data/<name>.yaml:
            - data_dir, train.images, train.annotations, etc.
            - num_classes, input_shape, file_format

    Returns:
        Tuple of (train_data, val_data, test_data).
        Format depends on the dataset (e.g., numpy arrays, DataLoader, file lists).
    """
    raise NotImplementedError("Implement: load data from config paths, return splits")


def get_sample(dataset, index: int):
    """Get a single sample from a dataset split.

    Used by visualization.samples to retrieve samples for preview plots.

    Args:
        dataset: One of the splits returned by load_dataset().
        index: Sample index.

    Returns:
        Tuple of (input, target) for the given sample.
    """
    raise NotImplementedError("Implement: return (input, target) for a sample")
