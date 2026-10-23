"""Build the 300 reply test set: 50 per type, mixing hand written HARD replies, MEDIUM replies (real world wrapping) and EASY ones.

Usage: python3 tools/make_dataset.py --seed 7 --out data/replies_300.jsonl
Each line: {"id", "text", "label", "difficulty", "tags", "also_acceptable"}.
 - hard   : hand written in data/hard_replies_base.json (sarcasm, mixed intent, redirects, legal threats, tiny replies,
            quoted threads, other languages, buried requests). See data/LABELING-GUIDE.md for how labels were decided.
 - medium : plain replies wrapped the way real inboxes look (quoted original email, long signatures, legal footers,
            mobile signatures, typos, shouting, trailing noise).
 - easy   : clear one liners (a sanity check: any model should get these right).
Everything is made up. Write your own replies in the same format to test on your own style.
"""
import argparse
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = ["interested", "not_now", "not_interested", "wrong_person", "unsubscribe", "question"]
PER_TYPE = 50
MEDIUM_PER_TYPE = 15

OPENERS = ["Hi", "Hey", "Hello", "Thanks for your note", "Thanks for reaching out", "Hi there", "Good morning", ""]
SIGNOFFS = ["", "Thanks", "Best", "Regards", "Cheers"]
NAMES = ["Sam", "Priya", "Jordan", "Alex", "Maria", "Chen", "Lee", "Taylor", "Noor", "Dana"]
PRODUCTS = ["the lead system", "your service", "this tool", "the platform", "what you built", "the offer"]

BODIES = {
    "interested": ["This looks interesting. Can we book a call this week?", "Sounds good, send me a few times that work for you.",
                   "We have been looking for exactly this. I'd like to see a demo.", "Happy to chat. How about Thursday at 3?",
                   "Yes, I'm interested in {p}. Please send the details and a link to book.", "Let's talk. I can do Tuesday or Wednesday morning.",
                   "Great timing, we were about to start on this. Who should I loop in?", "I'd like to learn more and schedule 20 minutes next week."],
    "not_now": ["Interesting, but we are not looking at anything until next quarter. Check back then.", "Bad timing for us. Reach out again after the new year.",
                "Not a priority right now. Maybe in a few months.", "We just signed with another provider, so please circle back in six months.",
                "Can you follow up in the spring? We are full until then.", "Not now, but keep me on your list for later this year.",
                "We have a freeze on new tools until our budget review. Try me in January.", "Good idea but we cannot take it on this half. Ping me later."],
    "not_interested": ["Not interested, thanks.", "No thank you, this is not for us.", "We're all set on this, thanks.", "I'll pass on this one.",
                       "We don't need {p}. Good luck though.", "Thanks, but we are happy with what we have and are not looking to change.",
                       "This is not relevant to our business.", "No, thanks. We have an in house team for this."],
    "wrong_person": ["I'm not the right person for this. Try our head of operations.", "I no longer work at this company.",
                     "I don't handle this. Please reach out to {n} in marketing.", "Wrong person, I'm in finance. Forwarding you to the right contact.",
                     "You may want to talk to my colleague {n}, who owns this area.", "I left the company last month. Please contact the team inbox.",
                     "That's not my area. Our operations lead is the one to ask.", "Not the right contact for this, sorry. I'll forward your note."],
    "unsubscribe": ["Please unsubscribe me from this list.", "Remove me from your mailing list.", "Stop emailing me. Take me off your list now.",
                    "Do not contact me again.", "I did not sign up for these. Unsubscribe me immediately.", "Opt out please. No more messages.",
                    "Please stop sending me emails about {p}.", "Take me off every list you have, and do not contact this address again."],
    "question": ["How much does {p} cost?", "What does the setup involve and how long does it take?", "Do you integrate with HubSpot and Slack?",
                 "Can you explain how this is different from what we already use?", "Which plan would a team of 10 need?",
                 "Is there a free trial, and who owns the data?", "Can you tell me more about how the reporting works?", "Do you support calls as well as email?"],
}

