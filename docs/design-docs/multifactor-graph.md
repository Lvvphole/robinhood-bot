# Multi-Factor Graph Design

Status: TARGET
Owner: repository
Last verified: 2026-08-08

## Problem
The system must manage three interacting constraints: long-horizon execution, strategic-versus-tactical reasoning, and bounded working memory. The graph makes coordination explicit rather than re-implementing glue logic per task.

## Nodes and edges
Nodes are specialized agents or deterministic computation units. Edges carry typed, versioned artifacts. The required factor set is market beta, size, value, momentum, profitability, investment, and low volatility.

Factor nodes never emit orders or portfolio weights. Each emits a typed factor artifact with provenance, as-of time, configuration/code/data hashes, normalization, and quality flags.

## Coordination states
Required node terminal states are `VALID`, `NOT_APPLICABLE`, `REJECTED_DATA`, or `FAILED`. Missing output is not neutral output. Retries are bounded and only valid for retryable failure classes.

## Strategic and tactical state
Strategic state includes definitions, universe, benchmark, topology, risk budgets, optimizer constraints, promotion gates, and evidence registry. It changes only through reviewed repository changes.

Tactical state includes current observations, exposures, positions, regime state, candidate portfolio, risk state, and broker/account state. Tactical state cannot rewrite strategic policy during the same evaluation period.

## Memory
Durable evidence lives in versioned/persistent artifacts. Agent context is bounded and disposable. Store decisions, reason codes, typed outputs, summaries, and evidence references; do not treat private chain-of-thought as financial evidence.

## Runtime
Slate/Onyx owns scheduling, dependency waits, parallelism, retries, checkpoints, budgets, cancellation, and escalation. Python owns deterministic numerical finance and risk-critical calculations.
