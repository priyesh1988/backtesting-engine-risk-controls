from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BacktestConfig:
    initial_cash: float = 100_000.0
    risk_per_trade: float = 0.01
    stop_loss: float = 0.03
    take_profit: float = 0.06
    max_hold_days: int = 10
    max_positions: int = 1
    kill_switch_dd: float = 0.08
    fee_per_trade: float = 0.0

    def validate(self) -> None:
        if self.initial_cash <= 0:
            raise ValueError("initial_cash must be positive")
        if not 0 < self.risk_per_trade <= 1:
            raise ValueError("risk_per_trade must be in (0, 1]")
        if not 0 < self.stop_loss < 1:
            raise ValueError("stop_loss must be in (0, 1)")
        if self.take_profit <= 0:
            raise ValueError("take_profit must be positive")
        if self.max_hold_days < 1:
            raise ValueError("max_hold_days must be >= 1")
        if self.max_positions < 1:
            raise ValueError("max_positions must be >= 1")
        if not 0 < self.kill_switch_dd < 1:
            raise ValueError("kill_switch_dd must be in (0, 1)")
