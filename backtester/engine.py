from __future__ import annotations

import pandas as pd

from .config import BacktestConfig
from .metrics import cagr, max_drawdown, sharpe_ratio, summarize_trades
from .models import BacktestResult, Position, Trade
from .risk import drawdown, position_size


def run_backtest(df: pd.DataFrame, strategy, config: BacktestConfig) -> BacktestResult:
    config.validate()

    cash = config.initial_cash
    peak_equity = cash
    equity_curve: list[float] = []
    trades: list[Trade] = []
    position: Position | None = None
    kill_switch_triggered = False

    for i, row in df.iterrows():
        date = row["date"]
        open_p, high_p, low_p, close_p = float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"])

        # exits first
        if position is not None:
            exit_price = None
            reason = None
            if low_p <= position.stop_price:
                exit_price = position.stop_price
                reason = "stop_loss"
            elif high_p >= position.take_profit_price:
                exit_price = position.take_profit_price
                reason = "take_profit"
            elif i >= position.max_exit_index:
                exit_price = close_p
                reason = "max_hold"
            else:
                sig = strategy.signal(df, i, True)
                if sig == -1:
                    exit_price = close_p
                    reason = "signal_exit"

            if exit_price is not None:
                gross = position.qty * exit_price
                pnl = (exit_price - position.entry_price) * position.qty - config.fee_per_trade
                cash += gross - config.fee_per_trade
                trades.append(
                    Trade(
                        entry_date=str(position.entry_date),
                        exit_date=str(date.date()),
                        entry_price=position.entry_price,
                        exit_price=exit_price,
                        qty=position.qty,
                        pnl=pnl,
                        pnl_pct=((exit_price - position.entry_price) / position.entry_price) * 100,
                        exit_reason=reason,
                    )
                )
                position = None

        # entries second
        if position is None and not kill_switch_triggered:
            sig = strategy.signal(df, i, False)
            if sig == 1:
                qty = position_size(cash, close_p, config.stop_loss, config.risk_per_trade)
                if qty > 0:
                    cost = qty * close_p + config.fee_per_trade
                    if cost <= cash:
                        cash -= cost
                        position = Position(
                            entry_date=str(date.date()),
                            entry_price=close_p,
                            qty=qty,
                            stop_price=close_p * (1 - config.stop_loss),
                            take_profit_price=close_p * (1 + config.take_profit),
                            max_exit_index=i + config.max_hold_days,
                        )

        equity = cash + (position.qty * close_p if position is not None else 0.0)
        equity_curve.append(equity)
        peak_equity = max(peak_equity, equity)

        if drawdown(equity, peak_equity) <= -config.kill_switch_dd:
            kill_switch_triggered = True
            if position is not None:
                exit_price = close_p
                pnl = (exit_price - position.entry_price) * position.qty - config.fee_per_trade
                cash += position.qty * exit_price - config.fee_per_trade
                trades.append(
                    Trade(
                        entry_date=str(position.entry_date),
                        exit_date=str(date.date()),
                        entry_price=position.entry_price,
                        exit_price=exit_price,
                        qty=position.qty,
                        pnl=pnl,
                        pnl_pct=((exit_price - position.entry_price) / position.entry_price) * 100,
                        exit_reason="kill_switch",
                    )
                )
                position = None
            break

    final_equity = cash + (position.qty * float(df.iloc[-1]["close"]) if position is not None else 0.0)
    trade_stats = summarize_trades(trades)
    summary = {
        "final_equity": round(final_equity, 2),
        "total_return_pct": round(((final_equity / config.initial_cash) - 1) * 100, 2),
        "cagr_pct": round(cagr(config.initial_cash, final_equity, len(equity_curve)) * 100, 2),
        "sharpe": round(sharpe_ratio(equity_curve), 4) if sharpe_ratio(equity_curve) is not None else None,
        "max_drawdown_pct": round(max_drawdown(equity_curve) * 100, 2),
        **trade_stats,
        "kill_switch_triggered": kill_switch_triggered,
    }
    return BacktestResult(
        equity_curve=equity_curve,
        trades=trades,
        final_equity=final_equity,
        kill_switch_triggered=kill_switch_triggered,
        summary=summary,
    )
