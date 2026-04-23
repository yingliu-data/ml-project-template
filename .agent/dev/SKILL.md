# <PROJECT_NAME> — Project Guide

## 1. Project Overview

<One-line description of what this project trains.>

## 2. Environment

- **Local:** `<LOCAL_PATH>`
- **Remote VMs:**
  - `<VM_NAME>.<ZONE>.<GCP_PROJECT>` → <GPU_TYPE> (`<MACHINE_TYPE>`)
  - *(Add more VMs as needed — different GPU configs for different workloads)*
- **Remote path:** `~/<PROJECT_NAME>/`
- **Sync (code):** Mutagen two-way (session: `<PROJECT_NAME>`)
- **Sync (outputs):** Mutagen one-way remote→local (session: `<PROJECT_NAME>-output`)
- Changes made locally or remotely are automatically synced.

---

## 3. Config System

4-tier YAML config (merged in order, later overrides earlier):

```
configs/default.yaml            <- Base: model arch, augmentation, viz settings
  | merge
configs/data/<dataset>.yaml     <- Dataset: paths, properties, format
  | merge
configs/feature/<method>.yaml   <- Features: preprocessing, extraction, reduction
  | merge
configs/train/<experiment>.yaml <- Experiment: run_id, hyperparams, references to data + feature
  = merged config
```

### Rules

- Every experiment gets its own `configs/train/<name>.yaml` with a unique `run_id`
- The `run_id` determines folder names: `checkpoints/<run_id>/`, `logs/training/<run_id>.log`
- Train configs reference data and feature configs by name (e.g., `data_config: coco2017`)
- Each `checkpoints/<run_id>/` is self-contained: weights, frozen config, results, and all visualizations
- A frozen `config_snapshot.yaml` is saved in `checkpoints/<run_id>/` at training time
- Use `_example.yaml` files as templates for new configs
- **Continuation runs** use `<experiment>_cont.yaml` (new checkpoint_path, different optimizer/LR, higher epoch count)

---

## 4. Development Workflow

### Develop

Make changes locally — Mutagen keeps code in sync.

- **Local editing:** edit files in `<LOCAL_PATH>`
- **Remote execution:** SSH into VM to run training with GPU
  ```bash
  gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT>
  cd ~/<PROJECT_NAME>
  ```

### Running Long Tasks on VM (tmux + auto-shutdown)

**IMPORTANT — Always use tmux so closing the local terminal does NOT interrupt the remote process.**

#### Option A: Interactive tmux (manual start)

```bash
gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT>
tmux new -s <session-name>
cd ~/<PROJECT_NAME>
<your-command> 2>&1 | tee logs/<category>/<logfile>.log && sudo shutdown -h now

# Detach: Ctrl+B then D (safe to close local terminal)
# Re-attach later: tmux attach -t <session-name>
```

#### Option B: One-liner (fire and forget)

```bash
gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> \
  --command="tmux new-session -d -s <session-name> 'cd ~/<PROJECT_NAME> && <your-command> 2>&1 | tee logs/<category>/<logfile>.log && sudo shutdown -h now'"
```

#### Option C: Use the wrapper script

```bash
bash <PACKAGE_NAME>/cloud/run_training.sh <config-name>
# e.g., bash <PACKAGE_NAME>/cloud/run_training.sh baseline_v1
```

#### Key Points

- `&& sudo shutdown -h now` auto-stops the VM (and GPU billing) when the command finishes
- `2>&1 | tee logs/<category>/<logfile>.log` saves output to the data disk for later review
- Closing the local terminal does NOT affect tmux — the process keeps running
- To check progress: `gcloud compute ssh ... --command="tail -20 logs/training/<run_id>.log"`
- To check if VM shut down: `gcloud compute instances describe <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> --format="value(status)"`

### Training Commands

```bash
# Train
python -m <PACKAGE_NAME>.training.train --config configs/train/<experiment>.yaml

# Resume from checkpoint
python -m <PACKAGE_NAME>.training.train --config configs/train/<experiment>.yaml --resume

# Continue from a previous run's best checkpoint (new config with different optimizer/LR)
python -m <PACKAGE_NAME>.training.train --config configs/train/<experiment>_cont.yaml

# Check if a run has converged (exit code 0 = converged, 1 = not converged)
python -m <PACKAGE_NAME>.training.check_convergence checkpoints/<run_id>

# Automated pipeline with convergence loop + auto-shutdown
bash <PACKAGE_NAME>/cloud/run_pipeline.sh <pipeline_name>
```

### Evaluation & Visualization

