import torch
from torch.utils.data import DataLoader

from PACKAGE_NAME.training.callbacks import EarlyStopping
from PACKAGE_NAME.training.train_loop import evaluate_one_epoch, train_one_epoch


def test_two_epoch_training_run(synthetic_tensor_dataset):
    model = torch.nn.Sequential(torch.nn.Linear(8, 16), torch.nn.ReLU(), torch.nn.Linear(16, 2))
    loader = DataLoader(synthetic_tensor_dataset, batch_size=8, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)
    loss_fn = torch.nn.MSELoss()
    device = torch.device("cpu")
    early = EarlyStopping(patience=5, min_delta=0.0)

    losses = []
    for _ in range(2):
        train_loss = train_one_epoch(model, loader, optimizer, loss_fn, device)
        val_loss = evaluate_one_epoch(model, loader, loss_fn, device)
        assert train_loss == train_loss  # not NaN
        assert val_loss == val_loss
        losses.append(train_loss)
        early(val_loss)

    assert len(losses) == 2
    assert all(l >= 0 for l in losses)
