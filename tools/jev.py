"""Tiny Jev client with no dependencies (Python 3.9+).

It calls the official API directly: POST https://api.typesafe.ai/v1/systemone
(docs.typesafe.ai/introduction/quickstart). Read your key from the TYPESAFE_API_KEY
environment variable or from a local .env file in the current directory. Never hard code a key.

Question helpers build the 3 question types the docs describe:
  choice(instructions, criteria)  pick 1 option; criteria is {option: description}
  score(instructions, levels)     rate on ordered levels; levels is a list of descriptions
  noul(instructions)              is this statement true of the state? (0 to 1)
"""
import json
import os
import time
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://api.typesafe.ai"
DEFAULT_MODEL = "jev-latest"  # pin a version (for example jev-1.13.0) when you need stable results
# Price on typesafe.ai on 2026-10-23: $42 per billion input tokens, output tokens free. Re check before you rely on it.
PRICE_PER_MILLION_INPUT_TOKENS = 0.042


class JevError(Exception):
    """Raised for any problem calling Jev, with a message a person can act on."""


def load_env_file(path=".env"):
    """Read KEY=VALUE lines from a local .env file into os.environ (existing variables win)."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def choice(instructions, criteria):
    return {"type": "choice", "instructions": instructions, "criteria": dict(criteria)}


def score(instructions, levels):
    return {"type": "score", "instructions": instructions, "criteria": list(levels)}


def noul(instructions):
    return {"type": "noul", "instructions": instructions}


class JevClient:
    def __init__(self, api_key=None, model=None, base_url=None, timeout=30, max_retries=4):
        load_env_file()
        self.api_key = api_key or os.environ.get("TYPESAFE_API_KEY", "")
        self.model = model or os.environ.get("JEV_MODEL", DEFAULT_MODEL)
        self.base_url = (base_url or os.environ.get("JEV_BASE_URL", DEFAULT_BASE_URL)).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        if not self.api_key:
            raise JevError(
                "No API key found. Set it in your own terminal (never in the AI chat): "
                'export TYPESAFE_API_KEY="your-key"  or put TYPESAFE_API_KEY=your-key in a local .env file.')

    def ask(self, state, questions):
        """Send 1 state and named questions in 1 request. Returns (answers, meta).

        meta has: model, input_tokens, output_tokens, seconds (time for the whole call including retries).
        """
        body = json.dumps({"state": state, "model": self.model, "questions": questions}).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + "/v1/systemone", data=body, method="POST",
            headers={"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json",
                     "User-Agent": "jev-claude-code-starter-kit/1.0"})
        started = time.time()
        last = None
        for attempt in range(self.max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    data = json.loads(response.read().decode("utf-8"))
                usage = data.get("usage", {})
                meta = {"model": data.get("model", self.model),
                        "input_tokens": usage.get("input_tokens", 0),
                        "output_tokens": usage.get("output_tokens", 0),
                        "seconds": time.time() - started}
                return data.get("answers", {}), meta
            except urllib.error.HTTPError as err:
                detail = err.read().decode("utf-8", "replace")[:300]
                if err.code in (429, 529) and attempt < self.max_retries:
                    time.sleep(2 ** attempt)  # 1, 2, 4, 8 seconds
                    last = "HTTP %s (retrying)" % err.code
                    continue
                raise JevError(explain_http_error(err.code, detail))
            except urllib.error.URLError as err:
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    last = str(err.reason)
                    continue
                raise JevError("Could not reach %s: %s" % (self.base_url, err.reason))
        raise JevError("Gave up after retries: %s" % last)


def explain_http_error(code, detail):
    hints = {
        400: "The request broke a rule (or the text is longer than the model's context). ",
        401: "The API key is missing, wrong or deleted. Create a new key in console.typesafe.ai/keys. ",
        413: "The request body is over 32 MiB. ",
        415: "Unsupported Content-Encoding. ",
        422: "Validation failed (a required field is missing or malformed). ",
        429: "Rate limit exceeded. Wait and retry, or lower the number of parallel requests. ",
        529: "TypeSafe is temporarily overloaded. Retry in a moment. ",
    }
    return "HTTP %s. %sServer said: %s" % (code, hints.get(code, ""), detail)


def top_choice(answer):
    """Return (option, probability, confidence) for a choice answer."""
    option = answer.get("choice")
    probs = answer.get("probabilities", {})
    return option, probs.get(option, 0.0), answer.get("confidence", 0.0)


def estimate_cost(input_tokens, price_per_million=PRICE_PER_MILLION_INPUT_TOKENS):
    """Cost in dollars for the input tokens (output is free at the time of writing)."""
    return input_tokens / 1_000_000 * price_per_million
