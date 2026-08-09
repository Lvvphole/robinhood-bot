# Quality Score

Status: BASELINE
Owner: repository
Last verified: 2026-08-09

Grades represent repository evidence, not intent.

| Domain | Grade | Evidence / gap |
|---|---|---|
| Agent entrypoint / progressive disclosure | A | `AGENTS.md` + canonical `CLAUDE.md` import are landed and CI-enforced |
| Knowledge-base structure | A- | structured docs + linter + weekly drift detector; autonomous fix-up PR agent not yet integrated |
| Architecture legibility | A- | target layers documented; executable import linter and structural regression tests enforce package boundaries |
| Graph runtime | D | Slate/Onyx program absent |
| Factor implementations | D | seven-factor nodes absent |
| Deterministic legacy research code | B | existing package/tests; migration not complete |
| Point-in-time research data | D | required synchronized historical dataset absent |
| Risk / live-order containment | B+ | live placement disabled; target broker boundary documented |
| Agent-legible observability | D | no isolated logs/metrics/traces stack yet |
| Verified OOS trading performance | F / NOT VERIFIED | no verified OOS result |

Update this file when evidence changes. A grade increase requires a linked test, artifact, or verified result.
