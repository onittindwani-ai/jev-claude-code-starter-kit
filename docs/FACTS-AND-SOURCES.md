# Facts and sources (checked 2026-10-23, re check before you rely on them)

| Fact | Source |
| --- | --- |
| Jev is TypeSafe's first public System One model; it returns typed decisions with probabilities | https://typesafe.ai and https://docs.typesafe.ai/introduction |
| Question types: Choice, Score, Noul (and Box for images in 1.14) | https://docs.typesafe.ai/introduction |
| API: `POST https://api.typesafe.ai/v1/systemone`, Bearer key, body `state`, `model`, `questions` | https://docs.typesafe.ai/introduction/quickstart.md |
| SDKs: `pip install typesafe-sdk` (Python 3.10+), `npm install @typesafe-ai/sdk` (Node 20+) | same quick start page |
| Claude Code plugin: `claude plugin marketplace add typesafe-ai/skills` then `claude plugin install typesafe@typesafe-ai`; others: `npx skills add typesafe-ai/skills --skill typesafe-ai` | quick start page and the console home Quickstart box |
| Price $42 per billion input tokens, output free | https://typesafe.ai (cost section) |
| 193.6x faster and 444.6x cheaper (TypeSafe's own tests) | https://typesafe.ai |
| Limits: 32 MiB body, depth 64, status codes 400, 401, 413, 415, 422, 429, 529 | https://docs.typesafe.ai/api/errors.md |
| Known weak spots of Jev 1.13 | https://docs.typesafe.ai/model-jaggedness/jev-1.13.md |
| Patterns and cookbooks | https://docs.typesafe.ai/patterns.md and https://docs.typesafe.ai/cookbooks.md |
| Jev 1.14 (14 to 15 Oct 2026): Box type, images (opt in), longer context | secondary coverage, for example https://www.marktechpost.com/2026/10/14/typesafe-ai-jev-1-14-images-box-long-context/ |
| The console needs credit before an API key can be created | observed in a real account on 2026-10-23 |

This kit is independent and not affiliated with TypeSafe AI.
