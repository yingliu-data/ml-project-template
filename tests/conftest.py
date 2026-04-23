import numpy as np
import pytest


@pytest.fixture
def rng():
    return np.random.default_rng(0)


@pytest.fixture
def synthetic_keypoints(rng):
    """(frame=4, joints=3, xyz=3) keypoints within [-32767, 32767]."""
    return rng.integers(-32767, 32767, size=(4, 3, 3)).astype(np.int32)


@pytest.fixture
def synthetic_tensor_dataset():
    """Small PyTorch TensorDataset for training-loop smoke tests."""
    import torch
    from torch.utils.data import TensorDataset

    x = torch.randn(32, 8)
    y = torch.randn(32, 2)
    return TensorDataset(x, y)
