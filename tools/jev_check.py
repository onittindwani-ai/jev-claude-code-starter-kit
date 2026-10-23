"""Smoke test: 1 request with 3 questions. Run it right after setup to prove your key works.

Usage (from the kit folder):
  export TYPESAFE_API_KEY="your-key"      # run this in YOUR terminal, never in the AI chat
  python3 tools/jev_check.py
"""
import sys

import jev

STATE = ("Our API integration started returning 500 errors on every request about 20 minutes ago, "
         "and we can't process any customer orders until this is fixed.")

QUESTIONS = {
    "department": jev.choice("Which team should handle this", {
        "billing": "Payment or subscription issues",
        "technical": "Bugs or integration problems",
        "sales": "Pricing or account questions"}),
    "frustration": jev.score("How frustrated the customer appears", [
        "Calm, just stating facts", "Frustrated but civil", "Very angry, strong language"]),
    "is_urgent": jev.noul("The message conveys urgency or time-sensitivity"),
}


def main():
    try:
        client = jev.JevClient()
        answers, meta = client.ask(STATE, QUESTIONS)
    except jev.JevError as err:
        print("FAILED:", err)
        return 1
    print("Jev answered in %.2f seconds (model %s)" % (meta["seconds"], meta["model"]))
    option, prob, conf = jev.top_choice(answers["department"])
    print("  department : %s (probability %.2f, confidence %.2f)" % (option, prob, conf))
    print("  frustration: score %s of 2 (confidence %s)" % (answers["frustration"].get("score"),
                                                         answers["frustration"].get("confidence")))
    print("  is_urgent  : %s (0 = no, 1 = yes)" % answers["is_urgent"].get("noul"))
    cost = jev.estimate_cost(meta["input_tokens"])
    print("  tokens in/out: %s/%s  estimated cost: $%.6f" % (meta["input_tokens"], meta["output_tokens"], cost))
    print("OK: setup works. Next: python3 tools/triage_replies.py data/sample_10_replies.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
