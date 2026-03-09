# Backtesting Engine with Risk Controls

Backtesting engine for systematic strategy research with practical risk controls.

## Features
- Event-driven portfolio simulation over OHLCV CSV data
- Pluggable strategies
- Risk controls:
  - stop loss
  - take profit
  - max holding period
  - max concurrent positions
  - per-trade risk cap
  - daily drawdown kill switch
- Metrics:
  - total return
  - CAGR
  - Sharpe ratio
  - max drawdown
  - win rate
  - average win / loss
- CLI runner
- Full unit tests
- GitHub Actions CI

## Repo structure

```
backtesting-engine-risk-controls/
├── backtester/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── data.py
│   ├── engine.py
│   ├── metrics.py
│   ├── models.py
│   ├── risk.py
│   └── strategies.py
├── tests/
├── examples/
├── .github/workflows/
├── pyproject.toml
└── README.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Input data format

CSV columns required:

```text
date,open,high,low,close,volume
```

Example:

```csv
date,open,high,low,close,volume
2024-01-01,100,101,99,100.5,100000
2024-01-02,100.5,102,100,101.7,110000
```

## How to use

### 1) Run the moving average crossover example

```bash
python -m backtester.cli \
  --csv examples/sample_prices.csv \
  --strategy ma_crossover \
  --fast 5 \
  --slow 20 \
  --initial-cash 100000 \
  --risk-per-trade 0.01 \
  --stop-loss 0.03 \
  --take-profit 0.06 \
  --max-hold-days 10 \
  --max-positions 1 \
  --kill-switch-dd 0.08
```

### 2) Run the mean reversion example

```bash
python -m backtester.cli \
  --csv examples/sample_prices.csv \
  --strategy mean_reversion \
  --window 10 \
  --z-entry -1.2 \
  --z-exit 0.0 \
  --initial-cash 100000 \
  --risk-per-trade 0.01 \
  --stop-loss 0.02 \
  --take-profit 0.04 \
  --max-hold-days 7 \
  --max-positions 1 \
  --kill-switch-dd 0.06
```

## Example output

```text
========== Backtest Summary ==========
Final equity: 104235.82
Total return: 4.24%
CAGR: 10.96%
Sharpe: 1.18
Max drawdown: -3.12%
Trades: 12
Win rate: 58.33%
Avg win: 1.94%
Avg loss: -1.02%
Kill switch triggered: False
======================================
```

## Strategy interface

Each strategy returns one of:
- `1` for long entry signal
- `0` for hold / no action
- `-1` for exit signal

The engine applies position sizing and risk logic.

## Running tests

```bash
pytest -q
```

## Successful scenario

Use trending sample data with:
- `ma_crossover`
- moderate stop loss
- wider take profit
- max holding period >= trend duration

Expected result:
- several entries
- controlled losses
- positive return if trend persists

## Unsuccessful scenario

Use choppy sideways data with:
- tight stop loss
- slow crossover
- low max holding period

Expected result:
- frequent whipsaws
- lower win rate
- possible kill switch trigger if drawdown threshold is tight

## License

All Rights Reserved.
