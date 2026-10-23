# Where Jev fits in an AI sales system

A typical AI sales system is a row of boxes. Most boxes are plain code. A few need a judgment about text. Those are Jev's job.

| Box | What happens | Who does it |
| --- | --- | --- |
| 1. Lead list in | Upload, clean, de duplicate | Code |
| 2. Fit check | Does this company match our ideal customer? | **Jev** (`lead-fit-icp.json`) |
| 3. Message written | Draft the email or call script | A chat model (Claude) |
| 4. Guardrail | Is the draft safe to send? | **Jev** (`outbound-message-guardrail.json`) |
| 5. Send or call | Limits, time zones, do not contact lists | Code |
| 6. Reply arrives | Real person, out of office, bounce? | **Jev** (`automated-message-detector.json`) |
| 7. Injection check | Is the reply trying to instruct my AI? | **Jev** (`prompt-injection-check.json`) |
| 8. Reply sorted | Interested, not now, no, wrong person, stop, question | **Jev** (`reply-triage.json`) |
| 9. Next step | Book, follow up later, close, ask, stop | Code, using Jev's answer and a threshold |
| 10. Call outcome | What happened on the call? | **Jev** (`call-outcome-router.json`) |
| 11. CRM update | Stage, fields, tasks | Code |
| 12. Morning list | What a person must look at | Code, from Jev's flags (`morning_review_queue.py`) |

Claude Code (or Codex) writes and maintains all 12 boxes. Jev is only the fast, cheap judgment inside 6 of them.
A person approves anything that leaves the building or cannot be undone.