QUOTED = ["On {d}, Alex <alex@sendmail.example.test> wrote:\n> Hi, I noticed your team is hiring for sales. We help teams follow up with every lead automatically.\n> Would a short call next week be useful?\n> Best, Alex",
          "On {d}, Alex wrote:\n> Quick follow up on my note below. Did you get a chance to look at it?\n> \n> On {d2}, Alex wrote:\n> We build AI systems that sort and answer sales replies. Worth 15 minutes?"]
SIGNATURES = ["\n\n--\n{n} | Operations Manager\nBluebird Logistics Ltd | 12 Harbour Street | +1 415 555 0107\nwww.bluebird.example.test",
              "\n\nBest regards,\n{n}\nDirector of Partnerships\nCedar and Pine Co. | Follow us on LinkedIn | Please consider the environment before printing this email"]
FOOTERS = ["\n\nCONFIDENTIALITY NOTICE: This email and any attachments are intended solely for the named recipient and may contain confidential or privileged information. If you received it in error, please notify the sender and delete it.",
           "\n\nThis message was sent from a monitored mailbox. Opinions are the sender's own and do not represent the company."]
MOBILE = ["\n\nSent from my iPhone", "\n\nSent from my Android, please excuse typos"]
DATES = ["Mon, Oct 19, 2026 at 9:14 AM", "Tue, Oct 20, 2026 at 4:02 PM", "Fri, Oct 16, 2026 at 11:30 AM"]


def typo(text, rng):
    words = text.split(" ")
    for i in rng.sample(range(len(words)), k=min(2, len(words))):
        w = words[i]
        if len(w) > 4:
            j = rng.randrange(1, len(w) - 2)
            words[i] = w[:j] + w[j + 1] + w[j] + w[j + 2:]
    return " ".join(words)


def easy_reply(label, rng):
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
    return text.strip(), []


def medium_reply(label, rng):
    body = rng.choice(BODIES[label]).format(p=rng.choice(PRODUCTS), n=rng.choice(NAMES))
    tags = []
    kinds = rng.sample(["quoted_thread", "signature", "footer", "mobile", "typos", "shouting"], k=rng.choice([2, 3]))
    if "typos" in kinds:
        body = typo(body, rng)
        tags.append("typos")
    if "shouting" in kinds and label in ("unsubscribe", "not_interested"):
        body = body.upper()
        tags.append("shouting")
    text = body
    if "signature" in kinds:
        text += rng.choice(SIGNATURES).format(n=rng.choice(NAMES))
        tags.append("long_signature")
    if "footer" in kinds:
        text += rng.choice(FOOTERS)
        tags.append("legal_footer")
    if "mobile" in kinds:
        text += rng.choice(MOBILE)
        tags.append("mobile")
    if "quoted_thread" in kinds:
        q = rng.choice(QUOTED).format(d=rng.choice(DATES), d2=rng.choice(DATES))
        text += "\n\n" + q
        tags.append("quoted_thread")
    return text, tags


def make_dataset(seed=7):
    rng = random.Random(seed)
    with open(os.path.join(HERE, "..", "data", "hard_replies_base.json"), encoding="utf-8") as handle:
        hard = json.load(handle)
    rows = []
    for label in LABELS:
        hard_rows = [h for h in hard if h["label"] == label]
        for h in hard_rows:
            rows.append({"text": h["text"], "label": label, "difficulty": "hard", "tags": h["tags"], "also_acceptable": h["also_acceptable"]})
        for _ in range(MEDIUM_PER_TYPE):
            text, tags = medium_reply(label, rng)
            rows.append({"text": text, "label": label, "difficulty": "medium", "tags": tags, "also_acceptable": []})
        easy_count = PER_TYPE - len(hard_rows) - MEDIUM_PER_TYPE
        for _ in range(easy_count):
            text, tags = easy_reply(label, rng)
            rows.append({"text": text, "label": label, "difficulty": "easy", "tags": tags, "also_acceptable": []})
    rng.shuffle(rows)
    return [dict(id=i, **r) for i, r in enumerate(rows, 1)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--out", default="data/replies_300.jsonl")
    args = parser.parse_args()
    rows = make_dataset(args.seed)
    with open(args.out, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    from collections import Counter
    print("wrote %d replies to %s: %s" % (len(rows), args.out, dict(Counter(r["difficulty"] for r in rows))))


if __name__ == "__main__":
    main()
