"""Make a made up set of sales replies with a known answer for each (6 types). No real customer data.

Usage: python3 tools/make_dataset.py --per-type 50 --seed 7 --out data/replies_300.jsonl
Each line: {"id": 1, "text": "...", "label": "interested"}
Write your own replies in the same format to test on your own style.
"""
import argparse
import json
import random

OPENERS = ["Hi", "Hey", "Hello", "Thanks for your note", "Thanks for reaching out", "Hi there", "Good morning", ""]
SIGNOFFS = ["", "Thanks", "Best", "Regards", "Cheers", "Sent from my phone"]
PRODUCTS = ["the lead system", "your service", "this tool", "the platform", "what you built", "the offer"]
NAMES = ["Sam", "Priya", "Jordan", "Alex", "Maria", "Chen", "Lee", "Taylor", "Noor", "Dana"]

BODIES = {
    "interested": [
        "This looks interesting. Can we book a call this week?",
        "Sounds good, send me a few times that work for you.",
        "We have been looking for exactly this. I'd like to see a demo.",
        "Happy to chat. How about Thursday at 3?",
        "Yes, I'm interested in {p}. Please send the details and a link to book.",
        "Let's talk. I can do Tuesday or Wednesday morning.",
        "Great timing, we were about to start on this. Who should I loop in?",
        "I'd like to learn more and schedule 20 minutes next week.",
    ],
    "not_now": [
        "Interesting, but we are not looking at anything until next quarter. Check back then.",
        "Bad timing for us. Reach out again after the new year.",
        "Not a priority right now. Maybe in a few months.",
        "We just signed with another provider, so please circle back in six months.",
        "Can you follow up in the spring? We are full until then.",
        "Not now, but keep me on your list for later this year.",
        "We have a freeze on new tools until our budget review. Try me in January.",
        "Good idea but we cannot take it on this half. Ping me later.",
    ],
    "not_interested": [
        "Not interested, thanks.",
        "No thank you, this is not for us.",
        "We're all set on this, please don't follow up.",
        "I'll pass on this one.",
        "We don't need {p}. Good luck though.",
        "Thanks, but we are happy with what we have and are not looking to change.",
        "This is not relevant to our business.",
        "No, thanks. We have an in house team for this.",
    ],
    "wrong_person": [
        "I'm not the right person for this. Try our head of operations.",
        "I no longer work at this company.",
        "I don't handle this. Please reach out to {n} in marketing.",
        "Wrong person, I'm in finance. Forwarding you to the right contact.",
        "You may want to talk to my colleague {n}, who owns this area.",
        "I left the company last month. Please remove this address and contact the team inbox.",
        "That's not my area. Our operations lead is the one to ask.",
        "Not the right contact for this, sorry. I'll forward your note.",
    ],
    "unsubscribe": [
        "Please unsubscribe me from this list.",
        "Remove me from your mailing list.",
        "Stop emailing me. Take me off your list now.",
        "Do not contact me again.",
        "I did not sign up for these. Unsubscribe me immediately.",
        "Opt out please. No more messages.",
        "Please stop sending me emails about {p}.",
        "Take me off every list you have, and do not contact this address again.",
    ],
    "question": [
        "How much does {p} cost?",
        "What does the setup involve and how long does it take?",
        "Do you integrate with HubSpot and Slack?",
        "Can you explain how this is different from what we already use?",
        "Which plan would a team of 10 need?",
        "Is there a free trial, and who owns the data?",
        "Can you tell me more about how the reporting works?",
        "Do you support calls as well as email?",
    ],
}


def make_reply(label, rng):
    body = rng.choice(BODIES[label]).format(p=rng.choice(PRODUCTS), n=rng.choice(NAMES))
    opener = rng.choice(OPENERS)
    if opener:
        first = body.split(" ")[0]
        if first not in ("I", "I'm", "I'd", "I'll", "I've") and not first.isupper():
            body = body[0].lower() + body[1:]
        text = opener + ", " + body
    else:
        text = body
    signoff = rng.choice(SIGNOFFS)
    if signoff:
        text += "\n" + signoff
        if rng.random() < 0.5:
            text += ", " + rng.choice(NAMES)
    return text.strip()


def make_dataset(per_type=50, seed=7):
    rng = random.Random(seed)
    rows = []
    for label in BODIES:
        for _ in range(per_type):
            rows.append({"text": make_reply(label, rng), "label": label})
    rng.shuffle(rows)
    for i, row in enumerate(rows, 1):
        row["id"] = i
    return [{"id": r["id"], "text": r["text"], "label": r["label"]} for r in rows]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-type", type=int, default=50)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--out", default="data/replies_300.jsonl")
    args = parser.parse_args()
    rows = make_dataset(args.per_type, args.seed)
    with open(args.out, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("wrote %d replies to %s" % (len(rows), args.out))


if __name__ == "__main__":
    main()
