import pandas as pd

from backtester.strategies import MeanReversionZScore, MovingAverageCrossover


def test_ma_crossover_entry_signal():
    df = pd.DataFrame({"close": [1, 2, 3, 4, 5, 6]})
    strat = MovingAverageCrossover(fast=2, slow=4)
    assert strat.signal(df, 5, False) == 1


def test_mean_reversion_entry_or_hold():
    df = pd.DataFrame({"close": [10, 10, 10, 10, 8]})
    strat = MeanReversionZScore(window=5, z_entry=-1.0, z_exit=0.0)
    assert strat.signal(df, 4, False) in (0, 1)
