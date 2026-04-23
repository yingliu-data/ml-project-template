import numpy as np

from PACKAGE_NAME.postprocessing.heatmap_decoder import HeatmapToKeypoint
from PACKAGE_NAME.preprocessing.heatmap_encoder import KeypointToHeatmap


def test_shapes_match_config():
    enc = KeypointToHeatmap(heatmap_shape=(12, 12, 10), axis_range=32767)
    kp = np.zeros((2, 3, 3), dtype=np.int32)
    hm = enc(kp)
    assert hm.shape == (2, 3, 12, 12, 10)


def test_encode_decode_recovers_centered_keypoint():
    shape = (24, 24, 24)
    enc = KeypointToHeatmap(heatmap_shape=shape, axis_range=32767, sigma=0.15)
    dec = HeatmapToKeypoint(axis_range=32767)

    kp = np.array([[[0, 0, 0]]], dtype=np.int32)
    hm = enc(kp)
    recovered = dec(hm, heatmap_shape=shape)

    assert recovered.shape == kp.shape
    assert np.max(np.abs(recovered - kp)) < 2000


def test_softmax_output_sums_to_one():
    enc = KeypointToHeatmap(heatmap_shape=(8, 8, 8))
    kp = np.array([[[100, 200, 300]]], dtype=np.int32)
    hm = enc(kp)
    assert np.allclose(hm.sum(axis=(-1, -2, -3)), 1.0, atol=1e-5)
