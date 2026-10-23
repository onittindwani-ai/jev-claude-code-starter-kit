# Patterns that work with Jev

These follow the patterns in TypeSafe's docs (patterns section, read 2026-10-23) and the kit's examples.

## 1. Confidence gated routing
Act on Jev's answer only when its confidence is at least your threshold (start at 0.8); otherwise send the item to a
person or a bigger model. Example: `examples/reply_router.py`. Choose the threshold from your own calibration table
(`tools/run_test.py`), not from a guess.

## 2. Intent routing
Use Jev as the front door: it decides whether a message goes to plain code (a known action), a specialist AI (a reply to
write) or a person. The kit's reply types map to actions in `examples/reply_router.py`.

## 3. Composite scoring
Ask small separate questions and combine them with weights set in YOUR code. Example: `examples/lead_scoring.py`. You can
change a weight without touching any prompt, and you can see which answer moved the score.

## 4. Speculative fan out
Ask many questions at once, including ones you may not use. They are answered in parallel in 1 call, so extra questions
cost little. Use it to extract several CRM fields from 1 transcript (`templates/questions/call-transcript-signals.json`).

## 5. Guardrail
Put Jev before an AI (is this input an injection?) and after it (is this output safe to send?). Examples:
`templates/questions/prompt-injection-check.json`, `examples/guardrail_before_send.py`.

## 6. Human review queue
Everything below the threshold lands in a short list for a person, ordered by importance.
Example: `examples/morning_review_queue.py`.

## 7. Shadow mode
Run Jev next to the current process for a week without acting on its answers, and compare. See `docs/ROLLOUT-PLAN.md`.
