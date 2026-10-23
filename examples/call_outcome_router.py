"""Turn call summaries into next steps for your CRM. Never acts on a do not call without a person confirming.

Usage: python3 examples/call_outcome_router.py [--mock]
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import jev  # noqa: E402

CALLS = [
    "Spoke with the owner. He liked the idea and we agreed on Thursday at 2pm for a demo.",
    "Went to voicemail, left a short message.",
    "She said please do not call this number again.",
    "He said call me back next Tuesday, he is in a meeting now.",
]
NEXT = {"meeting_booked": "Create the calendar event and update the CRM stage",
        "callback_requested": "Schedule a callback at the time they asked (check their time zone)",
        "voicemail": "Retry once on another day, then stop",
        "not_interested": "Close as not interested",
        "wrong_number": "Mark the number wrong, find the right contact",
        "do_not_call": "STOP: add to the do not call list and have a person confirm"}


def main():
    if "--mock" in sys.argv:
        os.environ.setdefault("JEV_BASE_URL", "http://127.0.0.1:8765")
        os.environ.setdefault("TYPESAFE_API_KEY", "mock")
    path = os.path.join(os.path.dirname(__file__), "..", "templates", "questions", "call-outcome-router.json")
    with open(path) as handle:
        info = json.load(handle)
    client = jev.JevClient()
    try:
        for call in CALLS:
            answers, _ = client.ask(call, info["questions"])
            outcome, _, conf = jev.top_choice(answers["outcome"])
            gate = info["thresholds"]["auto_if_confidence_at_least"]
            if outcome == "do_not_call" or conf < gate:
                action = "PERSON CONFIRMS (%s, confidence %.2f)" % (outcome, conf)
            else:
                action = NEXT[outcome]
            print("%-16s %.2f  -> %s\n     %s" % (outcome, conf, action, call[:70]))
    except jev.JevError as err:
        print("FAILED:", err)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
