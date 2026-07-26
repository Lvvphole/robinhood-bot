# Deterministic execution state

## Contract

- Measurement mode: native numeric
- Unit: USD per trading day
- Target direction: increase
- Baseline value: 0.0
- Minimum target value: 200.0
- Preferred upper target: 400.0
- Gap value: 200.0

## Baseline

No historical option-chain quote dataset was supplied. Current validated average daily P&L is therefore 0.0, not an estimate of future performance.

## Single strategy hypothesis

SPY 0DTE opening-range momentum using long calls or puts. Entries require opening-range breakout, VWAP alignment, EMA alignment, momentum, volume confirmation, same-day expiration, 0.35-0.55 absolute delta, and strict spread/liquidity filters.

## Risk shape

- Long premium only in v0.1
- Full premium used for capital-at-risk sizing
- Maximum two trades per day
- No averaging down
- No overnight holdings
- Daily loss cap
- 15:30 ET hard exit
- Live order placement disabled

## Verification evidence

- Unit and smoke tests: 6 passed
- Configuration relational invariants: passed
- Floating-point tolerance acceptance test: passed
- Floating-point rejection test: passed
- Python compile check: passed

## Evaluation

Engineering milestone is complete. Trading-performance milestone is not started because synchronized historical SPY and option-chain bid/ask data is absent.

## Next executable step

Load at least two years of synchronized 5-minute SPY bars and chain-wide 0DTE option quote snapshots, run chronological walk-forward tests, correct for multiple testing, run daily-P&L Monte Carlo, and begin paper incubation only if all robustness gates pass.
