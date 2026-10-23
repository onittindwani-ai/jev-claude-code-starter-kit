# 04. Go live: prompts that build Jev into YOUR real project

Open Claude Code or Codex in YOUR project (not this kit). First copy the helpers over (or let prompt 1 do it).
Replace the [BRACKETS]. Never paste your API key; each prompt tells the AI to use the environment variable.

## Prompt 1: teach your AI to use Jev everywhere it fits
```
Install the Jev helpers from the Jev Claude Code Starter Kit into this project: copy
[PATH TO KIT]/templates/claude-code/skills/jev-decisions to .claude/skills/jev-decisions, the commands folder to
.claude/commands, tools/jev.py into [WHERE MY TOOLS LIVE], and append CLAUDE.md.snippet (or AGENTS.md.snippet for Codex)
to my project instructions. Then scan this project and list every place where code makes a judgment about text with an
LLM call or a hand written rule (routing, classifying, scoring, yes or no checks). For each, tell me: is Jev a good fit,
why, what question type, what confidence threshold to start with, and what could go wrong. Do not change anything yet.
Never print or ask for my API key.
```

## Prompt 2: reply triage for my real replies
```
Build a reply triage step for my sales system using Jev, following the jev-decisions skill. Input: replies to my cold
emails from [WHERE REPLIES COME FROM]. Use the question set templates/questions/reply-triage.json (adjust the 6 types to
my business: [MY TYPES IF DIFFERENT]). Rules: a confidence gate of 0.8 (below goes to a person); any reply with a stop
request is added to my do not contact list on EVERY channel by my code (Jev only flags); nothing is sent automatically;
log every decision with the time, answer and confidence (no key, no personal data beyond what I already store). Write a
test with 100 made up examples in my style, run it, show accuracy and calibration, and tell me the threshold you chose.
```

## Prompt 3: score and prioritise leads
```
Build lead scoring with Jev using composite scoring: separate questions for industry fit, role relevance and purchase
intent (start from templates/questions/lead-fit-icp.json and change the options to my ideal customer: [DESCRIBE MY IDEAL
CUSTOMER]), with the weights set in code (start 0.4, 0.3, 0.3) and written in a config file I can change. Output a
score and the 3 answers behind it for each lead so a person can see why. Test on 50 made up leads, then show me the
ranking. Do not contact anyone.
```

## Prompt 4: a guardrail before any message is sent
```
Add a guardrail as the LAST step before my system sends any AI written message ([EMAIL, SMS, OR CALL SCRIPT]). Use
templates/questions/outbound-message-guardrail.json and examples/guardrail_before_send.py as the base. The check gets
the draft plus the facts we actually know about the recipient, and holds the message if it may invent a fact, mention an
unknown personal detail, promise a result or sound aggressive. Held messages go to a review list with the reason.
Never auto approve a held message. Add tests with 10 good and 10 bad drafts.
```

## Prompt 5: route call outcomes into my CRM
```
After every call my system produces a summary. Add a step that uses Jev (templates/questions/call-outcome-router.json)
to choose the outcome and the next step, then updates [MY CRM] through the existing integration. A do not call outcome or
a confidence below 0.85 is never applied automatically: it goes to a person. Keep an audit log. Add tests with 20 made
up call summaries in my style.
```

## Prompt 6: protect my AI from instructions hidden in replies
```
Before any outside text (reply, web page, document) reaches an AI that can take actions, run it through the prompt
injection check (templates/questions/prompt-injection-check.json). Anything at 0.5 or above is quarantined and shown to
a person; it never reaches the acting AI. Add tests using data/break_tests.json plus 10 new injection examples. Explain
what this does and does not protect against.
```

## Prompt 7: a daily morning list
```
Build a morning list for my team: every day at [TIME] take all replies from the last 24 hours, triage them with Jev,
and write a short list in this order: stop requests, interested replies, then everything that needs a person's eyes.
Deliver it to [WHERE: A FILE, SLACK, EMAIL DRAFT]. It must only prepare the list and drafts; nothing is sent to a
customer. Show me how to schedule it and how to stop it.
```

## Prompt 8: a safe rollout (shadow week)
```
Set up a shadow week for the Jev triage: Jev decides on every reply but a person still handles them as today. Record
Jev's answer next to the person's real action, and after 7 days produce a report: how often they agree, where they
disagree, the calibration table, the best confidence threshold, and what share could be automated safely. Do not change
how replies are handled during the week.
```

## Prompt 9: compare Jev with the model I use today
```
Run my real labelled examples ([PATH]) through Jev and through [MY CURRENT MODEL OR PROMPT]. Report accuracy, speed,
cost per 1,000 and which cases each one gets wrong. Use tools/run_test.py with --compare for the other model's answers.
Tell me honestly which one I should use for this step and why.
```

## Prompt 10: pin the version and monitor it
```
Pin the Jev model version in my project (JEV_MODEL) to the version I tested, add a weekly job that re runs my test set
and warns me if accuracy drops by more than 3 points or if the model alias now points to a different version, and write
a short note on how to upgrade safely (test first, then switch).
```
