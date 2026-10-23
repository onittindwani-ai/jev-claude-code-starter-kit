"""Run the Jev reply test: Jev versus a plain keyword rule (and any other model you add).

What it measures: accuracy, per type results, a confusion matrix, speed, cost, and whether Jev's
confidence is honest (calibration), plus what happens if low confidence answers go to a person.

Usage:
  python3 tools/run_test.py                                   # all 300 replies, real Jev
  python3 tools/run_test.py --limit 30                        # a cheap first try
  python3 tools/run_test.py --compare claude_predictions.csv  # add another model's answers (columns id,label)
  python3 tools/run_test.py --mock                            # dry run with the local fake (no key)
Results are saved in results/ (a JSON summary and a CSV of every answer).
"""
import argparse
import csv
import json
import os
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import baseline_rules
import jev
import score
from triage_replies import REPLY_TYPES, questions

LABELS = list(REPLY_TYPES)


def load_dataset(path):
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_predictions(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return {str(row["id"]): row["label"].strip() for row in csv.DictReader(handle)}


def run_jev(rows, workers):
    client = jev.JevClient()

    def one(row):
        answers, meta = client.ask(row["text"], questions())
        kind, prob, conf = jev.top_choice(answers["reply_type"])
        return {"id": row["id"], "pred": kind, "prob": prob, "conf": conf, "meta": meta}

    started = time.time()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(one, rows))
    return results, time.time() - started


def table(title, rows):
    print("\n" + title)
    for line in rows:
        print("  " + line)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="data/replies_300.jsonl")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--workers", type=int, default=4, help="parallel requests (the docs do not publish a rate limit)")
    parser.add_argument("--compare", help="CSV of another model's answers: id,label")
    parser.add_argument("--review-below", type=float, default=0.8)
    parser.add_argument("--out", default="results")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()
    if args.mock:
        os.environ.setdefault("JEV_BASE_URL", "http://127.0.0.1:8765")
        os.environ.setdefault("TYPESAFE_API_KEY", "mock")

    rows = load_dataset(args.data)
    if args.limit:
        rows = rows[:args.limit]
    truth = [r["label"] for r in rows]
    try:
        results, wall = run_jev(rows, args.workers)
    except jev.JevError as err:
        print("FAILED:", err)
        return 1

    jev_pred = [r["pred"] for r in results]
    conf = [r["conf"] for r in results]
    base_pred = [baseline_rules.classify(r["text"]) for r in rows]
    seconds = [r["meta"]["seconds"] for r in results]
    tokens = sum(r["meta"]["input_tokens"] for r in results)
    cost = jev.estimate_cost(tokens)
    models = {r["meta"]["model"] for r in results}

    print("Replies tested: %d   Jev model(s): %s" % (len(rows), ", ".join(sorted(models))))
    table("ACCURACY", ["Jev           : %5.1f%%" % (100 * score.accuracy(truth, jev_pred)),
                       "Keyword rule  : %5.1f%%" % (100 * score.accuracy(truth, base_pred))])
    summary = {"replies": len(rows), "models": sorted(models), "jev_accuracy": score.accuracy(truth, jev_pred),
               "rule_accuracy": score.accuracy(truth, base_pred)}
    if args.compare:
        other = load_predictions(args.compare)
        other_pred = [other.get(str(r["id"]), "") for r in rows]
        summary["other_accuracy"] = score.accuracy(truth, other_pred)
        print("  Other model   : %5.1f%%  (%s)" % (100 * summary["other_accuracy"], args.compare))

    table("SPEED AND COST (Jev)", [
        "Average per reply : %.0f ms   Median: %.0f ms   Slowest: %.0f ms" % (
            1000 * statistics.mean(seconds), 1000 * statistics.median(seconds), 1000 * max(seconds)),
        "Whole run (%d parallel): %.1f s" % (args.workers, wall),
        "Input tokens: %d   Estimated cost: $%.5f   Per 1,000 replies: $%.4f" % (
            tokens, cost, cost / len(rows) * 1000 if rows else 0)])
    summary.update({"avg_ms": 1000 * statistics.mean(seconds), "cost_total": cost,
                    "cost_per_1000": cost / len(rows) * 1000 if rows else 0})

    per = score.per_label(truth, jev_pred, LABELS)
    table("PER TYPE (Jev)", ["%-15s precision %.2f  recall %.2f  (n=%d)" % (k, v["precision"], v["recall"], v["support"])
                             for k, v in per.items()])
    matrix = score.confusion(truth, jev_pred, LABELS)
    table("CONFUSION (rows = right answer, columns = Jev)", [
        "%-15s " % "" + " ".join("%7s" % l[:7] for l in LABELS)] + [
        "%-15s " % t + " ".join("%7d" % matrix[t][p] for p in LABELS) for t in LABELS])

    cal = score.calibration(truth, jev_pred, conf)
    table("CALIBRATION: when Jev is X sure, how often is it right?", [
        "confidence %-12s answers %3d   mean confidence %.2f   share right %.2f" % (
            c["range"], c["answers"], c["mean_confidence"], c["share_right"]) for c in cal])
    split = score.review_split(truth, jev_pred, conf, args.review_below)
    table("HUMAN REVIEW RULE (confidence below %.2f goes to a person)" % args.review_below, [
        "Automatic: %d   To a person: %d   Accuracy of the automatic ones: %.1f%%" % (
            split["automatic"], split["to_a_person"], 100 * split["automatic_accuracy"])])
    summary.update({"calibration": cal, "review_rule": split})

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    with open(os.path.join(args.out, "answers.csv"), "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "right_answer", "jev", "confidence", "keyword_rule", "seconds"])
        for row, r, b in zip(rows, results, base_pred):
            writer.writerow([row["id"], row["label"], r["pred"], round(r["conf"], 3), b, round(r["meta"]["seconds"], 3)])
    print("\nSaved results/summary.json and results/answers.csv. Remember: made up replies written to be clear are easier "
          "than real inbox mail, so test your own replies too.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
