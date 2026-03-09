import pytest

from backtester.config import BacktestConfig


def test_config_validates_ok():
    BacktestConfig().validate()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"initial_cash": 0},
        {"risk_per_trade": 0},
        {"stop_loss": 1},
        {"take_profit": 0},
        {"max_hold_days": 0},
        {"max_positions": 0},
        {"kill_switch_dd": 1},
    ],
)
def test_config_invalid(kwargs):
    with pytest.raises(ValueError):
        BacktestConfig(**kwargs).validate()
