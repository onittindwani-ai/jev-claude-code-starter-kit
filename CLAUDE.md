# Jev Claude Code Starter Kit: instructions for Claude Code

This folder is a kit that helps people set up and use Jev (TypeSafe AI's System One model). When a user opens it:
- Offer the setup prompt in `02-SETUP-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md` and follow it exactly.
- NEVER ask for, print, log or write the API key. It lives only in `TYPESAFE_API_KEY` or a git ignored `.env`. If it is
  missing, tell the user the exact command to run in their own terminal.
- Tools use only the Python standard library. Run the tests with `python3 -m unittest discover -s tests`.
- The mock server (`tools/mock_server.py`) is a fake, not Jev. Always say so.
- Use made up data only. Never send, delete or pay anything.
- Follow `templates/claude-code/skills/jev-decisions/SKILL.md` whenever you design a decision with Jev.
- Prices and versions change: tell the user to re check typesafe.ai and docs.typesafe.ai.
