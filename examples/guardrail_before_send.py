"""Hold any drafted message that could invent a fact, push too hard or promise a result.

Usage: python3 examples/guardrail_before_send.py [--mock]
In your own system: call check(draft, facts) as the last step before sending and hold anything that returns HOLD.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import jev  # noqa: E402

DRAFTS = [
    ("Hi Sam, saw your post about hiring. We help agencies book meetings. Would a short call help?", "Sam posted about hiring."),
    ("Hi Sam, congrats on raising your Series B last week! We guarantee 50 meetings a month.", "Sam posted about hiring."),
]


def check(client, draft, facts):
    info_path = os.path.join(os.path.dirname(__file__), "..", "templates", "questions", "outbound-message-guardrail.json")
    with open(info_path) as handle:
        info = json.load(handle)
    state = "Known facts about the recipient: %s\n\nDraft message: %s" % (facts, draft)
    answers, _ = client.ask(state, info["questions"])
    limit = info["thresholds"]["hold_if_any_noul_at_least"]
    reasons = [k for k in ("unsupported_claim", "personal_detail_risk", "promises_results") if answers[k]["noul"] >= limit]
    if answers["aggressive_tone"].get("score", 0) >= info["thresholds"]["hold_if_tone_at_least"]:
        reasons.append("aggressive_tone")
    return ("HOLD", reasons) if reasons else ("SEND (after normal approval)", [])


def main():
    if "--mock" in sys.argv:
        os.environ.setdefault("JEV_BASE_URL", "http://127.0.0.1:8765")
        os.environ.setdefault("TYPESAFE_API_KEY", "mock")
    client = jev.JevClient()
    try:
        for draft, facts in DRAFTS:
            verdict, reasons = check(client, draft, facts)
            print("%s %s\n     %s" % (verdict, ", ".join(reasons), draft))
    except jev.JevError as err:
        print("FAILED:", err)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
