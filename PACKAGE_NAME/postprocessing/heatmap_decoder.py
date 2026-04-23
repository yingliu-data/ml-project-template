from typing import Sequence

import numpy as np


class HeatmapToKeypoint:
    """Decode 3D Gaussian heatmaps back into keypoints via expected-value over the grid.

    Input shape: (frame, joint, *heatmap_shape).
    Output shape: (frame, joint, xyz) scaled back to [-axis_range, axis_range].
    """

    def __init__(self, axis_range: int = 32767):
        self.axis_range = axis_range

    def __call__(self, heatmap: np.ndarray, heatmap_shape: Sequence[int] = (20, 20, 18)) -> np.ndarray:
        pos_xyz = np.meshgrid(*[np.linspace(0.0, 1.0, int(heatmap_shape[i])) for i in range(3)])
        hm = np.reshape(heatmap, (*heatmap.shape[:-3], *heatmap_shape))

        eps = 1e-6
        expected_xyz = [
            np.sum(pos_xyz[i].reshape(1, -1) * hm.reshape(*hm.shape[:-3], -1), axis=-1)
            / (np.sum(hm.reshape(*hm.shape[:-3], -1), axis=-1) + eps)
            for i in range(3)
        ]
        expected_xyz = np.stack(expected_xyz, axis=-1)
        return (expected_xyz * self.axis_range * 2 - self.axis_range).astype(np.int32)
