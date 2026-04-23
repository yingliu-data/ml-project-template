import numpy as np


class KeypointNormalizer:
    """Normalize/denormalize keypoints into a configurable axis range.

    Input data assumed in shape (..., xyz) with values in arbitrary physical units.
    Configured `axis_range` defines the target symmetric range [-axis_range, axis_range].
    """

    def __init__(self, axis_range: int = 32767, source_range: float = 1500.0):
        self.axis_range = axis_range
        self.source_range = source_range
        self.ratio = axis_range / source_range

    def normalise(self, data: np.ndarray) -> np.ndarray:
        out = data.astype(np.float64) * self.ratio
        out = np.where(np.isfinite(out), out, 0.0)
        if self.ratio >= 1:
            out = out.astype(np.int32)
        return out

    def denormalise(self, data: np.ndarray) -> np.ndarray:
        return data.astype(np.float64) / self.ratio
