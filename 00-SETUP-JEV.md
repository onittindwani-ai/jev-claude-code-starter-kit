# 00. Set up Jev in 5 minutes

Written from a real setup on 2026-10-23. Screens can change, so if a button moved, look for the same words.

## What you need
- A Google account or an email address.
- Claude Code (or Codex) on your computer.
- 5 dollars of credit (the console will not create an API key at zero credits; Onit's account showed "$0.00" and the error "API keys cannot be created or reactivated: this organization has no available credits. Add credits in Billing.").
- A terminal window.

## The steps
1. **Open typesafe.ai.** Scroll down a little and click **Create Account**.
2. **Sign up** with Google or with your email.
3. **Review our terms.** Tick "I have read and agreed to the Master Customer Agreement and Privacy Policy" and click **Continue**. (There is also a box to get product news; leave it ticked or untick it, your choice.)
4. **Tell us about yourself.** Check your name and email, pick your area of work, click **Next**, and finish the short onboarding.
5. **Meet Jev page.** Read the honest limits list if you like, then click **Enter console**.
6. **Console home.** Find the **Quickstart** box and click **Copy Agent Prompt**.
7. **Paste that prompt into Claude Code** (or Codex) and send it. It installs the TypeSafe skill (for Claude Code the prompt runs `claude plugin marketplace add typesafe-ai/skills` and `claude plugin install typesafe@typesafe-ai`; for other agents it uses `npx skills add typesafe-ai/skills --skill typesafe-ai`). Use one install method only. You may need to start a new session so the skill loads.
8. **Add credit.** In the console open **Billing** and click **Add funds**. 5 dollars is plenty for testing. (There is also a **Redeem code** button if you have a code.)
9. **Create an API key.** Open **API Keys**, click **Create key**, give it a name such as "test 1", and copy the key.
10. **Put the key in your terminal, never in the AI chat.** In a terminal run:
    `export TYPESAFE_API_KEY="your-key"` (use your real key inside the quotes).
    To keep it for next time, add that same line to your shell profile (for example `~/.zshrc` on a Mac).
11. **Tell Claude the key is set** (just say "it's set", never paste the key). Because a key set in one terminal may not reach the AI's own shell, you may need to start a new session after setting it.
12. **Try one small job.** For example: "Write 10 made up sales email replies, then use Jev to decide which ones deserve an answer, and show me a table." In Onit's run Jev returned its answers for all 10 emails in less than a second.

## Safety rules (read these)
- **Never paste your API key into a chat, a screenshot, a video or a public file.** If you ever do, delete the key in the console (API Keys) and make a new one.
- Make a key just for testing and delete it when you are done.
- Do not show your card details when recording. Blur the Billing page.
- Never send real customer data to any tool you have not read the data policy of. TypeSafe's console links an "Our Data Policy" page and a "Trust Center": read them first.
- Jev makes real API calls, so it uses your credit. Ten emails cost a tiny amount; check **Usage** in the console.

## If something goes wrong
| What you see | What to do |
| --- | --- |
| "API keys cannot be created or reactivated: this organization has no available credits" | Add funds in Billing first, then create the key |
| The AI says there is no key | The key was set in a different terminal. Start a new session, or add the export line to your shell profile |
| 401 error | The key is wrong or deleted; create a new key |
| 429 error | You hit a rate limit; wait and retry (the official SDKs retry for you) |
| The skill is not found | Start a new session after installing; use only one install method |

## What to remember
Jev does not write text. It answers typed questions with a probability. Your code (and Claude Code) does the rest.
Use its confidence number: anything below about 0.8 should go to a person (in Onit's 10 email run, the least sure answer was 0.64).

## Fast path with your AI (recommended)
After step 6 (you are inside the console), use `02-SETUP-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md`: open this kit folder in Claude
Code or Codex, paste that prompt, and it installs the TypeSafe skill, prepares your `.env`, runs the offline tests, and
prints the exact command to run in your terminal. Then use `03-TEST-PROMPT-FOR-CLAUDE-CODE-OR-CODEX.md` to see Jev work.

## The exact commands (run in YOUR terminal, in this kit's folder)
```
# 1. put your key in this terminal session (replace your-key with the key you copied)
export TYPESAFE_API_KEY="your-key"

# 2. prove it works (1 request, 3 questions)
python3 tools/jev_check.py

# 3. sort 10 sample replies and see the confidence
python3 tools/triage_replies.py data/sample_10_replies.json
```
Prefer a file? Run `cp .env.example .env`, open `.env` in an editor, replace `PASTE_YOUR_KEY_HERE` with your key and save.
`.env` is git ignored, and the tools read it automatically. You need Python 3.9 or newer (`python3 --version`); the tools
use only the Python standard library, so there is nothing to install.

## Offline practice (no key, no cost)
```
python3 tools/mock_server.py 8765 &     # a fake Jev, not the real model
python3 tools/triage_replies.py data/sample_10_replies.json --mock
```
