# 03. The test prompt (see Jev work, step by step)

Use this AFTER setup, when `python3 tools/jev_check.py` says "OK: setup works". Paste the box into Claude Code or Codex
in this kit's folder. It costs a few cents at most (about 100 short calls in total).

```
Test Jev for me and explain everything in plain words, as if I have never used it. Use only the made up data in this
kit. Never print, ask for or write my API key; it is in the TYPESAFE_API_KEY environment variable or in .env. If a
command says the key is missing, stop and tell me how to set it in my own terminal. Do not send, change or delete
anything outside this folder. Stop and ask me before you spend more than 20 cents.

PART 1. Prove it works
1. Run `python3 tools/jev_check.py`. Explain each line of the output: what department, frustration and urgent mean, what
   probability and confidence are, the time in seconds, the token count and the cost.

PART 2. See it on sales replies
2. Run `python3 tools/triage_replies.py data/sample_10_replies.json`. Show the table. For every row say in 1 sentence
   whether Jev's answer looks right and why. Point out which rows went to a person and why (low confidence, or a stop
   request).
3. Run `python3 examples/morning_review_queue.py results/triaged.csv` and show the morning list.
4. Run the 5 examples in `examples/` that use Jev (reply_router, lead_scoring, call_outcome_router, guardrail_before_send)
   and explain in 2 sentences what each one decided and what a real system would do next.

PART 3. Run the real test
5. Run `python3 tools/run_test.py --limit 60`. Explain: accuracy of Jev versus the plain keyword rule, the speed in
   milliseconds, the cost per 1,000 replies, the confusion table (which types get mixed up), the calibration table
   (when Jev says 90 percent, is it right about 90 percent of the time?) and the human review rule result.
6. If the results look good, run the full 300: `python3 tools/run_test.py`, and compare with the first 60.
7. Tell me: Is Jev better than the keyword rule here? Is its confidence honest? What confidence threshold would you
   choose, and what share of replies would go to a person at that threshold?

PART 4. Try to break it
8. Run `python3 tools/break_tests.py`. Explain each row: hidden instructions, double negatives, option order, long noise.
   Which ones did Jev get wrong, and was the confidence high (dangerous) or low (safe)?

PART 5. Cost
9. Run `python3 tools/cost_calculator.py --calls-per-day 5000 --tokens-per-call 500` and explain what 5,000 replies a day
   would cost with Jev. Mention that the price is $0.042 per million input tokens with free output on 2026-10-23 and that
   I should re check typesafe.ai.

PART 6. Report
10. Write `results/REPORT.md` with: what I tested, the numbers, 5 plain sentences about what Jev is good at, 5 about
    where it fails, the threshold you recommend, and the 3 next steps for using Jev in a real sales system.
    Mark every number as measured (from this run) or claimed (from TypeSafe).
11. End with a short summary of at most 10 lines, and the one thing I should do next.
```

## What you should see
- A table of 10 replies with a reply type, a probability, a confidence and a flag for a person.
- Answers in about a tenth of a second to half a second each (times vary; your own numbers are the ones that matter).
- A scoreboard comparing Jev with a plain keyword rule, and a calibration table.

## If something is odd
Read `docs/TROUBLESHOOTING.md`. If the keyword rule beats Jev on your replies, that is a real result: you may not need a
model for that step. If Jev's confidence is not honest on your data, set a higher threshold or send more to a person.