```bash
# Evaluate single dataset
python -m <PACKAGE_NAME>.training.evaluate \
    --config configs/train/<experiment>.yaml \
    --checkpoint checkpoints/<run_id>/weights/best.pt

# Cross-dataset evaluation (all datasets at once)
python -m <PACKAGE_NAME>.training.evaluate_all \
    --checkpoint checkpoints/<run_id>/weights/best.pt \
    --datasets <dataset1> <dataset2> <dataset3> \
    --batch 64

# Visualize predictions vs ground truth
python -m <PACKAGE_NAME>.training.visualize \
    --config configs/train/<experiment>.yaml \
    --checkpoint checkpoints/<run_id>/weights/best.pt \
    --num_samples 16

# Plot metrics (single run or comparison)
python -m <PACKAGE_NAME>.training.plot_metrics --run_dir checkpoints/<run_id>
python -m <PACKAGE_NAME>.training.plot_metrics --compare checkpoints/run1 checkpoints/run2
```

### Feature Engineering

```bash
tmux new -s feature
python -m <PACKAGE_NAME>.features.engineering --config configs/feature/<method>.yaml \
    2>&1 | tee logs/feature/<method>.log && sudo shutdown -h now
```

---

## 5. Cloud VM Setup

1. Run `<PACKAGE_NAME>/cloud/setup_vm.sh` on the VM (creates mount points, symlinks, installs deps)
2. Set up Mutagen sync (two sessions — see below)
3. Verify symlinks: `ls -la ~/<PROJECT_NAME>/ | grep "^l"`

### Disk Layout (Remote VM)

| Disk | Mount Point | Contents |
|------|------------|----------|
| Boot disk | `~/<PROJECT_NAME>/` | Python scripts, configs, small files (mutagen-synced) |
| Data disk (`<DISK_NAME>`) | `/mnt/data/` | `data/`, `checkpoints/`, `logs/` |

### Mutagen Sync Setup

```bash
# Session 1: Two-way sync (code + configs)
mutagen sync create --name=<PROJECT_NAME> --ignore-vcs \
  --ignore="data;checkpoints;logs;__pycache__;*.npy;*.npz;*.h5;*.keras;*.tflite;*.pt;*.pth;nohup.out;.DS_Store" \
  <LOCAL_PATH> <VM_NAME>.<ZONE>.<GCP_PROJECT>:~/<PROJECT_NAME>/

# Session 2: One-way sync (outputs: remote → local)
mutagen sync create --name=<PROJECT_NAME>-output \
  --mode=one-way-replica \
  --ignore="__pycache__;*.npy;*.npz;data/raw;data/processed;configs;<PACKAGE_NAME>;*.md;*.yml;*.yaml;.claude;.mutagen.yml" \
  <VM_NAME>.<ZONE>.<GCP_PROJECT>:~/<PROJECT_NAME>/ <LOCAL_PATH>/
```

**IMPORTANT:** When using multiple VMs, each needs its own Mutagen session name (e.g., `<PROJECT_NAME>-f`, `<PROJECT_NAME>-g`).

---

## 6. Documentation Workflow

### After every development session, update ALL of the following:

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview, setup instructions, how to run training/evaluation |
| `PROJECT_STRUCTURE.md` | Directory tree and description of every file/folder |
| `ASSETS.md` | Dataset locations (local and remote paths), model weights, checkpoints |
| `CHANGELOG.md` | What changed and when — new features, bug fixes, config changes |
| `TRAINLOG.md` | Training run log — hyperparams, dataset used, metrics, observations |

### Before Training (Planning)

1. Create experiment config in `configs/train/`
2. Add a **"Planned: Run N"** entry in `TRAINLOG.md` with goal, hypothesis, config references
3. Update `CHANGELOG.md` with any code changes made

### After Training (Recording)

`train.py` auto-generates inside `checkpoints/<run_id>/`:
- `weights/best.pt`, `weights/last.pt` — model checkpoints
- `config_snapshot.yaml` — frozen config
- `results.csv` — per-epoch metrics
- `training_metrics.png` — loss/metric curves
- `sample_{train,test}_{0,1,2}.png` — sample previews
- TRAINLOG.md entry — auto-appended with metrics

**Manually verify and update:**
- `TRAINLOG.md` — review auto-appended entry, add notes/observations
- `ASSETS.md` — add new checkpoint entry
- `CHANGELOG.md` — record any code changes
- `PROJECT_STRUCTURE.md` — if new files/folders were created

#### TRAINLOG.md format

```markdown
## Run <number> — <YYYY-MM-DD>

- **Config:** <config file used>
- **Dataset:** <dataset name and path>
- **Init weights:** <path to checkpoint this run started from>
- **Epochs:** <number> (best: <best_epoch>)
- **Batch size:** <number>
- **Optimizer:** <name> (lr=<value>)
- **Key metrics (best epoch):**
  - <Metric 1>: <value>
  - <Metric 2>: <value>
- **Duration:** <training time>
- **Checkpoint:** `checkpoints/<run_id>/`
- **VM:** <which VM this ran on>
- **Notes:** <observations, what worked, what to try next>
```

