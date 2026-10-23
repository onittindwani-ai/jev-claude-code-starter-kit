---
description: Design a new Jev decision (question set, thresholds, tests) from a plain description
---

I want a new decision with Jev: $ARGUMENTS

Follow the `jev-decisions` skill. 1) Restate the decision as specific questions (choice, score or noul). 2) Write a new
file in `templates/questions/` in the same format as the others (name, description, use_when, thresholds, questions).
3) Write 20 made up test examples with the right answers in `data/`. 4) Run them with `tools/run_questions.py` and a
small test script, and report accuracy, confidence and what goes to a person. 5) Tell me the weak spots from the skill
that apply and how the design avoids them. Never print the API key.
