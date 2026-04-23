"""Model Factory — Build Models from Config.

Creates model instances based on the model config (configs/default.yaml + train overrides).

Usage:
    from <PACKAGE_NAME>.modeling.model_builder import build_model

    model = build_model(config)
"""


def build_model(config: dict):
    """Build a model from the merged config.

    Weight loading priority:
    1. checkpoint_path (if set) — loads from a previous run's checkpoint
    2. pretrained_weights (if set) — loads pretrained backbone/foundation weights
    3. Neither — trains from scratch (random init)

    Args:
        config: Merged config dict. Uses keys:
            - model.name: architecture name
            - model.checkpoint_path: path to init from previous run (or null)
            - model.pretrained_weights: path/URL to pretrained weights (or null)
            - model.input_size: input resolution
            - model.device: GPU device index, list for DDP [0,1], or "cpu"

    Returns:
        Initialized model (framework-specific: nn.Module, keras.Model, etc.)
    """
    raise NotImplementedError(
        "Implement:\n"
        "  model_cfg = config['model']\n"
        "  weights = model_cfg.get('checkpoint_path') or model_cfg.get('pretrained_weights')\n"
        "  # Build model architecture, load weights if provided\n"
        "  # Handle multi-GPU (DDP) if device is a list"
    )


def load_checkpoint(model, checkpoint_path: str):
    """Load a checkpoint into an existing model.

    Args:
        model: Model instance.
        checkpoint_path: Path to checkpoint file (e.g., checkpoints/<run_id>/weights/best.pt).

    Returns:
        Model with loaded weights.
    """
    raise NotImplementedError("Implement: load checkpoint weights into model")
