from pathlib import Path

import pytest

from backtester.data import load_price_data


def test_load_price_data_ok(tmp_path: Path):
    p = tmp_path / "prices.csv"
    p.write_text("date,open,high,low,close,volume\n2024-01-01,100,101,99,100,1000\n")
    df = load_price_data(str(p))
    assert list(df.columns) == ["date", "open", "high", "low", "close", "volume"]
    assert len(df) == 1


def test_load_price_data_missing_cols(tmp_path: Path):
    p = tmp_path / "bad.csv"
    p.write_text("date,open,close\n2024-01-01,100,100\n")
    with pytest.raises(ValueError):
        load_price_data(str(p))
