# Core Beliefs

Status: ACTIVE
Owner: repository
Last verified: 2026-08-08

1. Humans steer; agents execute repository changes.
2. Human attention is scarce. Make the system observable and directly legible to agents.
3. Repository-local, versioned artifacts are the system of record. Context that is not discoverable in-repo effectively does not exist for an agent run.
4. Give agents a map, not a monolithic manual. Use progressive disclosure from `AGENTS.md` into focused documents.
5. When an agent fails, add the missing capability, tool, rule, or context instead of escalating prompt pressure.
6. Enforce invariants, not implementation taste. Boundaries, correctness, reproducibility, and safety are centralized; local expression remains flexible.
7. Promote repeated review feedback into executable guardrails.
8. Prefer legible, composable, stable dependencies. Wrap opaque upstream behavior behind typed providers.
9. Technical debt compounds. Continuously scan, grade, and remove drift in small increments.
10. Financial evidence outranks fluent reasoning. Models propose; deterministic verification and risk controls decide.
11. Capital preservation and verified expectancy override profit targets.
12. No claim of strategy success exists without point-in-time, cost-aware, chronological out-of-sample evidence.

Source adaptation: these operating principles apply the attached Harness Engineering practice report to this repository while retaining stricter trading-safety and human-approval requirements.
