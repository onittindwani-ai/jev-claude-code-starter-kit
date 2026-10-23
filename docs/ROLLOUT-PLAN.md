# Rollout plan: from first test to live (about 2 weeks)

## Day 1: prove it
Setup, `jev_check.py`, the test prompt, the break tests. Goal: you have seen Jev answer, and you know the cost.

## Days 2 to 3: test on your own data
Write 100 labelled examples in the style of your real messages (made up or properly anonymised). Run `tools/run_test.py
--data yours.jsonl`. Read accuracy, the confusion table and the calibration table. Pick a confidence threshold.

## Days 4 to 10: shadow week
Jev decides on every item but a person still does the real work. Store Jev's answer next to the person's action
(prompt 8 in `04-GO-LIVE-PROMPTS.md`). Do not act on Jev's answers.

## Day 11: review
Agreement rate, where they disagree (who was right?), the share at or above the threshold, anything dangerous (a wrong
answer with high confidence). Fix the questions or the threshold, and run the test again.

## Days 12 to 14: partial go live
Let Jev act automatically ONLY on safe, reversible actions above the threshold (for example sorting a reply into a
folder, creating a task). Keep the rest on the review list. Keep stop requests enforced by code.

## Always
- Pin the model version; re test before upgrading.
- Keep the audit log; read the review list daily for the first month.
- Re run your test set weekly and alert on a drop of more than 3 points.
- Delete or rotate any key that showed up anywhere it should not.
