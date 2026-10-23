# Jev Claude Code Starter Kit: instructions for Codex and other agents

Same rules as `CLAUDE.md`. Setup prompt: `02-SETUP-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md`. Never ask for, print, log or write the
API key (use `TYPESAFE_API_KEY` or a git ignored `.env`). Tools are Python standard library only; run
`python3 -m unittest discover -s tests`. The mock server is a fake, not Jev. Use made up data only. Follow the rules in
`templates/claude-code/skills/jev-decisions/SKILL.md` when designing a decision with Jev.
