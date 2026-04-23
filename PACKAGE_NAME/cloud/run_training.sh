#!/usr/bin/env bash
# =============================================================================
# Training Runner — tmux + logging + auto-shutdown
# =============================================================================
# Starts a training run in a detached tmux session with logging and auto-shutdown.
#
# Usage (from local machine):
#   gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> \
#     --command="bash ~/<PROJECT_NAME>/<PACKAGE_NAME>/cloud/run_training.sh <config_name>"
#
# Usage (on VM):
#   bash <PACKAGE_NAME>/cloud/run_training.sh <config_name>
#
# Example:
#   bash <PACKAGE_NAME>/cloud/run_training.sh baseline_v1
#   # This runs: python -m <PACKAGE_NAME>.training.train --config configs/train/baseline_v1.yaml
#   # Logs to: logs/training/baseline_v1.log
#   # Auto-shuts down VM after completion

set -euo pipefail

# === Configuration ===
PROJECT_NAME="<PROJECT_NAME>"
PROJECT_DIR="$HOME/$PROJECT_NAME"

# === Parse arguments ===
if [ $# -lt 1 ]; then
    echo "Usage: $0 <config_name> [--resume]"
    echo ""
    echo "  config_name  Name of the train config (without .yaml extension)"
    echo "               e.g., 'baseline_v1' loads configs/train/baseline_v1.yaml"
    echo "               e.g., 'baseline_v1_cont' for continuation from checkpoint"
    echo ""
    echo "  --resume     Resume from last checkpoint (optional)"
    echo ""
    echo "Examples:"
    echo "  $0 baseline_v1             # Fresh training"
    echo "  $0 baseline_v1 --resume    # Resume interrupted training"
    echo "  $0 baseline_v1_cont        # Continue from previous run's best.pt"
    exit 1
fi

CONFIG_NAME="$1"
RESUME_FLAG=""
if [ "${2:-}" = "--resume" ]; then
    RESUME_FLAG="--resume"
fi

CONFIG_PATH="configs/train/${CONFIG_NAME}.yaml"
LOG_PATH="logs/training/${CONFIG_NAME}.log"
SESSION_NAME="train-${CONFIG_NAME}"

# === Validate ===
if [ ! -f "$PROJECT_DIR/$CONFIG_PATH" ]; then
    echo "ERROR: Config file not found: $PROJECT_DIR/$CONFIG_PATH"
    exit 1
fi

# === Launch in tmux ===
echo "Starting training run: $CONFIG_NAME"
echo "  Config: $CONFIG_PATH"
echo "  Log:    $LOG_PATH"
echo "  tmux:   $SESSION_NAME"
echo "  VM will auto-shutdown after training completes."
echo ""

TRAIN_CMD="cd $PROJECT_DIR && python -m <PACKAGE_NAME>.training.train --config $CONFIG_PATH $RESUME_FLAG 2>&1 | tee $LOG_PATH && sudo shutdown -h now"

# Kill existing session with same name (if any)
tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true

# Start detached tmux session
tmux new-session -d -s "$SESSION_NAME" "$TRAIN_CMD"

echo "Training started in tmux session '$SESSION_NAME'."
echo ""
echo "To monitor:"
echo "  tmux attach -t $SESSION_NAME          # Attach to session"
echo "  tail -f $LOG_PATH                     # Follow log"
echo ""
echo "To detach from tmux: Ctrl+B then D"
echo "Safe to close SSH — training continues in background."
