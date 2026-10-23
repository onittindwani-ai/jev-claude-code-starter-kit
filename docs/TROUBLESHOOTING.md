# Troubleshooting

| What you see | Why | Fix |
| --- | --- | --- |
| `No API key found` | The key is not in this terminal session | Run `export TYPESAFE_API_KEY="your-key"` in the same terminal, or fill `.env`; start a new AI session if the AI cannot see it |
| `API keys cannot be created or reactivated: this organization has no available credits` (in the console) | No credit yet | Console > Billing > Add funds (5 dollars), then create the key |
| `HTTP 401` | Key wrong, deleted or has a typo | Create a new key in the console, set it again |
| `HTTP 429` | Rate limit | Wait; lower `--workers`; the client retries with backoff |
| `HTTP 529` | TypeSafe overloaded | Retry in a moment (the client retries) |
| `HTTP 400` with `max_tokens_exceeded` | Text longer than the model's context | Send less text |
| `HTTP 422` | A required field is missing or a question is malformed | Check the question set against `templates/questions` |
| `Could not reach api.typesafe.ai` | Network, VPN or firewall | Check your connection; try `curl -I https://api.typesafe.ai` |
| The AI says the TypeSafe skill is not found | The session started before the install | Start a new session; use only one install method |
| `python3: command not found` | Python is not installed | Install Python 3.9 or newer from python.org |
| Tests fail on your machine | Port 8791 or 8792 busy, or old Python | Close the other program; check `python3 --version` |
| Jev's answers look wrong | Question too vague, options overlap, or text too noisy | Rewrite the criteria; run `break_tests.py`; send less text; test option order |
| The keyword rule beats Jev | Your replies are simple | Use the rule. That is a real and good result |
| Costs look higher than expected | Long texts or many calls | Check the Usage page; trim the text; batch questions |

Still stuck? TypeSafe has a Discord (link on typesafe.ai) and docs at docs.typesafe.ai. Never paste your key there.
