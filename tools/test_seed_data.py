"""Regression checks for precision, provenance and generated static outputs."""
from __future__ import annotations

import copy
import json
import unittest

import build_seed_data as builder


class SeedDataTests(unittest.TestCase):
    def setUp(self):
        self.catalogue = json.loads(builder.SOURCE.read_text(encoding="utf-8"))
        self.sample = {"schemaVersion": 2, "checkedAt": "2026-10-04",
                       "seeds": [copy.deepcopy(self.catalogue["seeds"][0])]}

    def test_catalogue_has_four_balanced_groups_and_unique_strings(self):
        rows = builder.validate(self.catalogue)
        self.assertEqual(len(rows), 400)
        self.assertEqual(len({row["seed"] for row in rows}), 400)
        for version in builder.VERSIONS:
            self.assertEqual(sum(row["version"] == version for row in rows), 100)
        release_rows = [row for row in rows if row["version"] == "26.3"]
        self.assertTrue(all(row["verification"] == "publisher-tested" for row in release_rows))
        self.assertTrue(all(row["sourceVersion"] == "Java 26.3" for row in release_rows))
        self.assertTrue(all(row["sourceUrl"] for row in rows))
        self.assertFalse(any(row["verification"] == "legacy-collection" for row in rows))

    def test_full_signed_64_bit_boundaries_preserve_strings(self):
        for seed in (str(-(2**63)), str(2**63 - 1)):
            with self.subTest(seed=seed):
                self.sample["seeds"][0]["seed"] = seed
                js = builder.render_outputs(self.sample)[builder.OUTPUT]
                self.assertIn(f'"seed": "{seed}"', js)

    def test_numbers_noncanonical_and_out_of_range_seeds_fail(self):
        for seed in (123, True, "01", "-0", "+1", "1e8", "١٢٣", str(2**63), str(-2**63 - 1)):
            with self.subTest(seed=seed):
                self.sample["seeds"][0]["seed"] = seed
                with self.assertRaises(ValueError):
                    builder.validate(self.sample)

    def test_duplicates_across_versions_fail(self):
        other = copy.deepcopy(self.sample["seeds"][0])
        other["version"] = "26.2"
        self.sample["seeds"].append(other)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            builder.validate(self.sample)

    def test_unsafe_or_credential_bearing_source_urls_fail(self):
        for url in ("javascript:alert(1)", "data:text/html,test", "http://example.com/",
                    "https://user:secret@example.com/", "https://example.com/\nscript"):
            with self.subTest(url=url):
                self.sample["seeds"][0]["sourceUrl"] = url
                with self.assertRaises(ValueError):
                    builder.validate(self.sample)

    def test_claimed_verification_requires_source_and_date(self):
        for key in ("sourceUrl", "sourceVersion", "checkedAt"):
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.sample)
                candidate["seeds"][0][key] = None
                with self.assertRaises(ValueError):
                    builder.validate(candidate)

    def test_generated_files_and_html_counts_are_current(self):
        outputs = builder.render_outputs(self.catalogue)
        for path, expected in outputs.items():
            self.assertEqual(path.read_text(encoding="utf-8"), expected, path.name)
        self.assertIn('data-stat="all">400</dd>', outputs[builder.HTML])
        self.assertIn("js/seeds.js?v=", outputs[builder.HTML])

    def test_source_notes_cannot_break_markdown_table(self):
        self.sample["seeds"][0]["description"] = "<script> | [link]"
        markdown = builder.render_outputs(self.sample)[builder.MARKDOWN]
        self.assertIn("&lt;script&gt; &#124; &#91;link&#93;", markdown)


if __name__ == "__main__":
    unittest.main()
