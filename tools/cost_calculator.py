"""Estimate what a Jev workload costs and compare it with another model's price.

Usage:
  python3 tools/cost_calculator.py --calls-per-day 2000 --tokens-per-call 600
  python3 tools/cost_calculator.py --calls-per-day 2000 --tokens-per-call 600 --other-input-price 3.0 --other-output-price 15.0 --other-output-tokens 60
Prices are per million tokens in dollars. Jev on typesafe.ai (2026-10-23): $0.042 input, output free. Check the site before you rely on it.
"""
import argparse


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--calls-per-day", type=float, required=True)
    p.add_argument("--tokens-per-call", type=float, default=600, help="input tokens per call (text plus your questions)")
    p.add_argument("--jev-input-price", type=float, default=0.042)
    p.add_argument("--other-input-price", type=float, default=0.0)
    p.add_argument("--other-output-price", type=float, default=0.0)
    p.add_argument("--other-output-tokens", type=float, default=0.0)
    a = p.parse_args()
    jev_day = a.calls_per_day * a.tokens_per_call / 1e6 * a.jev_input_price
    print("Jev: $%.4f per day, $%.2f per 30 days, $%.5f per 1,000 calls" % (jev_day, jev_day * 30, jev_day / a.calls_per_day * 1000))
    if a.other_input_price:
        other_day = a.calls_per_day * (a.tokens_per_call * a.other_input_price + a.other_output_tokens * a.other_output_price) / 1e6
        print("Other model: $%.4f per day, $%.2f per 30 days" % (other_day, other_day * 30))
        if jev_day:
            print("Jev is %.0f times cheaper on price alone (your quality and your tests decide if that matters)" % (other_day / jev_day))


if __name__ == "__main__":
    main()
