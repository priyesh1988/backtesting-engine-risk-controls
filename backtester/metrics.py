from __future__ import annotations

import math
from typing import Sequence

from .models import Trade


def max_drawdown(equity_curve: Sequence[float]) -> float:
    if not equity_curve:
        return 0.0
    peak = equity_curve[0]
    worst = 0.0
    for x in equity_curve:
        peak = max(peak, x)
        dd = (x - peak) / peak
        worst = min(worst, dd)
    return worst


def sharpe_ratio(equity_curve: Sequence[float]) -> float | None:
    if len(equity_curve) < 2:
        return None
    rets = []
    for prev, cur in zip(equity_curve[:-1], equity_curve[1:]):
        if prev == 0:
            continue
        rets.append((cur - prev) / prev)
    if len(rets) < 2:
        return None
    mean = sum(rets) / len(rets)
    var = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
    std = math.sqrt(var)
    if std == 0:
        return None
    return (mean / std) * math.sqrt(252)


def cagr(initial_equity: float, final_equity: float, periods: int) -> float:
    if periods < 2 or initial_equity <= 0:
        return 0.0
    years = periods / 252
    if years <= 0:
        return 0.0
    return (final_equity / initial_equity) ** (1 / years) - 1


def summarize_trades(trades: Sequence[Trade]) -> dict[str, float | int]:
    if not trades:
        return {"trades": 0, "win_rate": 0.0, "avg_win": 0.0, "avg_loss": 0.0}
    wins = [t.pnl_pct for t in trades if t.pnl > 0]
    losses = [t.pnl_pct for t in trades if t.pnl <= 0]
    return {
        "trades": len(trades),
        "win_rate": (len(wins) / len(trades)) * 100,
        "avg_win": sum(wins) / len(wins) if wins else 0.0,
        "avg_loss": sum(losses) / len(losses) if losses else 0.0,
    }
