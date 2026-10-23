# 02. The setup prompt (paste this into Claude Code or Codex)

**Before you paste:** open Claude Code or Codex in THIS kit's folder (the one with `README.md` and `tools/`). If you do
not have the kit yet, download it from its GitHub page first. Do the account steps in `00-SETUP-JEV.md` (up to step 9)
so you have your API key ready, but do NOT paste the key into the chat.

Copy everything inside the box and paste it as your first message.

```
You are setting up Jev (TypeSafe AI's System One model) in this folder, the Jev Claude Code Starter Kit. Do everything
from your side, in order, and report each step. Rules first:

RULES
- NEVER ask me for my API key, never print it, never write it into a file you create, never put it in a command you run.
  If a step needs the key, tell me the exact command to run in MY OWN terminal.
- Do not use real customer data. Use only the made up data in this kit.
- Do not spend money. The only API calls allowed in this setup are none; I will make the first live call myself.
- Install the TypeSafe skill with ONE method only.

STEPS
1. Confirm you are in the kit folder: it must contain README.md, tools/jev.py and templates/. If not, tell me and stop.
2. Check Python: run `python3 --version`. It must be 3.9 or newer. If not, tell me how to install it for my system.
3. Install the official TypeSafe skill:
   - If you are Claude Code, run: `claude plugin marketplace add typesafe-ai/skills` and then
     `claude plugin install typesafe@typesafe-ai`.
   - If you are Codex or another agent, run: `npx skills add typesafe-ai/skills --skill typesafe-ai` and select your agent.
   - Use exactly one of these. If a command fails, show me the exact error and the fix. Tell me if a new session is
     needed for the skill to load.
4. Prepare my environment file: copy `.env.example` to `.env` ONLY IF `.env` does not exist yet. Leave the placeholder
   value `PASTE_YOUR_KEY_HERE` as it is. Check that `.gitignore` contains `.env` (add it if missing).
5. Install the kit's helpers into this project so you use Jev wherever it fits:
   - Claude Code: copy `templates/claude-code/skills/jev-decisions/` to `.claude/skills/jev-decisions/` and
     `templates/claude-code/commands/` to `.claude/commands/`. Append the text of `templates/claude-code/CLAUDE.md.snippet`
     to `CLAUDE.md` (create it if missing; do not duplicate it if it is already there).
   - Codex: append `templates/codex/AGENTS.md.snippet` to `AGENTS.md` (same rules).
6. Run the offline tests: `python3 -m unittest discover -s tests`. All tests must pass. If any fail, fix the setup problem
   (not the tests) or tell me exactly why.
7. Run an offline dry run with the built in fake Jev to prove the tools work without a key:
   start `python3 tools/mock_server.py 8765` in the background, run
   `python3 tools/triage_replies.py data/sample_10_replies.json --mock`, show me the table, and stop the mock server.
   Tell me clearly that the fake Jev is NOT the real model.
8. If the key is NOT already set in my environment, run `python3 tools/jev_check.py` ONLY to prove it fails politely (it must print how to set the key). If the key is already set, skip this step (do not make a live call).
   Do not try to find or guess a key.
9. FINISH by printing this exact message for me, with nothing missing:

   "Setup is ready. Now do this in YOUR OWN terminal, in this folder (do not paste your key here):

       export TYPESAFE_API_KEY="paste-your-key-here"
       python3 tools/jev_check.py

   (Or: cp .env.example .env, open .env, replace PASTE_YOUR_KEY_HERE with your key, save, then run
   python3 tools/jev_check.py.) When you see 'OK: setup works', come back and say: the key is set."

10. List every file you created or changed and every command you ran, and tell me what to do if I get a 401, a 429 or
    'No API key found'.
```

## What this prompt does, in plain words
It installs the official TypeSafe skill, prepares a safe `.env`, installs this kit's skill and snippets so your AI knows
when to use Jev, runs 15 offline tests, shows Jev's flow with a harmless fake, and ends by telling you the exact command
to run yourself. Your key never touches the chat.

## After it finishes
1. Run the 2 commands it printed in your own terminal.
2. Come back to the AI and say: **the key is set**.
3. Open `03-TEST-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md` and paste the test prompt.

If your AI cannot see the key (a key set in one terminal does not always reach the AI's own shell), start a new AI
session after setting the key, or put the key in `.env` (the tools read it automatically).
