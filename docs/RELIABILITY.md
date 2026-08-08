# Reliability

Status: ACTIVE
Owner: repository
Last verified: 2026-08-08

## Determinism
Pinned code/config/data/prompt hashes, seeded randomness, stable ordering, explicit tie-breaks, bounded numeric tolerance, and integer-cents/Decimal monetary accounting are required for critical calculations.

## Data integrity
Raw data is immutable. All research is point-in-time: no future quotes, future fundamentals, current constituents projected backward, silent restatement leakage, duplicates, unsorted observations, stale required inputs, or non-finite values.

## Graph execution
Every long-running workflow has a goal, step/retry/budget limits, checkpoint, cancellation semantics, idempotency policy, replay identifier, and typed terminal failure. Retry only when the failure class is retryable. A risk failure is never retried to evade the limit.

## Validation
The sync barrier never interprets missing output as neutral. The deterministic validator checks schema, as-of alignment, freshness, universe/version consistency, hashes, normalization, sample sufficiency, duplicates, and replay.

## Portfolio and risk
Optimization constraints are explicit and never silently relaxed. Risk has veto authority over alpha objectives and model recommendations. Costs, liquidity, turnover, concentration, beta/factor exposures, drawdown state, and options Greeks when applicable are measured before promotion.

## Research
Use chronological walk-forward/OOS evaluation, multiple-testing control, realistic fills/costs, sensitivity analysis, and robustness/Monte Carlo where appropriate. No post-test tuning while preserving the OOS label.

## Agent-legible observability target
Long-running graph/runtime work must expose structured logs, metrics, traces, state transitions, budgets, retries, validation failures, and risk vetoes through repository-documented query paths. Worktree/task isolation is preferred so an agent can reproduce and validate a change without polluting another run.
