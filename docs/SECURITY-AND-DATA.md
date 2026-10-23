# Security and data

## Your API key
- Keep it in the `TYPESAFE_API_KEY` environment variable or a git ignored `.env`. Nowhere else.
- Never paste it into an AI chat, a screenshot, a video, a doc or a commit. If it ever appears anywhere, delete the key in
  the console (API Keys) and create a new one right away.
- Create one key per project or person; delete test keys when you are done.
- Check `git status` before every commit. `.env` must never appear.
- API keys in the console are organization scoped and stay active even after their creator is removed (a note shown in the
  create key window on 2026-10-23): remove keys when people leave.

## Your data
- Read TypeSafe's data policy and Trust Center (linked at the bottom of the console home) BEFORE sending real customer
  messages. This kit's tests use made up data only.
- Send the minimum text that the decision needs. Remove names, emails and phone numbers when the decision does not need them.
- Keep your own audit log of decisions (time, answer, confidence), without secrets or more personal data than you already store.
- Ask your lawyer about consent and privacy rules in the places you operate. This kit is not legal advice.

## Prompt injection
Any text that comes from outside (a reply, a web page, a document) can contain instructions meant for an AI. TypeSafe
says Jev does not treat the text as hostile by default. So: run `templates/questions/prompt-injection-check.json` first,
quarantine what it flags, and never let one model's answer alone trigger a risky action.

## Actions
Sending, deleting, paying, signing, blocking: always behind a rule or a person. A stop or do not contact request is enforced by
your code on every channel; Jev only flags it.
