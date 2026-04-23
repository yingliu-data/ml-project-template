from typing import Callable, Iterable

import torch


def train_one_epoch(
    model: torch.nn.Module,
    dataloader: Iterable,
    optimizer: torch.optim.Optimizer,
    loss_fn: Callable,
    device: torch.device,
) -> float:
    model.train()
    total_loss = 0.0
    n_batches = 0
    for batch in dataloader:
        inputs, labels = batch
        optimizer.zero_grad()
        outputs = model(inputs.to(device))
        loss = loss_fn(outputs, labels.to(device))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        n_batches += 1
    return total_loss / max(n_batches, 1)


@torch.no_grad()
def evaluate_one_epoch(
    model: torch.nn.Module,
    dataloader: Iterable,
    loss_fn: Callable,
    device: torch.device,
) -> float:
    model.eval()
    total_loss = 0.0
    n_batches = 0
    for batch in dataloader:
        inputs, labels = batch
        outputs = model(inputs.to(device))
        loss = loss_fn(outputs, labels.to(device))
        total_loss += loss.item()
        n_batches += 1
    return total_loss / max(n_batches, 1)
