import pytest

from backtester.risk import drawdown, position_size


def test_position_size_basic():
    qty = position_size(cash=100000, entry_price=100, stop_loss_pct=0.02, risk_per_trade=0.01)
    assert qty == 500


def test_position_size_affordability_cap():
    qty = position_size(cash=1000, entry_price=600, stop_loss_pct=0.01, risk_per_trade=1.0)
    assert qty == 1


def test_position_size_bad_entry():
    with pytest.raises(ValueError):
        position_size(1000, 0, 0.02, 0.01)


def test_drawdown_basic():
    assert round(drawdown(90, 100), 4) == -0.1
