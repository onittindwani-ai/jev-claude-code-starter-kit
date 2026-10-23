import json
import os
import subprocess
import sys
import threading
import time
import unittest
from http.server import HTTPServer

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import baseline_rules  # noqa: E402
import jev  # noqa: E402
import make_dataset  # noqa: E402
import mock_server  # noqa: E402
import score  # noqa: E402

PORT = 8791


class MockServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", PORT), mock_server.Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        time.sleep(0.2)
        cls.client = jev.JevClient(api_key="test", base_url="http://127.0.0.1:%d" % PORT)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_three_question_types(self):
        answers, meta = self.client.ask("please unsubscribe me now", {
            "kind": jev.choice("type", {"unsubscribe": "asks to stop", "interested": "wants a demo"}),
            "level": jev.score("anger", ["calm", "angry"]),
            "stop": jev.noul("asks to stop"),
        })
        self.assertEqual(answers["kind"]["choice"], "unsubscribe")
        self.assertIn("probabilities", answers["kind"])
        self.assertIn("score", answers["level"])
        self.assertIn("noul", answers["stop"])
        self.assertGreater(meta["input_tokens"], 0)

    def test_bad_key_message(self):
        with self.assertRaises(jev.JevError):
            jev.JevClient(api_key="", base_url="http://127.0.0.1:%d" % PORT)

    def test_unknown_question_type(self):
        with self.assertRaises(jev.JevError) as ctx:
            self.client.ask("x", {"q": {"type": "bogus", "instructions": "x"}})
        self.assertIn("422", str(ctx.exception))

    def test_triage_end_to_end(self):
        env = dict(os.environ, JEV_BASE_URL="http://127.0.0.1:%d" % PORT, TYPESAFE_API_KEY="test")
        out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "triage_replies.py"),
                              os.path.join(ROOT, "data", "sample_10_replies.json"), "--out", "/tmp/jev_triage_test.csv"],
                             env=env, capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn("10 replies", out.stdout)

    def test_run_test_end_to_end(self):
        env = dict(os.environ, JEV_BASE_URL="http://127.0.0.1:%d" % PORT, TYPESAFE_API_KEY="test")
        out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "run_test.py"), "--limit", "24",
                              "--out", "/tmp/jev_results_test"], env=env, capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        for word in ("ACCURACY", "CALIBRATION", "HUMAN REVIEW RULE", "CONFUSION"):
            self.assertIn(word, out.stdout)
        self.assertTrue(os.path.exists("/tmp/jev_results_test/summary.json"))


class ExamplesAndTemplatesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", PORT + 1), mock_server.Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        time.sleep(0.2)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def env(self):
        return dict(os.environ, JEV_BASE_URL="http://127.0.0.1:%d" % (PORT + 1), TYPESAFE_API_KEY="test")

    def test_examples_run(self):
        for name in ("reply_router.py", "lead_scoring.py", "call_outcome_router.py", "guardrail_before_send.py"):
            out = subprocess.run([sys.executable, os.path.join(ROOT, "examples", name)], env=self.env(),
                                 capture_output=True, text=True, cwd=ROOT)
            self.assertEqual(out.returncode, 0, name + out.stdout + out.stderr)

    def test_morning_queue(self):
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "triage_replies.py"),
                        os.path.join(ROOT, "data", "sample_10_replies.json"), "--out", "/tmp/jev_q.csv"],
                       env=self.env(), capture_output=True, text=True, cwd=ROOT)
        out = subprocess.run([sys.executable, os.path.join(ROOT, "examples", "morning_review_queue.py"), "/tmp/jev_q.csv"],
                             capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("MORNING LIST", out.stdout)

    def test_every_question_set_is_valid(self):
        folder = os.path.join(ROOT, "templates", "questions")
        files = [f for f in os.listdir(folder) if f.endswith(".json")]
        self.assertGreaterEqual(len(files), 10)
        for name in files:
            with open(os.path.join(folder, name), encoding="utf-8") as handle:
                data = json.load(handle)
            for key in ("name", "description", "use_when", "questions"):
                self.assertIn(key, data, name)
            for qname, q in data["questions"].items():
                self.assertIn(q["type"], ("choice", "score", "noul"), name + qname)
                self.assertTrue(q["instructions"], name + qname)
                if q["type"] == "choice":
                    self.assertGreaterEqual(len(q["criteria"]), 2, name + qname)
                if q["type"] == "score":
                    self.assertIsInstance(q["criteria"], list, name + qname)
            out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "run_questions.py"),
                                  os.path.join(folder, name), "--text", "Sounds good, let's talk Thursday."],
                                 env=self.env(), capture_output=True, text=True, cwd=ROOT)
            self.assertEqual(out.returncode, 0, name + out.stdout + out.stderr)


class DatasetTest(unittest.TestCase):
    def test_counts_and_labels(self):
        rows = make_dataset.make_dataset(50, 7)
        self.assertEqual(len(rows), 300)
        counts = {}
        for r in rows:
            counts[r["label"]] = counts.get(r["label"], 0) + 1
        self.assertEqual(set(counts.values()), {50})
        self.assertEqual(len(counts), 6)

    def test_shipped_file_matches_generator(self):
        with open(os.path.join(ROOT, "data", "replies_300.jsonl"), encoding="utf-8") as handle:
            shipped = [json.loads(l) for l in handle if l.strip()]
        self.assertEqual(shipped, make_dataset.make_dataset(50, 7))

    def test_no_dashes_in_data(self):
        for name in ("replies_300.jsonl", "break_tests.json", "sample_10_replies.json"):
            with open(os.path.join(ROOT, "data", name), encoding="utf-8") as handle:
                text = handle.read()
            self.assertFalse(any(d in text for d in "\u2014\u2013"), name)


class ScoreTest(unittest.TestCase):
    def test_accuracy(self):
        self.assertEqual(score.accuracy(["a", "b"], ["a", "c"]), 0.5)

    def test_calibration_groups(self):
        rows = score.calibration(["a", "a", "a", "a"], ["a", "a", "b", "b"], [0.95, 0.96, 0.6, 0.62])
        shares = sorted(r["share_right"] for r in rows)
        self.assertEqual(shares, [0.0, 1.0])

    def test_review_split(self):
        split = score.review_split(["a", "a"], ["a", "b"], [0.9, 0.5], 0.8)
        self.assertEqual((split["automatic"], split["to_a_person"]), (1, 1))

    def test_baseline_rules(self):
        self.assertEqual(baseline_rules.classify("Please unsubscribe me"), "unsubscribe")
        self.assertEqual(baseline_rules.classify("I'm not the right person for this"), "wrong_person")
        self.assertEqual(baseline_rules.classify("Sounds good, let's talk"), "interested")


if __name__ == "__main__":
    unittest.main()
