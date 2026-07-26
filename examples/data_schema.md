# Historical data contract

## Underlying bars

Required columns:

`timestamp, open, high, low, close, volume`

Optional: `vwap`. Timestamps must be timezone-aware or UTC-compatible. The baseline assumes 5-minute SPY bars.

## Option quote snapshots

Required columns:

`timestamp, expiration, strike, right, bid, ask, last, volume, open_interest, implied_volatility, delta, gamma, theta, vega`

Optional: `symbol`.

The backtest requires contemporaneous bid/ask snapshots for every candidate contract. Last-trade-only data is rejected because it cannot model spread cost, stale prints, or realistic fills.