#### CHANGELOG.md format

```markdown
## <YYYY-MM-DD>

- <description of change>
```

---

## 7. Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|\
| Run ID | `<descriptive_name>` | `baseline_v1`, `lr_sweep_001` |
| Data config | `<dataset_name>.yaml` | `coco2017.yaml`, `custom_poses.yaml` |
| Feature config | `<method_name>.yaml` | `raw_normalized.yaml`, `pca_32d.yaml` |
| Train config | `<experiment_name>.yaml` | `baseline_v1.yaml`, `lr_sweep_001.yaml` |
| Continuation config | `<experiment>_cont.yaml` | `baseline_v1_cont.yaml` |
| Pipeline script | `run_<pipeline_name>.sh` | `run_pipeline.sh`, `run_generalist_pipeline.sh` |
| Log files | `<run_id>.log` | `baseline_v1.log` |

---

## 8. GPU Flexibility

### GPU Options (same zone)

| GPU | Machine Type | vRAM | Cost/hr | Use Case |
|-----|-------------|------|---------|----------|
| A100 40GB | `a2-highgpu-1g` | 40 GB | ~$3.67 | Large models, fast training |
| L4 | `g2-standard-4` | 24 GB | ~$0.70 | Good default for most training |
| T4 | `n1-standard-4` + accelerator | 16 GB | ~$0.35 | Budget option |
| None (CPU) | `e2-standard-4` | — | ~$0.13 | Data processing, feature engineering |

### Switching GPU (delete and recreate VM)

GCE does **not** allow changing the GPU on an existing VM. Delete and recreate. The data disk survives because `auto-delete=no`.

```bash
# === Step 1: Stop and delete old VM ===
gcloud compute instances stop <VM_NAME> \
  --zone=<ZONE> --project=<GCP_PROJECT>
gcloud compute instances delete <VM_NAME> \
  --zone=<ZONE> --project=<GCP_PROJECT> --quiet

# === Step 2: Create new VM with desired GPU ===

# L4 GPU (recommended default)
gcloud compute instances create <VM_NAME> \
  --zone=<ZONE> \
  --machine-type=g2-standard-4 \
  --accelerator=type=nvidia-l4,count=1 \
  --maintenance-policy=TERMINATE \
  --boot-disk-size=256GB \
  --boot-disk-type=pd-balanced \
  --image-family=ubuntu-minimal-2204-lts \
  --image-project=ubuntu-os-cloud \
  --disk=name=<DISK_NAME>,mode=rw,auto-delete=no \
  --project=<GCP_PROJECT>

# A100 GPU (single)
gcloud compute instances create <VM_NAME> \
  --zone=<ZONE> \
  --machine-type=a2-highgpu-1g \
  --accelerator=type=nvidia-tesla-a100,count=1 \
  --maintenance-policy=TERMINATE \
  --boot-disk-size=256GB \
  --boot-disk-type=pd-balanced \
  --image-family=ubuntu-minimal-2204-lts \
  --image-project=ubuntu-os-cloud \
  --disk=name=<DISK_NAME>,mode=rw,auto-delete=no \
  --project=<GCP_PROJECT>

# A100 GPU (multi — for DDP training)
gcloud compute instances create <VM_NAME> \
  --zone=<ZONE> \
  --machine-type=a2-highgpu-2g \
  --accelerator=type=nvidia-tesla-a100,count=2 \
  --maintenance-policy=TERMINATE \
  --boot-disk-size=256GB \
  --boot-disk-type=pd-balanced \
  --image-family=ubuntu-minimal-2204-lts \
  --image-project=ubuntu-os-cloud \
  --disk=name=<DISK_NAME>,mode=rw,auto-delete=no \
  --project=<GCP_PROJECT>

# CPU-only (data processing, no GPU cost)
gcloud compute instances create <VM_NAME> \
  --zone=<ZONE> \
  --machine-type=e2-standard-4 \
  --boot-disk-size=256GB \
  --boot-disk-type=pd-balanced \
  --image-family=ubuntu-minimal-2204-lts \
  --image-project=ubuntu-os-cloud \
  --disk=name=<DISK_NAME>,mode=rw,auto-delete=no \
  --project=<GCP_PROJECT>

# === Step 3: Post-creation setup ===

# Update SSH config (IP changes on each new VM)
gcloud compute config-ssh --project <GCP_PROJECT>

# Mount data disk (check device name first!)
gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> \
  --command="lsblk"

gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> \
  --command="sudo mkdir -p /mnt/data && sudo mount /dev/<DEVICE> /mnt/data && sudo chown \$USER:\$USER /mnt/data && echo '/dev/<DEVICE> /mnt/data ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab"

# Create symlinks
gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> \
  --command="mkdir -p ~/<PROJECT_NAME> && for dir in data checkpoints logs; do ln -sf /mnt/data/<PROJECT_NAME>/\$dir ~/<PROJECT_NAME>/\$dir; done && ls -la ~/<PROJECT_NAME>/ | grep '^l'"

# Recreate mutagen sync (old session points to dead VM)
mutagen sync terminate <PROJECT_NAME>
mutagen sync terminate <PROJECT_NAME>-output
# Re-run mutagen create commands from "Mutagen Sync Setup" section above
```

