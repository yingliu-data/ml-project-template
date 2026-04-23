from typing import Sequence

import numpy as np


class KeypointToHeatmap:
    """Encode keypoints (frame, joint, xyz) as Gaussian 3D heatmaps.

    Output shape: (frame, joint, *heatmap_shape).
    """

    def __init__(
        self,
        heatmap_shape: Sequence[int] = (20, 20, 18),
        axis_range: int = 32767,
        sigma: float = 0.2,
        mu: float = 1e-4,
    ):
        self.heatmap_shape = np.array(heatmap_shape)
        y, x, z = [np.linspace(0.0, 1.0, int(heatmap_shape[i])) for i in range(3)]
        self.pos_xyz = np.meshgrid(x, y, z)
        self.axis_range = axis_range
        self.sigma = sigma
        self.mu = mu

    def __call__(self, keypoints: np.ndarray) -> np.ndarray:
        frame_num, joint_num = keypoints.shape[:2]
        heatmap = np.zeros((frame_num, joint_num, *self.heatmap_shape))
        keypoints = self._normalise(keypoints)

        for i in range(frame_num):
            for k in range(joint_num):
                dis = np.sqrt(
                    np.sum([(self.pos_xyz[j] - keypoints[i, k, j]) ** 2 for j in range(3)], axis=0)
                )
                g = self._gaussian(dis)
                heatmap[i, k] = self._softmax(g)
        return heatmap

    def _gaussian(self, dis: np.ndarray) -> np.ndarray:
        return (1.0 / (self.sigma * np.sqrt(2 * np.pi))) * np.exp(-((dis - self.mu) ** 2) / (2 * self.sigma ** 2))

    @staticmethod
    def _softmax(data: np.ndarray) -> np.ndarray:
        e = np.exp(data - data.max())
        return e / e.sum()

    def _normalise(self, data: np.ndarray) -> np.ndarray:
        resolution = [self.axis_range * 2 / self.heatmap_shape[i] for i in range(3)]
        data = np.divide((data + self.axis_range), resolution)
        return np.divide(data.astype(int), self.heatmap_shape - 1)
