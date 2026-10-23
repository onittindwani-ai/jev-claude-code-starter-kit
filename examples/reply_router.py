"""Route sales replies to the next step. It never sends anything: it only decides and writes a plan.

Pattern: confidence gated routing (see docs/PATTERNS.md). Jev decides, code checks, a person approves.
Usage: python3 examples/reply_router.py data/sample_10_replies.json [--mock]
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import jev  # noqa: E402
from triage_replies import load_replies  # noqa: E402

ROUTES = {
    "interested": "Create a task: a person replies today and offers 2 meeting times",
    "not_now": "Schedule a follow up in 90 days with 1 honest message",
    "not_interested": "Mark closed, no more messages",
    "wrong_person": "Ask who the right person is, once; update the contact",
    "unsubscribe": "Add to the do not contact list on EVERY channel right now",
    "question": "Draft an answer from the approved FAQ for a person to approve",
}
AUTOMATED = {"out_of_office": "Wait until the return date, then retry once", "bounce": "Mark the address invalid",
             "spam": "Ignore"}
THRESHOLD = 0.8


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--mock" in sys.argv:
        os.environ.setdefault("JEV_BASE_URL", "http://127.0.0.1:8765")
        os.environ.setdefault("TYPESAFE_API_KEY", "mock")
    path = args[0] if args else "data/sample_10_replies.json"
    with open(os.path.join(os.path.dirname(__file__), "..", "templates", "questions", "automated-message-detector.json")) as h:
        detector = json.load(h)["questions"]
    with open(os.path.join(os.path.dirname(__file__), "..", "templates", "questions", "reply-triage.json")) as h:
        triage = json.load(h)["questions"]
    client = jev.JevClient()
    try:
        for reply in load_replies(path):
            first, _ = client.ask(reply["text"], detector)
            kind, _, conf = jev.top_choice(first["message_kind"])
            if kind != "human_reply" and conf >= THRESHOLD:
                print("#%s  AUTOMATED (%s, %.2f): %s" % (reply["id"], kind, conf, AUTOMATED.get(kind, "Ignore")))
                continue
            answers, _ = client.ask(reply["text"], triage)
            rtype, _, rconf = jev.top_choice(answers["reply_type"])
            stop = answers["stop_request"].get("noul", 0)
            if stop >= 0.5:
                print("#%s  STOP REQUEST (%.2f): %s" % (reply["id"], stop, ROUTES["unsubscribe"]))
            elif rconf < THRESHOLD:
                print("#%s  PERSON REVIEWS (%s, confidence %.2f is below %.2f)" % (reply["id"], rtype, rconf, THRESHOLD))
            else:
                print("#%s  %-15s (%.2f)  -> %s" % (reply["id"], rtype, rconf, ROUTES[rtype]))
    except jev.JevError as err:
        print("FAILED:", err)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
