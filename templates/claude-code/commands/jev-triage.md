---
description: Sort a file of sales replies with Jev and show the morning list
---

Run `python3 tools/triage_replies.py $ARGUMENTS --out results/triaged.csv` and then
`python3 examples/morning_review_queue.py results/triaged.csv`. Show me the table, count how many went to a person, and
point out the 3 least sure answers in plain words. Do not send or change anything. Do not use real customer data unless
I say I have the right to.
