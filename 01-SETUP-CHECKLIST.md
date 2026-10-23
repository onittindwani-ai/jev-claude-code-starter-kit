# 01. Setup checklist

Tick every box. If one fails, open `docs/TROUBLESHOOTING.md`.

## Account
- [ ] Opened typesafe.ai, scrolled down, clicked **Create Account**
- [ ] Signed up with Google or email
- [ ] Reviewed and accepted the terms, finished the onboarding questions
- [ ] Landed on the Meet Jev page and clicked **Enter console**
- [ ] Read the **Our Data Policy** and **Trust Center** links on the console home

## Credit and key
- [ ] Added funds in **Billing** (5 dollars is enough for testing; the console will not create a key at $0)
- [ ] Created an API key in **API Keys** with a name like "test 1"
- [ ] Copied the key ONCE and kept it out of every chat, screenshot, video and file that is shared

## Your AI
- [ ] Opened this kit folder in Claude Code or Codex
- [ ] Pasted the setup prompt from `02-SETUP-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md`
- [ ] The AI installed the TypeSafe skill with ONE method only (Claude Code plugin or `npx skills add`)
- [ ] The AI ran the offline tests (15 tests pass) and did not ask for my key

## Your key (in YOUR terminal, never in the chat)
- [ ] Ran `export TYPESAFE_API_KEY="your-key"` in the kit folder (or filled `.env`)
- [ ] Ran `python3 tools/jev_check.py` and saw "OK: setup works"
- [ ] Told my AI "the key is set" (without pasting the key); started a new session if it could not see the key

## See it work
- [ ] Ran the test prompt from `03-TEST-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md`
- [ ] Saw the reply table with probabilities and confidence
- [ ] Understood which answers go to a person (low confidence)
- [ ] Looked at **Usage** in the console to see the (tiny) cost

## Put it to work
- [ ] Copied the CLAUDE.md or AGENTS.md snippet and the `jev-decisions` skill into my own project (`04-GO-LIVE-PROMPTS.md`)
- [ ] Picked 1 decision from `templates/questions/` to start with
- [ ] Wrote 100 of MY OWN labelled examples (no real customer data unless I have the right to use it)
- [ ] Ran my test, read the calibration table, chose my confidence threshold
- [ ] Planned a shadow week: Jev decides, a person still does the real work, I compare

## Safety
- [ ] No key in git (`git status` shows no `.env`)
- [ ] Deleted the test key in the console when finished with it (or rotated it if it ever showed up anywhere)
- [ ] Nothing irreversible (send, delete, pay, block) happens without a rule or a person
