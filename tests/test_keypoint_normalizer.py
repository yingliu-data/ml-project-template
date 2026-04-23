import numpy as np

from PACKAGE_NAME.preprocessing.keypoint_normalizer import KeypointNormalizer


def test_scaling_ratio():
    n = KeypointNormalizer(axis_range=3000, source_range=1500.0)
    assert n.ratio == 2.0


def test_normalise_denormalise_roundtrip(rng):
    n = KeypointNormalizer(axis_range=32767, source_range=1500.0)
    raw = rng.uniform(-1500, 1500, size=(4, 3)).astype(np.float64)
    norm = n.normalise(raw)
    back = n.denormalise(norm.astype(np.float64))
    assert np.allclose(back, raw, atol=1.0)


def test_nan_inf_are_replaced():
    n = KeypointNormalizer()
    raw = np.array([[np.nan, np.inf, -np.inf]])
    out = n.normalise(raw)
    assert np.all(np.isfinite(out))
