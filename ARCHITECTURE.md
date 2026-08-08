# Architecture

Status: TARGET_WITH_LEGACY_COMPATIBILITY
Owner: repository
Last verified: 2026-08-08

## Purpose
This is the top-level architecture map. Detailed design rationale lives in `docs/design-docs/`.

## System shape

```text
Slate/Onyx orchestration
        |
        v
factor graph + coordination state
        |
        v
deterministic Python finance services
        |
        v
validation -> portfolio -> risk
        |
        v
research/paper execution boundary -> broker providers
```

The graph coordinates work; it does not replace deterministic numerical finance logic.

## Canonical graph

```text
orchestrator
  -> market_beta
  -> size
  -> value
  -> momentum
  -> profitability
  -> investment
  -> low_volatility
  -> sync
  -> validator
  -> regime_auditor
  -> portfolio_constructor
  -> risk_decomposer
  -> research_or_paper_gate
  -> state_commit_and_observability
  -> next_cycle
```

Factor nodes may execute in parallel only when current-cycle inputs are independent. `sync` is an explicit barrier. Required failures fail closed unless a tested degraded-mode contract exists.

## Layer rule
Target domain packages follow one forward dependency direction:

```text
contracts/types -> config -> repositories -> services -> runtime -> interfaces
                       ^          ^
                       |          |
                    providers ----+
```

- `contracts/types`: schemas, enums, immutable DTOs.
- `config`: typed/versioned policy and strategy configuration.
- `repositories`: point-in-time data access and persistence abstractions.
- `services`: deterministic factor, validation, portfolio, risk, and accounting logic.
- `runtime`: Slate/Onyx graph bindings, scheduling, retries, checkpoints, budgets.
- `interfaces`: CLI/reporting/operator surfaces.
- `providers`: the only boundary for broker, market-data, clock, model, and observability implementations.

Cross-domain imports that bypass this direction are prohibited. External systems enter through providers, never directly from factor or portfolio logic.

## Legacy boundary
`src/zero_dte_bot/` is the current tactical research module. It is quarantined as legacy until migrated by execution plan. Do not add new graph architecture inside it except safety fixes required to preserve behavior.

## Financial authority boundary
Generative agents can produce hypotheses and advisory artifacts. Final factor values, portfolio weights, position sizing, risk vetoes, promotion, and order placement are deterministic state transitions with typed evidence.

## Change rule
New nodes, edges, providers, strategy definitions, risk limits, or dependency exceptions require a design record/ADR plus executable structural tests.
