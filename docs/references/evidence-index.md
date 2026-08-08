# Evidence Index

Status: ACTIVE
Owner: repository
Last verified: 2026-08-08

Evidence classes:
`PEER_REVIEWED_PRIMARY`, `OFFICIAL_RUNTIME_OR_BROKER_DOC`, `PRACTICE_REPORT`, `PREPRINT`, `THESIS`, `INSTITUTIONAL_WHITEPAPER`, `BOOK_OR_SECONDARY`, `PROJECT_DECISION`, `VERIFIED_REPOSITORY_EVIDENCE`, `VERIFIED_MARKET_DATA_RESULT`.

Do not upgrade a source class in prose. Preprints, theses, vendor practice reports, and project decisions are not peer-reviewed ground truth.

## Harness engineering
- *Harness engineering: leveraging Codex in an agent-first world* — `PRACTICE_REPORT`. Governs the repository-engineering operating model adopted here: humans steer/agents execute, progressive disclosure, repository knowledge as system of record, agent legibility, mechanical architecture/docs enforcement, agent-to-agent review loops, and continuous garbage collection.

## Multi-factor foundations
- Sharpe (1964), market equilibrium/beta — `PEER_REVIEWED_PRIMARY`.
- Fama & French (1993), size/value — `PEER_REVIEWED_PRIMARY`.
- Jegadeesh & Titman (1993), momentum — `PEER_REVIEWED_PRIMARY`.
- Ang et al. (2006), volatility/expected returns — `PEER_REVIEWED_PRIMARY`.
- Novy-Marx (2013), gross profitability — `PEER_REVIEWED_PRIMARY`.
- Fama & French (2015), profitability/investment — `PEER_REVIEWED_PRIMARY`.
- Harvey, Liu & Zhu (2016), multiple-testing/factor-zoo caution — `PEER_REVIEWED_PRIMARY`.
- Hou, Xue & Zhang (2020), anomaly replication — `PEER_REVIEWED_PRIMARY`.

## Graph / agent research
- ReAct (ICLR 2023), Generative Agents (UIST 2023), Graph of Thoughts (AAAI 2024), MetaGPT (ICLR 2024), AgentVerse (ICLR 2024) — classify by publication record.
- AGAO / attention orchestration and graph-native reasoning uploaded to this project remain `PREPRINT` unless publication status is independently verified.
