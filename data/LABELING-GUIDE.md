# How the 300 test replies were labelled

The test is only fair if the right answers are written down BEFORE any model sees the replies. Rules used (in this order):

1. **unsubscribe** beats everything. Any request to stop, remove, delete data or not be contacted again, in any wording or language, even if it
   is mixed with other content, buried inside a long message, or comes with a question ("how did you get my email? remove it").
2. **wrong_person** beats interest. If the sender says they are not the right person, the wrong company, or points or forwards to someone else, it is
   wrong_person even when they like the idea.
3. **not_interested**: a firm no (no need, already covered, policy, bad past experience, price far too high), without a request to stop all contact.
   "No thanks" is not_interested; "please don't contact me again" is unsubscribe.
4. **not_now**: open to it later, or timing, budget or a freeze blocks it. A dated "talk in December" is not_now (the sender plans a later talk).
5. **interested vs question**: interested if the sender clearly wants to talk, see a demo, get pricing or book a time (even with conditions or a
   question attached). question if they ask something before deciding and show no clear decision yet.

`also_acceptable` lists a second label that a reasonable person could also choose for genuinely ambiguous replies. `run_test.py` shows
both strict accuracy (only the main label counts) and lenient accuracy (the main label or an acceptable one).

Difficulty: `hard` replies were written by hand to be confusing (sarcasm, mixed intent, redirects, legal threats, one word answers needing context,
quoted threads, other languages, buried requests); `medium` replies are plain replies wrapped the way real inboxes look; `easy` are clear one liners.
All text is made up. Names and emails use example.test domains. Your own real replies will be messier still: test them too.
