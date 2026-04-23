"""Feature Engineering Pipeline.

Applies feature extraction and transformation based on the feature config
(configs/feature/<name>.yaml). Processed features are cached in data/processed/<method>/.

Can be run standalone:
    python -m <PACKAGE_NAME>.features.engineering --config configs/feature/<method>.yaml

Or called from training/train.py as part of the pipeline.

Usage:
    from <PACKAGE_NAME>.features.engineering import apply_features

    features = apply_features(raw_data, config)
"""


def apply_features(data, config: dict):
    """Apply feature engineering to raw data.

    Reads the feature config tier to determine:
    - Preprocessing (normalization, sampling rate, clipping)
    - Feature extraction (windowing, stats, spectral, embeddings)
    - Dimensionality reduction (PCA, etc.)

    Results are cached to config['feature']['cache_dir'] (data/processed/<method>/)
    so subsequent runs with the same feature config skip reprocessing.

    Args:
        data: Raw data (output of dataset.load_dataset()).
        config: Merged config dict. Uses keys from configs/feature/<name>.yaml:
            - preprocessing.normalization, preprocessing.sampling_rate
            - extraction.method, extraction.window_length
            - reduction.method, reduction.params

    Returns:
        Processed feature data, ready for model input.
    """
    raise NotImplementedError("Implement: preprocess, extract features, reduce, cache")


def load_cached_features(config: dict):
    """Load previously cached features from data/processed/<method>/.

    Args:
        config: Merged config dict with feature cache_dir.

    Returns:
        Cached feature data, or None if cache doesn't exist.
    """
    raise NotImplementedError("Implement: check cache dir, load if exists")


if __name__ == "__main__":
    """Standalone feature engineering entry point.

    Usage:
        python -m <PACKAGE_NAME>.features.engineering --config configs/feature/<method>.yaml

    Loads raw data, applies feature engineering, and caches results.
    """
    raise NotImplementedError("Implement: argparse, load data, apply features, save")
