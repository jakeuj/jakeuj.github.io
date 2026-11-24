"""Tests for scripts/algolia_index.py."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import algolia_index as index  # noqa: E402


def record(content, **extra):
    return {"objectID": "_a.html#", "content": content, "contentBoost": 1, **extra}


class AlgoliaIndexTest(unittest.TestCase):
    def run_dir(self, files):
        with tempfile.TemporaryDirectory() as folder:
            for name, data in files.items():
                (Path(folder) / name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            index.normalize(folder)
            return {name: json.loads((Path(folder) / name).read_text(encoding="utf-8")) for name in files}

    def test_drops_boost_and_keeps_small_records(self):
        out = self.run_dir({"a.json": record("短內容")})
        self.assertEqual(out["a.json"], {"objectID": "_a.html#", "content": "短內容"})

    def test_trims_oversized_records_to_the_limit(self):
        out = self.run_dir({"a.json": record("設定範本" * 4000)})
        self.assertLessEqual(index.size(out["a.json"]), index.LIMIT)
        self.assertTrue(out["a.json"]["content"].endswith("…"))
        self.assertGreater(index.size(out["a.json"]), index.LIMIT - 200)

    def test_json_escaping_is_counted(self):
        out = self.run_dir({"a.json": record('"\\' * 6000)})
        self.assertLessEqual(index.size(out["a.json"]), index.LIMIT)

    def test_lists_and_multiple_files(self):
        out = self.run_dir({"a.json": [record("a"), record("文" * 5000)], "b.json": record("b")})
        self.assertNotIn("contentBoost", out["a.json"][0])
        self.assertLessEqual(index.size(out["a.json"][1]), index.LIMIT)

    def test_record_without_content_is_an_error(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / "a.json").write_text(json.dumps({"objectID": "x" * 12000}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "no content"):
                index.normalize(folder)


if __name__ == "__main__":
    unittest.main()
