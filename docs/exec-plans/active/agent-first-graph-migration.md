# Agent-First Graph Migration

Status: ACTIVE
Owner: repository
Last verified: 2026-08-08

## Goal
Migrate the repository from a single tactical Python research package to an agent-legible graph-engineering system without changing live-trading authorization or claiming unverified trading performance.

## Baseline
Current `main` contains a small `src/zero_dte_bot/` package, baseline config, examples, and tests. No root `AGENTS.md`, structured knowledge base, graph runtime, or graph packages are present. Live placement is disabled and verified OOS performance is absent.

## Acceptance criteria
- short root `AGENTS.md` acts as table of contents;
- structured docs are repository system of record;
- knowledge-base structure and links are mechanically linted in CI;
- target architecture and legacy quarantine are explicit;
- later implementation adds structural import tests before moving graph code;
- no change weakens existing risk or promotion gates.

## Progress
- [x] Refactor monolithic AGENTS contract into progressive-disclosure map.
- [x] Add architecture, design, product, reliability, security, quality, reference, and plan docs.
- [x] Add repository-knowledge linter and generated repository map.
- [x] Add CI contract job.
- [ ] Add executable architecture dependency linter with package migration.
- [ ] Introduce typed graph schemas and Slate/Onyx program.
- [ ] Implement seven factor nodes and deterministic validator.

## Decisions
- Preserve deterministic Python finance code; orchestration does not justify a rewrite.
- Quarantine `src/zero_dte_bot/` as legacy until migrated.
- Human merge approval remains mandatory despite higher agent autonomy because this is a financial-risk repository.

## Verification
Run `python tools/lint_repo_knowledge.py`, `python tools/generate_repo_map.py --check`, and `pytest`.

## Next action
Land this repository-contract scaffold on a feature branch, obtain independent review, then implement the structural dependency linter before adding graph runtime code.
