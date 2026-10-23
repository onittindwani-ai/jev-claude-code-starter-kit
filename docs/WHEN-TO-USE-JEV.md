# When to use Jev (and when not to)

Checked against TypeSafe's docs on 2026-10-23. Jev is a System One model: fast, automatic judgment, not thinking in words.

## The test in 4 questions
1. Is the answer 1 of a set I can list, a rating on a scale I can describe, or a yes or no? (If you need a paragraph, no.)
2. Does it happen many times a day? (If it happens twice a month, any model is fine.)
3. Do I need it fast and cheap? (A sales reply needs an answer in a blink; an essay does not.)
4. Can a rule or a person catch the mistakes? (If not, do not automate it yet.)
4 yes: Jev fits. 3 or fewer: use a bigger model, plain code or a person.

## Good fits in a sales system
| Decision | Question type | Start with |
| --- | --- | --- |
| Which kind of reply is this? | choice | `templates/questions/reply-triage.json` |
| Is this a stop request? | noul | same file, `stop_request` |
| Real person or out of office or bounce? | choice | `automated-message-detector.json` |
| Does this lead fit our ideal customer? | choice, score, noul | `lead-fit-icp.json` |
| What happened on this call? | choice | `call-outcome-router.json` |
| What is the main objection? | choice | `objection-classifier.json` |
| Wants a meeting? Proposed a time? | noul | `meeting-intent.json` |
| Is this draft safe to send? | noul, score | `outbound-message-guardrail.json` |
| Is this outside text trying to instruct my AI? | noul | `prompt-injection-check.json` |
| Which team should get this ticket? | choice | `support-triage.json` |
| What CRM signals are in this transcript? | noul, score | `call-transcript-signals.json` |

## Bad fits (use something else)
- Writing a reply, summarising, explaining, brainstorming: use a chat model.
- Writing or changing code: use Claude Code or Codex.
- Any arithmetic, counting or date comparison: use code.
- Long multi step reasoning ("compare these 5 contracts and decide"): a bigger model or a person.
- Anything that should never be wrong and has no check behind it.
- Secret or sensitive data you are not allowed to send to a third party.

## The winning pattern
Jev decides the cheap, frequent, clear decisions. Code checks them against rules. A bigger model or a person handles the
hard and risky ones. Claude Code writes and maintains the whole system.
