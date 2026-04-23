#!/usr/bin/env bash
# =============================================================================
# One-Time VM Setup Script
# =============================================================================
# Run this on the VM after creating/attaching a data disk.
# Usage: bash <PACKAGE_NAME>/cloud/setup_vm.sh
#
# What it does:
# 1. Detects the data disk device name
# 2. Mounts the data disk to /mnt/data
# 3. Creates project directories on the data disk
# 4. Creates symlinks from project directory to data disk
# 5. Adds fstab entry for auto-mount on reboot
# 6. Installs Python dependencies

set -euo pipefail

# === Configuration ===
# Replace these placeholders before running!
PROJECT_NAME="<PROJECT_NAME>"
PROJECT_DIR="$HOME/$PROJECT_NAME"
DATA_MOUNT="/mnt/data"
DATA_DIR="$DATA_MOUNT/$PROJECT_NAME"

# === Step 1: Detect data disk device ===
echo "=== Detecting data disk device ==="
echo "Current block devices:"
lsblk
echo ""

# Try common device names
if [ -b /dev/nvme0n2 ]; then
    DEVICE="/dev/nvme0n2"
    echo "Detected NVMe data disk: $DEVICE (GPU VM)"
elif [ -b /dev/sdb ]; then
    DEVICE="/dev/sdb"
    echo "Detected SCSI data disk: $DEVICE (Standard VM)"
else
    echo "ERROR: Could not auto-detect data disk device."
    echo "Please check 'lsblk' output and set DEVICE manually."
    exit 1
fi

# === Step 2: Mount data disk ===
echo ""
echo "=== Mounting $DEVICE to $DATA_MOUNT ==="

if mountpoint -q "$DATA_MOUNT"; then
    echo "$DATA_MOUNT is already mounted."
else
    sudo mkdir -p "$DATA_MOUNT"

    # Check if disk has a filesystem
    if ! sudo blkid "$DEVICE" | grep -q 'TYPE='; then
        echo "Disk has no filesystem. Formatting with ext4..."
        echo "WARNING: This will erase all data on $DEVICE!"
        read -p "Continue? (y/N): " confirm
        if [ "$confirm" != "y" ]; then
            echo "Aborted."
            exit 1
        fi
        sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0 "$DEVICE"
    fi

    sudo mount "$DEVICE" "$DATA_MOUNT"
    sudo chown "$USER:$USER" "$DATA_MOUNT"
    echo "Mounted $DEVICE to $DATA_MOUNT"
fi

# === Step 3: Add to fstab (if not already there) ===
if ! grep -q "$DATA_MOUNT" /etc/fstab; then
    echo "$DEVICE $DATA_MOUNT ext4 defaults,nofail 0 2" | sudo tee -a /etc/fstab
    echo "Added fstab entry for auto-mount."
else
    echo "fstab entry already exists."
fi

# === Step 4: Create project directories on data disk ===
echo ""
echo "=== Creating project directories on data disk ==="

DIRS=(
    "data"
    "data/raw"
    "data/processed"
    "checkpoints"
    "logs"
    "logs/training"
    "logs/feature"
    "logs/evaluation"
    "logs/data"
    "logs/cloud"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$DATA_DIR/$dir"
    echo "  Created $DATA_DIR/$dir"
done

# === Step 5: Create symlinks ===
echo ""
echo "=== Creating symlinks ==="

mkdir -p "$PROJECT_DIR"

SYMLINKS=("data" "checkpoints" "logs")

for dir in "${SYMLINKS[@]}"; do
    if [ -L "$PROJECT_DIR/$dir" ]; then
        echo "  Symlink already exists: $PROJECT_DIR/$dir -> $(readlink "$PROJECT_DIR/$dir")"
    elif [ -d "$PROJECT_DIR/$dir" ]; then
        echo "  WARNING: $PROJECT_DIR/$dir is a real directory, not a symlink."
        echo "  Move its contents to $DATA_DIR/$dir and replace with a symlink."
    else
        ln -sf "$DATA_DIR/$dir" "$PROJECT_DIR/$dir"
        echo "  Linked $PROJECT_DIR/$dir -> $DATA_DIR/$dir"
    fi
done

# === Step 6: Provision Python env via uv ===
echo ""
echo "=== Provisioning Python env (uv) ==="

if ! command -v uv >/dev/null 2>&1; then
    echo "uv not found; installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi
uv --version

if [ -f "$PROJECT_DIR/pyproject.toml" ]; then
    echo "Syncing dependencies from $PROJECT_DIR (honours uv.lock + .python-version)..."
    (cd "$PROJECT_DIR" && uv sync --frozen)
else
    echo "No pyproject.toml found in $PROJECT_DIR. Skipping dependency install."
fi

# === Done ===
echo ""
echo "=== Setup complete ==="
echo "Data disk: $DEVICE -> $DATA_MOUNT"
echo "Project data: $DATA_DIR"
echo "Symlinks:"
ls -la "$PROJECT_DIR/" | grep "^l" || echo "  (none)"
echo ""
echo "Disk usage:"
df -h "$DATA_MOUNT"
