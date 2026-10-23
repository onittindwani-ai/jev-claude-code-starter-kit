"""A plain keyword rule for the 6 reply types. It is the baseline every model must beat.

If a simple rule scores as well as Jev on your replies, you do not need a model for that step.
"""
import re

ORDER = ["unsubscribe", "wrong_person", "not_interested", "not_now", "question", "interested"]

PATTERNS = {
    "unsubscribe": r"unsubscribe|remove me|stop (emailing|contacting|sending)|take me off|do not contact|opt out",
    "wrong_person": r"wrong person|not the right person|no longer (here|with)|i don't handle|reach out to|forwarding you|talk to my colleague|not my area|left the company",
    "not_interested": r"not interested|no thanks|no thank you|not for us|we're all set|we are all set|pass on this|don't need",
    "not_now": r"not now|next quarter|check back|later this year|reach out (in|again)|bad timing|not a priority|in a few months|after the new year|circle back",
    "question": r"\?|how much|what does|do you (offer|integrate|support)|can you explain|which (plan|tool)|tell me more about",
    "interested": r"interested|sounds good|let's talk|lets talk|book a (call|time)|send (me )?(a )?(time|times|link|details)|i'd like to|demo|happy to chat|schedule",
}


def classify(text):
    lowered = text.lower()
    for label in ORDER:
        if re.search(PATTERNS[label], lowered):
            return label
    return "question"
