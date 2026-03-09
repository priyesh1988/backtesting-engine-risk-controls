from __future__ import annotations

import argparse

from .config import BacktestConfig
from .data import load_price_data
from .engine import run_backtest
from .strategies import MeanReversionZScore, MovingAverageCrossover


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run a backtest with risk controls")
    p.add_argument("--csv", required=True)
    p.add_argument("--strategy", choices=["ma_crossover", "mean_reversion"], required=True)
    p.add_argument("--fast", type=int, default=5)
    p.add_argument("--slow", type=int, default=20)
    p.add_argument("--window", type=int, default=10)
    p.add_argument("--z-entry", type=float, default=-1.2)
    p.add_argument("--z-exit", type=float, default=0.0)
    p.add_argument("--initial-cash", type=float, default=100000)
    p.add_argument("--risk-per-trade", type=float, default=0.01)
    p.add_argument("--stop-loss", type=float, default=0.03)
    p.add_argument("--take-profit", type=float, default=0.06)
    p.add_argument("--max-hold-days", type=int, default=10)
    p.add_argument("--max-positions", type=int, default=1)
    p.add_argument("--kill-switch-dd", type=float, default=0.08)
    return p


def main() -> None:
    args = build_parser().parse_args()
    df = load_price_data(args.csv)
    if args.strategy == "ma_crossover":
        strategy = MovingAverageCrossover(fast=args.fast, slow=args.slow)
    else:
        strategy = MeanReversionZScore(window=args.window, z_entry=args.z_entry, z_exit=args.z_exit)

    cfg = BacktestConfig(
        initial_cash=args.initial_cash,
        risk_per_trade=args.risk_per_trade,
        stop_loss=args.stop_loss,
        take_profit=args.take_profit,
        max_hold_days=args.max_hold_days,
        max_positions=args.max_positions,
        kill_switch_dd=args.kill_switch_dd,
    )
    result = run_backtest(df, strategy, cfg)
    s = result.summary
    print("========== Backtest Summary ==========")
    print(f"Final equity: {s['final_equity']:.2f}")
    print(f"Total return: {s['total_return_pct']:.2f}%")
    print(f"CAGR: {s['cagr_pct']:.2f}%")
    print(f"Sharpe: {s['sharpe']}")
    print(f"Max drawdown: {s['max_drawdown_pct']:.2f}%")
    print(f"Trades: {s['trades']}")
    print(f"Win rate: {s['win_rate']:.2f}%")
    print(f"Avg win: {s['avg_win']:.2f}%")
    print(f"Avg loss: {s['avg_loss']:.2f}%")
    print(f"Kill switch triggered: {s['kill_switch_triggered']}")
    print("======================================")


if __name__ == "__main__":
    main()
