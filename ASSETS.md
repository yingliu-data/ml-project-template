# Assets

## Datasets

| Name | Location | Format | Size | Description |
|------|----------|--------|------|-------------|
| `<DATASET_1>` | `/mnt/data/<PROJECT_NAME>/data/raw/<dataset_1>/` | `<format>` | `<size>` | `<description>` |
| `<DATASET_2>` | `/mnt/data/<PROJECT_NAME>/data/raw/<dataset_2>/` | `<format>` | `<size>` | `<description>` |

### <DATASET_1> Layout

```
data/raw/<dataset_1>/
├── train/
├── val/
└── annotations/
    ├── train.json
    └── val.json
```

### <DATASET_2> Layout

```
data/raw/<dataset_2>/
├── ...
```

## Model Backbone / Pretrained Weights

| Name | Source | Used By | Notes |
|------|--------|---------|-------|
| `<BACKBONE_NAME>` | `<URL or path>` | `configs/train/*.yaml` | `<e.g., auto-downloaded, manually placed>` |

## Model Checkpoints (Training Outputs)

| Run | Config | Path | Init Weights | Key Metric | Description |
|-----|--------|------|-------------|:----------:|-------------|
| `<run_id>` | `configs/train/<experiment>.yaml` | `checkpoints/<run_id>/` | `<source checkpoint>` | `<value>` | `<description>` |

## Outputs

| Name | Path | Description |
|------|------|-------------|
| Checkpoints | `checkpoints/<run_id>/` | Weights, frozen config, results, metric curves, sample previews |
| Training logs | `logs/training/<run_id>.log` | Full stdout/stderr from training |
| Feature logs | `logs/feature/<method>.log` | Feature engineering run logs |
| Evaluation logs | `logs/evaluation/<run_id>_eval.log` | Evaluation run logs |
