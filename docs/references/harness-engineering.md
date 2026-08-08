# Harness Engineering Practice Report Notes

Status: SOURCE_SUMMARY
Owner: repository
Last verified: 2026-08-08

Source: *Harness engineering: leveraging Codex in an agent-first world*.
Classification: `PRACTICE_REPORT`.

Repository rules derived from the source:
- humans specify intent and validate outcomes; agents implement and maintain artifacts;
- work depth-first by adding missing capabilities and scaffolding;
- make code, docs, logs, metrics, traces, and runtime behavior directly legible to agents;
- keep root instructions small and use a structured repository knowledge base;
- use progressive disclosure and versioned execution plans;
- mechanically validate knowledge structure, freshness, links, architecture, and taste invariants;
- favor strict architectural boundaries with local implementation autonomy;
- encode review feedback into guardrails so judgment compounds;
- use agent-to-agent review/feedback loops and escalate only when human judgment is required;
- continuously garbage-collect drift and technical debt.

Project adaptation: trading safety, promotion, and human live-order/merge authority remain stricter than the practice report where required by this repository contract.
