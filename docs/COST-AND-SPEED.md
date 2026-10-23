# Cost and speed

## What TypeSafe says (typesafe.ai and docs, 2026-10-23, re check)
- Price: $42 per billion input tokens ($0.042 per million), output tokens free.
- Claims: 193.6x faster and 444.6x cheaper than frontier chat models on System One tasks, from TypeSafe's own tests.
- Reported latency: roughly 70 to 500 milliseconds per call (third party and vendor sources).
- Batching questions into 1 call is cheaper and faster than 1 call per question: the docs report 12.2x cheaper and 10.0x
  faster on 1 cookbook example. This kit's triage already asks several questions in 1 call.

## What to measure yourself
`python3 tools/run_test.py` prints milliseconds per reply and the estimated cost per 1,000 replies from the token counts
the API returns. Those are YOUR numbers. Quote those, not the vendor's.

## The calculator
```
python3 tools/cost_calculator.py --calls-per-day 5000 --tokens-per-call 500
python3 tools/cost_calculator.py --calls-per-day 5000 --tokens-per-call 500 --other-input-price 3.0 --other-output-price 15.0 --other-output-tokens 60
```
Replace the "other" numbers with the real price of the model you use today. Price is only half the story: quality, your
confidence threshold and the share that needs a person decide the real cost.

## Rules of thumb
- Send less text: fewer tokens is cheaper and more accurate.
- Ask several related questions in 1 call (the state is read once).
- Cache the answers for identical text.
- Watch the **Usage** page in the console during the first week.
