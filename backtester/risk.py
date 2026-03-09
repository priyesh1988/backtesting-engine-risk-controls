from __future__ import annotations

import math


def position_size(cash: float, entry_price: float, stop_loss_pct: float, risk_per_trade: float) -> int:
    if entry_price <= 0:
        raise ValueError("entry_price must be positive")
    if not 0 < stop_loss_pct < 1:
        raise ValueError("stop_loss_pct must be in (0,1)")
    if not 0 < risk_per_trade <= 1:
        raise ValueError("risk_per_trade must be in (0,1]")

    risk_budget = cash * risk_per_trade
    per_share_risk = entry_price * stop_loss_pct
    qty = math.floor(risk_budget / per_share_risk)
    max_affordable = math.floor(cash / entry_price)
    return max(0, min(qty, max_affordable))


def drawdown(current_equity: float, peak_equity: float) -> float:
    if peak_equity <= 0:
        raise ValueError("peak_equity must be positive")
    return (current_equity - peak_equity) / peak_equity
