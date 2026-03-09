from backtester.metrics import cagr, max_drawdown, sharpe_ratio


def test_max_drawdown():
    assert round(max_drawdown([100, 120, 90, 110]), 4) == -0.25


def test_sharpe_none_for_flat_series():
    assert sharpe_ratio([100, 100, 100]) is None


def test_cagr_positive():
    assert cagr(100, 110, 252) > 0
