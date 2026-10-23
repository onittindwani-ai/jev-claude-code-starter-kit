"""Score leads with composite scoring: ask small separate questions, combine them with weights set in YOUR code.

Pattern: composite scoring (docs/PATTERNS.md). Change WEIGHTS to match your business.
Usage: python3 examples/lead_scoring.py [--mock]
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import jev  # noqa: E402

WEIGHTS = {"industry": 0.4, "role": 0.3, "intent": 0.3}
LEADS = [
    "Head of sales at a 40 person recruiting agency. Posted last week that they want to automate follow ups.",
    "Software engineer at a large bank, researching AI tools for fun.",
    "Owner of a 12 person roofing company. Asked a friend for lead generation help.",
]


def main():
    if "--mock" in sys.argv:
        os.environ.setdefault("JEV_BASE_URL", "http://127.0.0.1:8765")
        os.environ.setdefault("TYPESAFE_API_KEY", "mock")
    path = os.path.join(os.path.dirname(__file__), "..", "templates", "questions", "lead-fit-icp.json")
    with open(path) as handle:
        questions = json.load(handle)["questions"]
    client = jev.JevClient()
    try:
        for lead in LEADS:
            answers, _ = client.ask(lead, questions)
            fit = answers["industry_fit"]["probabilities"]
            industry = fit.get("strong", 0) + 0.5 * fit.get("maybe", 0)
            role = answers["role_relevance"].get("score", 0) / 2  # levels 0 to 2
            intent = answers["purchase_intent"].get("noul", 0)
            total = WEIGHTS["industry"] * industry + WEIGHTS["role"] * role + WEIGHTS["intent"] * intent
            print("%.2f  industry %.2f  role %.2f  intent %.2f  | %s" % (total, industry, role, intent, lead[:60]))
    except jev.JevError as err:
        print("FAILED:", err)
        return 1
    print("\nSorted by the number on the left. The weights are yours to change; Jev only answers the small questions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
