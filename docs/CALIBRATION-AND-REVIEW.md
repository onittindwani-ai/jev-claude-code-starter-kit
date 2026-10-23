# Calibration and the review rule, explained simply

Jev returns a **confidence** with each answer. TypeSafe says it is calibrated: when it says 80 percent, it should be
right about 80 times in 100. That is a claim, so test it.

## How the kit tests it
`tools/run_test.py` puts all answers into groups by confidence (for example 0.90 to 0.95) and prints how often Jev was right
in each group. Read the table like this:
- Share right close to the confidence: honest. Good.
- Share right far BELOW the confidence: over confident. Raise your threshold.
- Share right far ABOVE the confidence: cautious. You may be able to lower the threshold and automate more.

## The review rule
Everything below the threshold goes to a person. The test prints how many go to a person at your threshold and how accurate
the automatic ones are. Choose the lowest threshold where the automatic group is accurate enough for the risk of the action.

| Risk of a wrong automatic action | Start threshold |
| --- | --- |
| Tiny and reversible (sorting into a folder) | 0.70 |
| Normal (creating a task, drafting a reply) | 0.80 |
| Costly (anything customer facing) | 0.90, and a person approves |
| Irreversible (send, delete, pay, block) | Never automatic |

Do not trust a calibration table made from 20 examples. Use at least 100, and more for rare cases.
