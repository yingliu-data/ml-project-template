"""4-Tier YAML Configuration Loader.

Loads and deep-merges configuration from 4 tiers:

1. configs/default.yaml          — base defaults (model, augmentation, viz)
2. configs/data/<name>.yaml      — dataset paths and properties
3. configs/feature/<name>.yaml   — feature engineering pipeline
4. configs/train/<name>.yaml     — experiment hyperparameters (top-level config)

The train config references data and feature configs by name:
    data_config: <dataset_name>       → loads configs/data/<dataset_name>.yaml
    feature_config: <method_name>     → loads configs/feature/<method_name>.yaml

Multi-dataset support:
    datasets: [coco2017, mpii, crowdpose]  → loads and merges all data configs

Usage:
    from <PACKAGE_NAME>.config import load_config, save_config_snapshot

    config = load_config("configs/train/baseline_v1.yaml")
    # config is a fully merged dict with all 4 tiers

    save_config_snapshot(config, "checkpoints/baseline_v1/")
    # Saves frozen config_snapshot.yaml for reproducibility
"""


def load_config(train_config_path: str) -> dict:
    """Load and merge 4-tier configuration.

    Args:
        train_config_path: Path to the tier-4 train config YAML file.
            Must contain 'data_config' (single dataset) or 'datasets' (multi-dataset list),
            and 'feature_config' referencing tier-2 and tier-3 configs by name.

    Returns:
        Fully merged config dict. Contains all keys from all 4 tiers,
        with later tiers overriding earlier ones. Also includes:
        - '_data_config_path': resolved path to the data config file(s)
        - '_feature_config_path': resolved path to the feature config file
        - '_train_config_path': path to the train config file
        - 'datasets_resolved': list of resolved dataset config dicts (for multi-dataset)

    Merge order (later overrides earlier):
        default.yaml → data/<name>.yaml → feature/<name>.yaml → train/<name>.yaml
    """
    raise NotImplementedError(
        "Implement:\n"
        "  1. Load default.yaml\n"
        "  2. Load data config(s) — support both 'data_config' (single) and 'datasets' (list)\n"
        "  3. Load feature config\n"
        "  4. Load train config\n"
        "  5. Deep-merge in order\n"
        "  6. For multi-dataset: build combined dataset YAML (e.g., temp file with all paths)"
    )


def save_config_snapshot(config: dict, run_dir: str) -> str:
    """Save a frozen copy of the merged config to the run directory.

    This preserves the exact configuration used for a training run,
    even if source config files are later modified.

    Args:
        config: Fully merged config dict from load_config().
        run_dir: Path to the run's checkpoint directory
                 (e.g., 'checkpoints/<run_id>/').

    Returns:
        Path to the saved config_snapshot.yaml file.
    """
    raise NotImplementedError("Implement: write config dict to YAML file")


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override dict into base dict.

    For nested dicts, merge recursively. For all other types,
    override replaces base.

    Args:
        base: Base configuration dict.
        override: Dict with values to override.

    Returns:
        New merged dict (does not modify inputs).
    """
    raise NotImplementedError("Implement: recursive dict merge")
