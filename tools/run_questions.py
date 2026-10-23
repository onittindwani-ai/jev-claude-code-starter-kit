"""Run any question set from templates/questions on a piece of text.

Usage:
  python3 tools/run_questions.py templates/questions/reply-triage.json --text "Sounds good, send me times."
  python3 tools/run_questions.py templates/questions/call-outcome-router.json --file call_summary.txt
Add --mock for a dry run with the local fake. Build your own set by copying a file and changing the questions.
"""
import argparse
import json
import os
import sys

import jev


def load_set(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return data, data["questions"]


def show(name, answer):
    kind = answer.get("type")
    if kind == "choice":
        option, prob, conf = jev.top_choice(answer)
        return "%-24s %s (probability %.2f, confidence %.2f)" % (name, option, prob, conf)
    if kind == "score":
        return "%-24s score %s (confidence %s)" % (name, answer.get("score"), answer.get("confidence"))
    if kind == "noul":
        return "%-24s %.2f (0 = no, 1 = yes)" % (name, answer.get("noul", 0))
    return "%-24s %s" % (name, answer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question_set")
    parser.add_argument("--text")
    parser.add_argument("--file")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()
    if not args.text and not args.file:
        parser.error("give --text or --file")
    text = args.text if args.text else open(args.file, encoding="utf-8").read()
    if args.mock:
        os.environ.setdefault("JEV_BASE_URL", "http://127.0.0.1:8765")
        os.environ.setdefault("TYPESAFE_API_KEY", "mock")
    info, questions = load_set(args.question_set)
    try:
        answers, meta = jev.JevClient().ask(text, questions)
    except jev.JevError as err:
        print("FAILED:", err)
        return 1
    print("%s: %s" % (info.get("name"), info.get("description")))
    for name, answer in answers.items():
        print("  " + show(name, answer))
    print("  (%.2f seconds, %d input tokens)" % (meta["seconds"], meta["input_tokens"]))
    print("  thresholds to apply in your code: %s" % json.dumps(info.get("thresholds", {})))
    return 0


if __name__ == "__main__":
    sys.exit(main())
