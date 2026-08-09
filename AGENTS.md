# AGENTS.md

## Authority
This file is the small, stable entry point for agents working in this repository.
It is a map, not the repository encyclopedia. Repository-local docs, schemas, tests, plans, and generated artifacts are the system of record.

Authority for claims and actions:
`legal/broker/exchange constraints → verified market data → executable tests/replay → locked config/schemas → repo docs/code → reviewed research → model output`.
No model output is authoritative by itself.

## Mission
Build and maintain a research-only, agent-first graph-engineered investment decision platform that turns point-in-time market evidence into governed, reproducible portfolio proposals while remaining risk-bounded and economical in human attention.
Humans steer: define intent, acceptance criteria, priorities, and approvals. Agents execute: design, implement, test, review, document, and maintain repository artifacts.

## Start Here
Read only what the task needs, in this order:
1. `ARCHITECTURE.md` — domain map, dependency directions, graph/runtime boundaries.
2. `docs/design-docs/index.md` — design records and verification status.
3. `docs/product-specs/investment-decision-platform.md` — canonical user story, user experience, goal, desired state, and product definition of done.
4. `docs/product-specs/index.md` — subordinate product and research contracts.
5. `docs/PLANS.md` — planning rules and active execution plans.
6. `docs/RELIABILITY.md` — determinism, data integrity, testing, risk, replay.
7. `docs/SECURITY.md` — secrets, broker permissions, live-order boundary.
8. `docs/QUALITY_SCORE.md` — current gaps and quality grades.
9. `docs/references/evidence-index.md` — evidence classes and research sources.

Use progressive disclosure. Do not load the whole knowledge base unless the task requires it.

## Current State
- Repository status: `research_only`.
- Current validated average daily P&L: `0.0 USD/trading_day`; no verified OOS result exists.
- Existing `src/zero_dte_bot/` is a legacy tactical research module and remains safety-constrained.
- Target orchestration: Slate/Onyx graph programs plus deterministic Python finance code.
- Live order placement remains disabled until separate promotion and human approval.

## Canonical Graph
`orchestrator → {market_beta,size,value,momentum,profitability,investment,low_volatility} → sync → validator → regime_auditor → portfolio_constructor → risk_decomposer → research/paper gate → state/observability`.
Nodes are bounded workers or deterministic units. Edges are typed data hand-offs. Barriers, retries, budgets, checkpoints, cancellation, and escalation are explicit.

## Financial Authority Boundary
Agents may research, propose, explain, and write code. Agents may not directly set final factor values, portfolio weights, position sizes, risk overrides, promotion state, or live orders.
Financially consequential transitions require deterministic validation and typed configuration.
`model proposes → deterministic verifier decides → risk vetoes/constrains → human/promotion policy authorizes`.

## Hard Safety Rules
No naked short options, undefined risk, overnight 0DTE holdings, martingale, averaging down, revenge logic, lookahead, future quote/fundamental matching, optimistic fills, or silent constraint relaxation.
Missing/failed required inputs fail closed unless a pre-approved degraded mode exists.
Risk limits cannot be overridden by an LLM, optimizer, retry loop, or profit target.

## Engineering Workflow
Direct writes to `main` are prohibited.
`contract → baseline → plan → implement → test → verify evidence → review → PR → human merge`.
Complex work requires a checked-in execution plan under `docs/exec-plans/active/`; move it to `completed/` only with verification evidence.
When an agent fails, do not "try harder" blindly. Identify the missing capability, rule, tool, or context and make it repository-legible and mechanically enforceable.

## Repository Knowledge Rules
- Durable project knowledge belongs in the repository, not chat, memory, or private scratchpads.
- Keep `AGENTS.md` short; deeper rules belong in the linked docs.
- `CLAUDE.md` is the Claude Code compatibility entry point and must import `AGENTS.md`; shared repository rules must not be duplicated there.
- Update docs in the same PR when behavior, architecture, constraints, or operating assumptions change.
- Promote repeated review feedback into documentation, tests, linters, schemas, or tooling.
- Generated docs must be regenerated, not hand-edited.

## Architecture Rules
Follow `ARCHITECTURE.md`. Enforce boundaries centrally and allow implementation freedom locally.
New graph nodes, dependencies, broker capabilities, data sources, or strategy definitions require an ADR/design record and tests.
Prefer inspectable, composable dependencies; opaque behavior must be wrapped behind typed providers or replaced with a smaller legible implementation when justified.

## Validation Commands
Run before proposing completion:
`python tools/lint_repo_knowledge.py`
`python tools/lint_architecture.py`
`python tools/generate_repo_map.py --check`
`pytest`
Release-critical warnings are errors.

## Review Loop
Self-review locally, request independent agent review, address feedback, rerun validation, and repeat until clean.
For every Codex review finding that is fixed, reply in the same review thread with the implemented fix and verification evidence, then resolve that thread. A Codex fix is not complete until both actions are done.
Escalate to a human for judgment, policy, live-trading authorization, or unresolved safety ambiguity.

## Stop Rule
Stop and report on: insufficient data, invariant failure, point-in-time integrity failure, risk limit, budget limit, execution failure, rejected gate, or user termination.
Never manufacture progress by turning missing evidence into a positive assumption.
