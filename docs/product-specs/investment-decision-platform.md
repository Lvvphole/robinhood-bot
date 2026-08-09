# Investment Decision Platform

Status: RESEARCH_ONLY
Owner: repository
Last verified: 2026-08-08

## Authority
This is the canonical top-level product contract for the repository. Subsystem specifications, architecture documents, execution plans, and implementation details may refine how the product is built but may not redefine this user story, goal, desired state, or definition of done unless this contract is explicitly amended through the governed review process.

Numeric strategy targets and factor-specific objectives are subordinate research criteria. They do not replace the product North Star.

## User Story
As a systematic investor or portfolio operator, I want to provide an investment objective, universe, benchmark, horizon, capital allocation, and risk constraints and receive a portfolio recommendation that combines multiple independent sources of return, explains why each position exists, quantifies its risks, and can be reproduced from evidence, so I can make better investment decisions without manually coordinating models, datasets, research workflows, and broker-specific tooling.

## User Experience
The user interacts with one investment intelligence system, not with individual factor agents, graph-runtime internals, Python modules, or broker APIs.

The user defines the mandate and constraints. The system acquires point-in-time evidence, evaluates eligible research dimensions, validates outputs, assesses regime context, constructs a constrained portfolio, decomposes its risk, and presents a governed proposal with evidence, uncertainty, provenance, rejected alternatives where material, and the next required authorization action.

The user must be able to inspect why the proposal exists, what evidence supported or rejected it, what risks it creates, and what would prevent promotion. Implementation details remain observable for engineering and audit purposes without becoming the primary product experience.

## Goal
Produce economically useful, evidence-backed investment decisions that improve risk-adjusted outcomes relative to the declared benchmark after real costs, while controlling model risk, point-in-time data integrity, concentration, turnover, transaction costs, execution risk, failure modes, and system cost.

This is a research objective, not a performance promise. The goal is not to maximize raw return, maximize win rate, maximize agent activity, use a particular model, preserve a fixed factor count, or trade through a particular broker.

## North Star
Turn diverse market evidence into governed, reproducible portfolio decisions that earn superior risk-adjusted outcomes after real costs.

## Desired State
A broker-independent, model-agnostic, graph-orchestrated systematic investment platform in which specialized research capabilities discover and evaluate opportunities while deterministic controls govern data integrity, portfolio construction, risk, promotion, and execution authority.

The system continuously measures which factors, workflows, models, and allocations deserve continued use based on validated evidence rather than narrative confidence. Broker, model, orchestration, and data implementations remain replaceable providers behind explicit boundaries.

## Definition of Done
The first production-capable release is done only when a user can move from investment mandate to validated evidence to factor or signal research to regime assessment to portfolio proposal to risk decomposition to approval or promotion decision to a reproducible paper/live-ready artifact through one governed workflow, with objective evidence for all of the following:

1. The investment contract is explicit and versioned: universe, benchmark, horizon, rebalance frequency, capital, risk limits, turnover limits, transaction-cost assumptions, and promotion criteria are machine-readable.
2. Point-in-time data integrity is proven: no lookahead, survivorship leakage, future fundamentals, future quote matching, optimistic fills, or silently missing required inputs.
3. The factor layer is operational: market beta, size, value, momentum, profitability, investment, and low-volatility research produce typed, independently testable outputs, and the architecture can add or remove factors without redefining the product contract.
4. The graph workflow is executable end to end with explicit dependencies, synchronization, failure, timeout, retry, budget, checkpoint, cancellation, and escalation behavior.
5. Financial authority remains deterministic where consequence matters: generative models may propose research or explanations but cannot directly override factor acceptance, portfolio weights, position sizing, risk constraints, promotion state, or execution permission.
6. Risk is visible before capital exposure: concentration, factor exposure, volatility, drawdown sensitivity, correlation, liquidity, turnover, transaction costs, and relevant scenario or stress risks are quantified.
7. Research survives chronological out-of-sample evaluation with declared baselines, real costs, appropriate multiple-testing controls, and robustness testing before promotion.
8. Prospective paper operation demonstrates the complete workflow for a predeclared incubation period without future information and produces replayable operational evidence.
9. Every decision is auditable and reproducible from versioned inputs, configuration, code, evidence, and deterministic state transitions.
10. Failure containment is demonstrated for missing or stale data, model failure, factor disagreement, invalid outputs, risk violations, provider outages, and orchestration failures; required failures fail closed unless an approved degraded mode exists.
11. Economics are measured: data, model, compute, orchestration, latency, human-review, turnover, and execution costs are tracked against the incremental value created by each capability.
12. Broker independence is demonstrated: replacing a broker provider does not require redesigning research, portfolio construction, validation, or risk logic.
13. Human authority remains explicit for capital-bearing promotion and live-trading authorization until a separately governed policy changes that boundary.
14. The product is understandable without knowledge of its internals: the primary user view communicates mandate, evidence, portfolio, risk, uncertainty, provenance, and required action rather than graph plumbing or agent transcripts.
15. The integrated system has measured evidence that it is better than the simpler baseline it replaces on at least one justified dimension such as correctness, risk-adjusted performance, failure containment, human effort, or economic efficiency without violating mandatory safety and reliability constraints.

## Non-goals
- Do not define the product as an autonomous trader, chatbot, broker bot, fixed seven-factor strategy, or specific orchestration framework.
- Do not treat Robinhood, Slate/Onyx, any model provider, or any current implementation dependency as the product identity.
- Do not claim alpha, production readiness, or live-trading readiness from backtest evidence alone.
- Do not add complexity, agents, controls, or dependencies unless their expected benefit justifies their latency, cost, context, and failure surface.
- Do not weaken deterministic financial authority, point-in-time integrity, risk limits, or human promotion gates to improve apparent performance.

## Success Measures
Success thresholds must be predeclared in versioned research or promotion specifications before evaluation. The product-level measurement set includes:

- benchmark-relative net risk-adjusted performance after modeled and realized costs;
- drawdown, concentration, liquidity, turnover, and risk-limit adherence;
- point-in-time data-integrity violations and prevented leakage defects;
- reproducibility and replay success rate;
- prospective paper/shadow reliability and failure-containment behavior;
- total data, model, compute, orchestration, execution, latency, and human-review cost;
- incremental benefit versus declared simpler baselines and previous promoted candidates.

## System Lifecycle
`investment mandate → point-in-time evidence → independent research/factor intelligence → validation → regime context → portfolio construction → risk decomposition → human/promotion gate → paper/live execution boundary → realized evidence → evaluate → adapt → repeat`
