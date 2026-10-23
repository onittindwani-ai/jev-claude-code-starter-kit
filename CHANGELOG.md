# Changelog

## 1.1.0 (2026-10-24)
- The 300 reply test set is now realistic and hard: 150 hand written confusing replies (sarcasm, mixed intent, redirects that
  sound interested, legal and privacy requests, one word answers needing context, quoted threads, other languages, requests
  buried in long messages), 90 real inbox style replies (quoted emails, long signatures, legal footers, mobile signatures, typos),
  and 60 easy ones. Every reply has a difficulty, tags and an optional acceptable second label. See `data/LABELING-GUIDE.md`.
- The reply type definitions now carry the decision rules (stop beats everything, a redirect beats interest, and so on).
- `run_test.py` also reports lenient accuracy, accuracy by difficulty, the weakest tags and the most dangerous mistakes
  (wrong with the highest confidence). New break tests (hidden instruction in a polite decline, double negative, buried demo request).
- A harder 10 reply sample. 18 tests.

## 1.0.0 (2026-10-23)
- First release: setup guide, checklist, setup prompt, test prompt, go live prompts; a dependency free client, smoke test,
  reply triage, 300 reply test with calibration, break tests, question runner, cost calculator and a mock server;
  10 decision sets; a Claude Code skill, 3 commands and CLAUDE.md or AGENTS.md snippets; 5 examples; guides.
- Checked against Jev 1.13 and the docs on 2026-10-23.
