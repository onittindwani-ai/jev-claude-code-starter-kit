# Jev Claude Code Starter Kit

**Set up Jev in 5 minutes. See it work in 60 seconds. Put it to work in your AI sales system by tonight.**

Jev is a model from TypeSafe AI that does not write text. It answers typed questions (which option, how much, yes or
no) with a probability, in a fraction of a second, for a fraction of a cent. That is exactly what an AI sales system
needs for its hundreds of small daily decisions: is this reply interested, which team, should this message go out.

This kit gives you EVERYTHING in one place so you never have to figure it out alone:

- the setup guide, a checklist, and a prompt that makes Claude Code or Codex set it all up for you;
- a prompt that makes your AI test Jev and show you what happens;
- a tested client, a 300 reply test built to be hard (150 confusing hand written replies, 90 real inbox style ones, 60 easy ones) with a scoreboard, break tests, and a cost calculator;
- 10 ready made decision sets for sales, support and safety (reply triage, lead fit, call outcomes, guardrails, more);
- a Claude Code skill, commands and a CLAUDE.md or AGENTS.md snippet so your AI uses Jev wherever it fits;
- 5 working examples (reply router, lead scoring, call outcome router, guardrail before sending, morning review list);
- guides: when to use Jev, honest limits, security, cost, patterns, rollout plan, troubleshooting, prompt library.

It works offline with a built in fake Jev, so you can learn the whole kit before you spend a cent.

## Start here (the 3 minute path)

1. Open `00-SETUP-JEV.md` and follow the 12 steps (account, 5 dollars of credit, API key).
2. Open this folder in Claude Code or Codex and paste the prompt from `02-SETUP-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md`.
3. In YOUR terminal (never in the AI chat) run the command it prints, with your key:
   `export TYPESAFE_API_KEY="your-key"` then `python3 tools/jev_check.py`
4. Paste the prompt from `03-TEST-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md` and watch Jev work.

## What is inside

| Path | What it is |
| --- | --- |
| `00-SETUP-JEV.md` | Step by step setup, from the typesafe.ai page to your first answer |
| `01-SETUP-CHECKLIST.md` | A tick box list: nothing forgotten |
| `02-SETUP-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md` | The prompt that sets up everything from your AI's side and prints your exact command |
| `03-TEST-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md` | A full prompt that tests Jev for you and explains the results |
| `04-GO-LIVE-PROMPTS.md` | Prompts that build Jev into YOUR real sales system |
| `tools/` | The client (`jev.py`), smoke test, reply triage, 300 reply test, break tests, question runner, cost calculator, mock server |
| `data/` | 300 made up replies with answers, 10 sample replies, break test cases |
| `templates/questions/` | 10 ready made decision sets in JSON |
| `templates/claude-code/` | A skill, 3 commands and a CLAUDE.md snippet |
| `templates/codex/` | An AGENTS.md snippet |
| `examples/` | 5 working examples that never send anything |
| `docs/` | Guides: when to use, limits, security, cost, patterns, rollout, troubleshooting, glossary, sources |

## Honest limits

- This is an independent kit, not made or endorsed by TypeSafe AI. Jev can be wrong, and its confidence is not the same
  as being right. Test on your own data before you trust it, and keep a person or a rule in front of risky actions.
- Prices, versions and features change fast. Everything here was checked on 2026-10-23; see `docs/FACTS-AND-SOURCES.md`.
- The test replies are made up. 150 are deliberately confusing, but your real inbox will still surprise you. Test your own replies too.
- Never put your API key in chat, screenshots, videos or git. See `docs/SECURITY-AND-DATA.md`.

Now open `00-SETUP-JEV.md`. Your first answer from Jev is about 5 minutes away.
