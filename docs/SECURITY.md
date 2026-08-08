# Security and Execution Authority

Status: ACTIVE
Owner: repository
Last verified: 2026-08-08

- Never commit API keys, broker credentials, tokens, account identifiers, or private user data.
- Secrets enter only through approved environment/secret-management boundaries and are never written to logs or plans.
- Broker and market-data SDK/tool shapes are parsed at the boundary; do not guess response fields.
- Order review and order placement are separate capabilities.
- Live order placement is disabled until explicit promotion; human approval remains mandatory while the project contract requires it.
- Before any future placement: stale-signal check, position reconciliation, duplicate-order guard, buying-power check, hard risk check, broker pre-trade review, approval gate, order construction, and post-order reconciliation.
- Agents and retries may not widen permissions, bypass review, or lower risk controls.
