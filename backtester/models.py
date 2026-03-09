from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Position:
    entry_date: str
    entry_price: float
    qty: int
    stop_price: float
    take_profit_price: float
    max_exit_index: int


@dataclass
class Trade:
    entry_date: str
    exit_date: str
    entry_price: float
    exit_price: float
    qty: int
    pnl: float
    pnl_pct: float
    exit_reason: str


@dataclass
class BacktestResult:
    equity_curve: list[float]
    trades: list[Trade]
    final_equity: float
    kill_switch_triggered: bool
    summary: dict[str, float | int | bool | None]
