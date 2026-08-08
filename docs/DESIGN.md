# Design

Status: ACTIVE
Owner: repository
Last verified: 2026-08-08

Design principle: make the repository easy for a fresh agent to inspect, reason about, validate, and change without hidden organizational knowledge.

Mandatory design invariants:
- typed data at external and graph boundaries;
- explicit dependency direction from `ARCHITECTURE.md`;
- deterministic finance logic separated from generative orchestration;
- structured, queryable logs for long-running/runtime work;
- bounded retries and explicit terminal failure states;
- no hidden defaults on financial critical paths;
- small modules and named contracts over implicit conventions;
- remediation-oriented linter/test failures.

When a rule repeatedly appears in reviews, encode it in code, schema, lint, or test rather than adding more prose to `AGENTS.md`.
