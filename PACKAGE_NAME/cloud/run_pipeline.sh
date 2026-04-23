#!/usr/bin/env bash
# =============================================================================
# Multi-Step Training Pipeline — train + convergence check + eval + shutdown
# =============================================================================
# Trains a model, checks convergence (auto-resumes if not converged),
# runs cross-dataset evaluation, then shuts down the VM.
#
# Usage (on VM):
#   bash <PACKAGE_NAME>/cloud/run_pipeline.sh <config_name> [--datasets "ds1 ds2 ds3"]
#
# Example:
#   bash <PACKAGE_NAME>/cloud/run_pipeline.sh baseline_v1
#   bash <PACKAGE_NAME>/cloud/run_pipeline.sh generalist_v1 --datasets "coco2017 mpii crowdpose"

set -e

# === Configuration ===
PROJECT_NAME="<PROJECT_NAME>"
PROJECT_DIR="$HOME/$PROJECT_NAME"

# === Parse arguments ===
if [ $# -lt 1 ]; then
    echo "Usage: $0 <config_name> [--datasets \"ds1 ds2 ds3\"]"
    exit 1
fi

CONFIG_NAME="$1"
DATASETS=""
if [ "${2:-}" = "--datasets" ]; then
    DATASETS="$3"
fi

CONFIG_PATH="configs/train/${CONFIG_NAME}.yaml"
SAVED_MODEL_DIR="checkpoints/${CONFIG_NAME}"
LOG_PATH="logs/training/${CONFIG_NAME}_pipeline.log"

cd "$PROJECT_DIR"

echo "============================================"
echo "=== Pipeline Started: $(date) ==="
echo "=== Config: $CONFIG_NAME ==="
echo "============================================"

# --- Step 1: Train (with convergence loop) ---
echo ""
echo "=== Training $CONFIG_NAME ==="
python3 -m <PACKAGE_NAME>.training.train --config "$CONFIG_PATH"

while ! python3 -m <PACKAGE_NAME>.training.check_convergence "$SAVED_MODEL_DIR"; do
    echo "=== Not converged, resuming... ==="
    python3 -m <PACKAGE_NAME>.training.train --config "$CONFIG_PATH" --resume
done
echo "=== Training complete ==="

# --- Step 2: Cross-dataset evaluation (optional) ---
if [ -n "$DATASETS" ]; then
    echo ""
    echo "=== Cross-dataset evaluation ==="
    python3 -m <PACKAGE_NAME>.training.evaluate_all \
        --checkpoint "$SAVED_MODEL_DIR/best.pt" \
        --datasets $DATASETS \
        --batch 64
fi

echo ""
echo "============================================"
echo "=== Pipeline Complete: $(date) ==="
echo "============================================"
sudo shutdown -h now
