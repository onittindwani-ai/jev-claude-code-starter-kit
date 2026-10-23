"""A fake Jev for testing your code without a key or credits. It is NOT Jev and its answers are simple keyword guesses.

Usage:  python3 tools/mock_server.py 8765
Then:   JEV_BASE_URL=http://127.0.0.1:8765 TYPESAFE_API_KEY=test python3 tools/jev_check.py
It mirrors the response shape in the official quick start (choice, score, noul, usage).
"""
import json
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


def words(text):
    return set(re.findall(r"[a-z']+", str(text).lower()))


def answer_choice(state_words, question):
    options = question["criteria"]
    raw = {}
    for name, desc in options.items():
        hits = len(state_words & (words(name.replace("_", " ")) | words(desc)))
        raw[name] = hits + 0.1
    total = sum(raw.values())
    probs = {k: round(v / total, 2) for k, v in raw.items()}
    best = max(probs, key=probs.get)
    ordered = sorted(probs.values(), reverse=True)
    margin = ordered[0] - (ordered[1] if len(ordered) > 1 else 0)
    return {"type": "choice", "choice": best, "confidence": round(min(1.0, 0.4 + margin), 2), "probabilities": probs}


def answer_score(state_words, question):
    levels = question["criteria"]
    idx = min(len(levels) - 1, len(state_words) // 8)
    probs = {str(i): (0.8 if i == idx else round(0.2 / max(1, len(levels) - 1), 2)) for i in range(len(levels))}
    return {"type": "score", "score": float(idx), "confidence": 0.6,
            "legend": {str(i): d for i, d in enumerate(levels)}, "probabilities": probs}


def answer_noul(state_words, question):
    hits = len(state_words & words(question["instructions"]))
    return {"type": "noul", "noul": round(min(0.99, 0.1 + 0.2 * hits), 2)}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/v1/systemone":
            return self.reply(404, {"error": "not found"})
        if not self.headers.get("Authorization", "").startswith("Bearer "):
            return self.reply(401, {"error": "missing key"})
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        state_words = words(body.get("state", ""))
        answers = {}
        for name, q in body.get("questions", {}).items():
            kind = q.get("type")
            fn = {"choice": answer_choice, "score": answer_score, "noul": answer_noul}.get(kind)
            if not fn:
                return self.reply(422, {"error": "unknown question type %s" % kind})
            answers[name] = fn(state_words, q)
        tokens = max(1, len(str(body.get("state", ""))) // 4 + 60 * len(answers))
        self.reply(200, {"model": "mock-jev", "answers": answers, "usage": {"input_tokens": tokens, "output_tokens": 10}})

    def reply(self, code, payload):
        data = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def serve(port=8765):
    server = HTTPServer(("127.0.0.1", port), Handler)
    print("Mock Jev on http://127.0.0.1:%d (not the real model)" % port)
    server.serve_forever()


if __name__ == "__main__":
    serve(int(sys.argv[1]) if len(sys.argv) > 1 else 8765)
