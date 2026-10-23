"""Sort sales replies with Jev and flag the unsure ones for a person.

Input : a .json list, a .jsonl file, or a .csv with a column named text (and optional id).
Output: a CSV with reply type, probability, confidence and a REVIEW flag.

Usage:
  python3 tools/triage_replies.py data/sample_10_replies.json
  python3 tools/triage_replies.py my_replies.csv --out results/triaged.csv --review-below 0.8
Add --mock to use a local fake Jev (no key, not the real model) for a dry run.
"""
import argparse
import csv
import json
import os
import sys

import jev

REPLY_TYPES = {
    "interested": "The sender wants to talk, see a demo, get pricing or book a time, even if they add conditions or questions, and they are the person who will take the next step",
    "not_now": "The sender is open to it but asks to be contacted later, or says timing, budget or a freeze blocks it for now",
    "not_interested": "The sender declines for now and for good: no interest, no need, already covered, or a firm no, without asking to stop all contact",
    "wrong_person": "The sender says they are not the right person or the wrong company, or points to or forwards it to someone else, even if they like the idea",
    "unsubscribe": "The sender asks to stop, be removed, delete data or not be contacted again, in any wording or language, even if mixed with other content or buried in a long message",
    "question": "The sender asks something before deciding (price, how it works, security, source of their email) and shows no clear decision yet",
}


def load_replies(path):
    if path.endswith(".csv"):
        with open(path, newline="", encoding="utf-8") as handle:
            return [{"id": row.get("id") or i + 1, "text": row["text"]} for i, row in enumerate(csv.DictReader(handle))]
    with open(path, encoding="utf-8") as handle:
        text = handle.read().strip()
    if text.startswith("["):
        rows = json.loads(text)
    else:
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    return [{"id": r.get("id", i + 1), "text": r["text"] if isinstance(r, dict) else str(r)} for i, r in enumerate(rows)]


def questions():
    return {
        "reply_type": jev.choice("What type of reply is this message to a sales email", REPLY_TYPES),
        "stop_request": jev.noul("The sender asks to stop receiving messages or to be removed from the list"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--out", default="results/triaged.csv")
    parser.add_argument("--review-below", type=float, default=0.8, help="confidence below this goes to a person")
    parser.add_argument("--mock", action="store_true", help="use the local mock server (start tools/mock_server.py)")
    args = parser.parse_args()
    if args.mock:
        os.environ.setdefault("JEV_BASE_URL", "http://127.0.0.1:8765")
        os.environ.setdefault("TYPESAFE_API_KEY", "mock")
    try:
        client = jev.JevClient()
        rows = []
        for reply in load_replies(args.input):
            answers, meta = client.ask(reply["text"], questions())
            kind, prob, conf = jev.top_choice(answers["reply_type"])
            stop = answers["stop_request"].get("noul", 0.0)
            review = conf < args.review_below or (stop >= 0.5 and kind != "unsubscribe")
            rows.append({"id": reply["id"], "reply_type": kind, "probability": round(prob, 2),
                         "confidence": round(conf, 2), "stop_request": round(stop, 2),
                         "action": "REVIEW (person)" if review else "AUTO", "seconds": round(meta["seconds"], 2),
                         "text": reply["text"].replace("\n", " ")[:90]})
    except jev.JevError as err:
        print("FAILED:", err)
        return 1
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print("%-4s %-15s %-6s %-6s %-16s %s" % ("id", "reply type", "prob", "conf", "action", "text"))
    for r in rows:
        print("%-4s %-15s %-6s %-6s %-16s %s" % (r["id"], r["reply_type"], r["probability"], r["confidence"],
                                                r["action"], r["text"][:50]))
    review = sum(1 for r in rows if r["action"].startswith("REVIEW"))
    print("\n%d replies, %d sent to a person (confidence below %.2f or a stop request that was not labelled unsubscribe). Saved %s"
          % (len(rows), review, args.review_below, args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
