# Honest limits of Jev, and how this kit designs around them

Source: TypeSafe's own "jaggedness" page for Jev 1.13 (docs.typesafe.ai/model-jaggedness/jev-1.13.md, read 2026-10-23),
plus the product documentation. Re check it before you rely on it: versions change.

| # | Weak spot (TypeSafe's words, shortened) | What to do |
| --- | --- | --- |
| 1 | Answers the question you wrote, not the one you meant (scope words, negations) | Write plain, literal questions; test odd phrasings (`break_tests.py`) |
| 2 | Not a calculator; counting unreliable; numbers like hex or RGB do badly | Do maths in code; pass counts as facts, not for Jev to compute |
| 3 | Reads dates as text, not as ordered quantities | Compare dates in code before or after Jev |
| 4 | Double negatives and "a property of a property" reduce accuracy | Split into simple questions; avoid double negatives in criteria |
| 5 | Accuracy falls as the text fills with unrelated content | Send only the relevant text (strip signatures, long quotes, footers) |
| 6 | Does not treat the text as hostile: injected instructions can shift answers | Run the prompt injection check; never let Jev alone trigger an action |
| 7 | Contradictory instructions or criteria confuse it | Keep criteria consistent; one meaning per option |
| 8 | Leans toward the first option in a Choice | Test option order; put the safest or most common option where you want bias to land |
| 9 | Not trained to generate text; forcing it is slow and weak | Use a chat model to write; Jev only decides |

Also true: a typed answer is always in the right FORMAT, but it can still be the WRONG choice with high confidence.
"Zero hallucinations" is a format promise, not a truth promise. Measure accuracy and calibration on your own data
(`tools/run_test.py`).

Also from the docs: Jev 1.14 (about 14 to 15 October 2026) added image input and longer context behind opt in headers;
TypeSafe itself calls these features not yet production ready. This kit does not use them.

The test data in this kit is built to expose these weak spots: sarcasm, mixed intent, buried requests, redirects, very short replies and
quoted threads each have tags, and `run_test.py` prints the weakest ones. If Jev scores very high on everything, make your own harder
replies from your real inbox (anonymised) and test again.
