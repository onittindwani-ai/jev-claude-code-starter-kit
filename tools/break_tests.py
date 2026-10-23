"""Try to break Jev with the weak spots TypeSafe lists in its own docs (hidden instructions, double negatives,
option order, long noise). Run it to see for yourself before you trust Jev with real traffic.

Usage: python3 tools/break_tests.py [--mock]
"""
import argparse
import json
import os
import sys

import jev
from triage_replies import REPLY_TYPES


def ask_type(client, text, order):
    options = {k: REPLY_TYPES[k] for k in order}
    answers, _ = client.ask(text, {"reply_type": jev.choice("What type of reply is this message to a sales email", options)})
    return jev.top_choice(answers["reply_type"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--data", default="data/break_tests.json")
    args = parser.parse_args()
    if args.mock:
        os.environ.setdefault("JEV_BASE_URL", "http://127.0.0.1:8765")
        os.environ.setdefault("TYPESAFE_API_KEY", "mock")
    with open(args.data, encoding="utf-8") as handle:
        data = json.load(handle)
    default_order = list(REPLY_TYPES)
    try:
        client = jev.JevClient()
        results = []
        for group in ("hidden_instruction", "double_negative", "long_noise"):
            for case in data[group]:
                kind, prob, conf = ask_type(client, case["text"], default_order)
                results.append((group, case["id"], case["right"], kind, conf))
        for case in data["option_order"]["replies"]:
            a = ask_type(client, case["text"], default_order)
            b = ask_type(client, case["text"], list(reversed(default_order)))
            results.append(("option_order", case["id"], case["right"], "%s | reversed: %s" % (a[0], b[0]),
                            min(a[2], b[2])))
    except jev.JevError as err:
        print("FAILED:", err)
        return 1
    print("%-18s %-4s %-16s %-34s %s" % ("test", "id", "right answer", "Jev said", "confidence"))
    for group, cid, right, said, conf in results:
        print("%-18s %-4s %-16s %-34s %.2f" % (group, cid, right, said, conf))
    print("\nRead it like this: a wrong answer with HIGH confidence is the dangerous kind. Keep a person or a rule "
          "in front of anything risky.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
