import pandas as pd

from backtester.config import BacktestConfig
from backtester.engine import run_backtest


class AlwaysLongThenHold:
    def signal(self, df, i, in_position):
        if not in_position and i == 0:
            return 1
        return 0


class EnterThenExit:
    def signal(self, df, i, in_position):
        if not in_position and i == 0:
            return 1
        if in_position and i == 2:
            return -1
        return 0


def test_engine_take_profit_exit():
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "open": [100, 101, 102],
            "high": [100, 110, 103],
            "low": [99, 100, 101],
            "close": [100, 105, 102],
            "volume": [1000, 1000, 1000],
        }
    )
    cfg = BacktestConfig(stop_loss=0.02, take_profit=0.05, max_hold_days=5)
    result = run_backtest(df, AlwaysLongThenHold(), cfg)
    assert len(result.trades) == 1
    assert result.trades[0].exit_reason == "take_profit"


def test_engine_signal_exit():
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]),
            "open": [100, 100, 100, 100],
            "high": [101, 101, 101, 101],
            "low": [99, 99, 99, 99],
            "close": [100, 101, 102, 103],
            "volume": [1000, 1000, 1000, 1000],
        }
    )
    cfg = BacktestConfig(stop_loss=0.1, take_profit=0.5, max_hold_days=10)
    result = run_backtest(df, EnterThenExit(), cfg)
    assert len(result.trades) == 1
    assert result.trades[0].exit_reason == "signal_exit"


def test_engine_kill_switch_triggers():
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "open": [100, 100],
            "high": [100, 100],
            "low": [100, 50],
            "close": [100, 50],
            "volume": [1000, 1000],
        }
    )
    cfg = BacktestConfig(risk_per_trade=1.0, stop_loss=0.8, take_profit=0.5, kill_switch_dd=0.10)
    result = run_backtest(df, AlwaysLongThenHold(), cfg)
    assert result.kill_switch_triggered is True
