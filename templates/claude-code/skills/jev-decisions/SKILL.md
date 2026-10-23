---
name: jev-decisions
description: Use Jev (TypeSafe's System One model) for fast, cheap, structured decisions inside software: routing, classifying, scoring and yes or no checks, with confidence gates and a person in the loop. Use whenever code you are writing needs a judgment call about text, such as sorting replies, scoring leads, checking a draft before sending, or detecting stop requests. Not for writing text or code.
---

# Jev decisions

## What Jev is (2026-10-23)
A hosted model that does not write text. You send 1 `state` (text or JSON) and named questions; it returns for each a
choice (with probabilities), a score on levels you define, or a noul (yes or no as 0 to 1), plus a confidence.
Endpoint `POST https://api.typesafe.ai/v1/systemone`. Price: $0.042 per million input tokens, output free (re check
typesafe.ai). Official docs: docs.typesafe.ai. TypeSafe also publishes its own skill (`typesafe-ai`); use it for API
details and this skill for the decision design rules below.

## When to use Jev
- Routing a message to 1 of a fixed set of destinations.
- Scoring against a rubric (urgency, fit, risk).
- Checking if a statement is true of a text before acting.
- Replacing a prompt that asks an LLM to "return JSON".
- Anything that happens many times a day and must be fast and cheap.

## When NOT to use Jev
- Writing or rewriting text, explaining, chatting, writing code: use the main model.
- Maths, counting, date arithmetic: do it in code.
- Hard cases that need reasoning over many steps: send to the main model or a person.
- Anything where a wrong answer is costly and nothing checks it.

## How to build a decision (always in this order)
1. Write the decision as ONE specific question per judgment. For multi factor decisions ask each factor separately and combine them in code (weights in code, never in the prompt).
2. Pick the type: choice (1 of N), score (levels), noul (yes or no).
3. Write option descriptions that say what the option means, not just its name. Do not put contradicting instructions in the criteria.
4. Use `tools/jev.py` (or the official SDK). Read the key from `TYPESAFE_API_KEY`; never print or log it.
5. Add a confidence gate: below the threshold (start at 0.8) the item goes to a person or to the main model.
6. Pin the model version in production (`JEV_MODEL=jev-1.13.0` or the version you tested) and re test before changing it.
7. Test with `tools/run_test.py` on at least 100 labelled examples written like your real data, and check calibration.
8. Add the risky cases from `data/break_tests.json` to your own tests.

## Known weak spots (from TypeSafe's own Jev 1.13 notes)
Literal reading of the question; not a calculator; dates read as text; double negatives and multi hop questions; accuracy
drops when the text has lots of unrelated content; does not treat input as hostile (prompt injection can shift answers);
contradicting criteria confuse it; leans toward the first option; cannot generate text. Design around these: keep text
short and relevant, strip what is not needed, shuffle or test option order, run the injection check on outside text.

## Hard rules
- Never let Jev alone take an irreversible action (send, delete, pay, sign, add to a block list) without a rule or a person confirming.
- A stop or do not contact request is always honoured on every channel; the model only flags, your code enforces.
- Never put real customer data in tests, prompts or logs unless you have read TypeSafe's data policy and have the right to.
- Never paste or echo the API key. If the key is missing, tell the user to set it in their own terminal.
- Say what is a measured result and what is a guess.
