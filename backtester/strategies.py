from __future__ import annotations

import numpy as np
import pandas as pd


class MovingAverageCrossover:
    def __init__(self, fast: int = 5, slow: int = 20):
        if fast < 1 or slow < 2 or fast >= slow:
            raise ValueError("require 1 <= fast < slow")
        self.fast = fast
        self.slow = slow

    def signal(self, df: pd.DataFrame, i: int, in_position: bool) -> int:
        if i < self.slow - 1:
            return 0
        closes = df["close"]
        fast_ma = closes.iloc[i - self.fast + 1 : i + 1].mean()
        slow_ma = closes.iloc[i - self.slow + 1 : i + 1].mean()
        if not in_position and fast_ma > slow_ma:
            return 1
        if in_position and fast_ma < slow_ma:
            return -1
        return 0


class MeanReversionZScore:
    def __init__(self, window: int = 10, z_entry: float = -1.2, z_exit: float = 0.0):
        if window < 2:
            raise ValueError("window must be >= 2")
        self.window = window
        self.z_entry = z_entry
        self.z_exit = z_exit

    def signal(self, df: pd.DataFrame, i: int, in_position: bool) -> int:
        if i < self.window - 1:
            return 0
        series = df["close"].iloc[i - self.window + 1 : i + 1]
        mean = series.mean()
        std = series.std(ddof=0)
        if std == 0 or np.isnan(std):
            return 0
        z = (series.iloc[-1] - mean) / std
        if not in_position and z <= self.z_entry:
            return 1
        if in_position and z >= self.z_exit:
            return -1
        return 0