### Moving to a Different Zone

Data disk is zone-locked. To move zones:

```bash
# 1. Snapshot the data disk
gcloud compute disks snapshot <DISK_NAME> \
  --snapshot-names=<DISK_NAME>-snap \
  --zone=<ZONE> \
  --project=<GCP_PROJECT>

# 2. Create disk in new zone from snapshot
gcloud compute disks create <DISK_NAME> \
  --source-snapshot=<DISK_NAME>-snap \
  --size=<DISK_SIZE> --type=pd-balanced \
  --zone=<NEW_ZONE> \
  --project=<GCP_PROJECT>

# 3. Create new VM in new zone (use commands from "Switching GPU" above, change --zone)
# 4. Follow Step 3 post-creation setup
```

### Fallback Strategy (if GPU stockout)

1. Try switching GPU type in the same zone (keeps data disk)
2. Try other zones in the same region — data disk is zone-locked, requires snapshot + restore
3. **Always ask the user** before changing GPU type or zone — never decide automatically

---

## 9. Data Disk Management

### Create a New Data Disk

```bash
gcloud compute disks create <DISK_NAME> \
  --size=<DISK_SIZE> \
  --type=pd-balanced \
  --zone=<ZONE> \
  --project=<GCP_PROJECT> \
  --description="Training data for <PROJECT_NAME>"
```

### Attach / Detach

```bash
# Attach
gcloud compute instances attach-disk <VM_NAME> \
  --disk=<DISK_NAME> \
  --zone=<ZONE> \
  --project=<GCP_PROJECT>

# Detach (VM must be stopped)
gcloud compute instances stop <VM_NAME> --zone=<ZONE> --project=<GCP_PROJECT>
gcloud compute instances detach-disk <VM_NAME> \
  --disk=<DISK_NAME> \
  --zone=<ZONE> \
  --project=<GCP_PROJECT>
```

### Resize

```bash
gcloud compute disks resize <DISK_NAME> \
  --size=<NEW_SIZE> \
  --zone=<ZONE> \
  --project=<GCP_PROJECT>
```

---

## 10. Checklists

### Pre-Session

- [ ] GCloud auth is valid. If expired, ask the user to run `gcloud auth login`.
- [ ] Mutagen sync is running (`mutagen sync list` — check sessions are active)
- [ ] VM is running (`gcloud compute instances describe <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> --format="value(status)"`)
- [ ] If VM fails to start due to GPU stockout, always ask the user whether to try a different zone/GPU or wait. Never decide automatically.

### Post-Session

- [ ] `README.md` is up to date
- [ ] `PROJECT_STRUCTURE.md` reflects current file structure
- [ ] `ASSETS.md` lists all dataset and checkpoint paths
- [ ] `CHANGELOG.md` has entries for today's changes
- [ ] `TRAINLOG.md` has entries for any training runs completed

---

## 11. Useful Commands

```bash
# Check mutagen sync status
mutagen sync list

# Pause/resume sync
mutagen sync pause <PROJECT_NAME>
mutagen sync resume <PROJECT_NAME>

# SSH into VM
gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT>

# Check VM status
gcloud compute instances describe <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> --format="value(status)"

# List all running instances
gcloud compute instances list --project <GCP_PROJECT> --filter="status=RUNNING"

# Start/stop VM
gcloud compute instances start <VM_NAME> --zone <ZONE> --project <GCP_PROJECT>
gcloud compute instances stop <VM_NAME> --zone <ZONE> --project <GCP_PROJECT>

# Check GPU usage on VM
gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> \
  --command="nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader"

# Check disk usage on data disk
gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> --command="df -h /mnt/data"

# Tail training log remotely
gcloud compute ssh <VM_NAME> --zone <ZONE> --project <GCP_PROJECT> \
  --command="tail -50 ~/<PROJECT_NAME>/logs/training/<run_id>.log"
```

---

## 12. Project Lifecycle

```
1. Plan    → Write TRAINLOG "Planned" entry + create configs
2. Train   → Run on VM with tmux + auto-shutdown
3. Review  → Check auto-generated plots + metrics
4. Record  → Update TRAINLOG, ASSETS, CHANGELOG
5. Iterate → Plan next run based on observations
```

---

## Self-Updating Rule

Update this document whenever the workflow, VM setup, or project conventions change.
