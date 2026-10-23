"""Turn a triaged CSV (from tools/triage_replies.py) into a short morning list for a person.

Usage: python3 examples/morning_review_queue.py results/triaged.csv
Order: stop requests first, then replies from interested people, then everything that needs review.
"""
import csv
import sys


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "results/triaged.csv"
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    stops = [r for r in rows if float(r["stop_request"]) >= 0.5]
    hot = [r for r in rows if r["reply_type"] == "interested" and r not in stops]
    review = [r for r in rows if r["action"].startswith("REVIEW") and r not in stops and r not in hot]
    print("MORNING LIST (%d replies)\n" % len(rows))
    for title, group in (("1. STOP REQUESTS: handle now", stops), ("2. INTERESTED: answer today", hot),
                         ("3. NEEDS A PERSON'S EYES", review)):
        print(title)
        for r in group:
            print("   #%s [%s, confidence %s] %s" % (r["id"], r["reply_type"], r["confidence"], r["text"]))
        if not group:
            print("   (none)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
