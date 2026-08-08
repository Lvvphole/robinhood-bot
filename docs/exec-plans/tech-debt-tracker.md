# Technical Debt Tracker

Status: ACTIVE
Owner: repository
Last verified: 2026-08-08

| ID | Gap | Severity | Evidence | Next action |
|---|---|---:|---|---|
| TD-001 | Legacy package is not yet layered to target architecture | HIGH | repository tree | build structural import linter, then migrate by slice |
| TD-002 | Slate/Onyx graph program not yet versioned | HIGH | repository tree | add typed program after architecture linter |
| TD-003 | Seven factor nodes not implemented | HIGH | repository tree | implement only after contracts/data specification |
| TD-004 | Agent-legible local logs/metrics/traces not yet present | MEDIUM | repository tree | design isolated observability stack |
| TD-005 | No verified synchronized historical option-chain dataset | HIGH | `STATUS.md` | acquire/validate point-in-time data before performance claims |
