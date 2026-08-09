# Agent-First Graph Migration

Status: ACTIVE
Owner: repository
Last verified: 2026-08-08

## Goal
Migrate the repository from a single tactical Python research package to an agent-legible graph-engineering system without changing live-trading authorization or claiming unverified trading performance.

## Non-goals
- Do not enable live order placement as part of this migration.
- Do not claim production readiness or verified out-of-sample profitability without evidence.
- Do not rewrite deterministic finance logic solely to fit an orchestration framework.

## Baseline
At the start of the Product Authority Alignment slice, `main` already contains the root `AGENTS.md`, canonical `CLAUDE.md` compatibility entry point, structured repository knowledge base, repository-contract CI, target architecture, and the quarantined `src/zero_dte_bot/` legacy module. The product purpose and definition of done were still distributed across mission, product-sense, research, and migration documents rather than codified as one canonical product contract. No graph runtime or target graph packages are implemented, live placement remains disabled, and verified OOS performance remains absent.

## Acceptance criteria
- short root `AGENTS.md` acts as table of contents;
- canonical product authority defines the user story, user experience, goal, desired state, and product definition of done;
- structured docs are repository system of record;
- knowledge-base structure, canonical product sections, and links are mechanically linted in CI;
- target architecture and legacy quarantine are explicit;
- later implementation adds structural import tests before moving graph code;
- no change weakens existing risk or promotion gates.

## Progress
- [x] Refactor monolithic AGENTS contract into progressive-disclosure map.
- [x] Add architecture, design, product, reliability, security, quality, reference, and plan docs.
- [x] Add repository-knowledge linter and generated repository map.
- [x] Add CI contract job.
- [x] Add Claude Code compatibility entry point without duplicating authoritative rules.
- [x] Codify canonical product authority and mechanically require its core sections.
- [ ] Add executable architecture dependency linter with package migration.
- [ ] Introduce typed graph schemas and Slate/Onyx program.
- [ ] Implement seven factor nodes and deterministic validator.

## Decisions
- Preserve deterministic Python finance code; orchestration does not justify a rewrite.
- Quarantine `src/zero_dte_bot/` as legacy until migrated.
- The top-level product contract governs subsystem research specs and execution plans.
- Human merge approval remains mandatory despite higher agent autonomy because this is a financial-risk repository.

## Verification
Run `python tools/lint_repo_knowledge.py`, `python tools/generate_repo_map.py --check`, and `pytest`.

## Risks
- Documentation and implementation can drift if repository-knowledge checks do not discover newly added governed documents.
- Product intent can drift if subsystem specifications or migration plans silently redefine the canonical product contract.
- Graph migration can accidentally weaken live-trading safety boundaries if legacy execution code is moved without explicit promotion gates.
- New orchestration dependencies can add complexity and cost without measurable reliability benefit.

## Next action
Implement the executable architecture dependency linter with structural package-boundary tests before adding graph runtime code.
