#!/usr/bin/env python3
"""Tests for usage_report.py."""

import json
import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from usage_report import (
    _resolve_pricing_key,
    clean_project_name,
    compute_model_cost,
    fmt_cost,
    fmt_num,
    generate_report,
    get_generation,
    get_model_family,
    get_pricing,
    load_pricing,
    model_display_name,
    parse_timestamp,
    process_files,
    scan_jsonl_files,
)


class TestGetModelFamily(unittest.TestCase):
    def test_opus(self):
        self.assertEqual(get_model_family("claude-opus-4-6"), "opus")
        self.assertEqual(get_model_family("claude-opus-4-1-20250805"), "opus")

    def test_sonnet(self):
        self.assertEqual(get_model_family("claude-sonnet-4-6"), "sonnet")
        self.assertEqual(get_model_family("claude-sonnet-4-0"), "sonnet")

    def test_haiku(self):
        self.assertEqual(get_model_family("claude-haiku-4-5-20251001"), "haiku")
        self.assertEqual(get_model_family("claude-haiku-3-5"), "haiku")

    def test_unknown(self):
        self.assertEqual(get_model_family("unknown-model"), "other")
        self.assertEqual(get_model_family(""), "other")


class TestGetGeneration(unittest.TestCase):
    def test_current(self):
        self.assertEqual(get_generation("claude-opus-4-6"), "current")
        self.assertEqual(get_generation("claude-sonnet-4-5"), "current")
        self.assertEqual(get_generation("claude-haiku-4-5-20251001"), "current")

    def test_previous(self):
        self.assertEqual(get_generation("claude-opus-4-1-20250805"), "previous")
        self.assertEqual(get_generation("claude-opus-4-0"), "previous")
        self.assertEqual(get_generation("claude-sonnet-4-20250514"), "previous")

    def test_legacy(self):
        self.assertEqual(get_generation("claude-3-5-haiku"), "legacy")

    def test_legacy_3(self):
        self.assertEqual(get_generation("claude-3-haiku-20240307"), "legacy-3")

    def test_unknown_defaults_to_current(self):
        self.assertEqual(get_generation("some-new-model"), "current")


class TestModelDisplayName(unittest.TestCase):
    def test_opus_current(self):
        self.assertEqual(model_display_name("claude-opus-4-6"), "Opus (4.5/4.6)")

    def test_sonnet_previous(self):
        self.assertEqual(model_display_name("claude-sonnet-4-0"), "Sonnet (4.0/4.1)")

    def test_haiku_legacy(self):
        self.assertEqual(model_display_name("claude-3-5-haiku"), "Haiku (3.5)")


class TestResolvePricingKey(unittest.TestCase):
    def test_opus_current(self):
        self.assertEqual(_resolve_pricing_key("Opus (4.5/4.6)"), ("opus", "current"))

    def test_haiku_legacy(self):
        self.assertEqual(_resolve_pricing_key("Haiku (3.5)"), ("haiku", "legacy"))

    def test_sonnet_previous(self):
        self.assertEqual(_resolve_pricing_key("Sonnet (4.0/4.1)"), ("sonnet", "previous"))

    def test_haiku_legacy_3(self):
        self.assertEqual(_resolve_pricing_key("Haiku (3)"), ("haiku", "legacy-3"))

    def test_unknown_defaults_sonnet_current(self):
        self.assertEqual(_resolve_pricing_key("Other (unknown)"), ("sonnet", "current"))


class TestGetPricing(unittest.TestCase):
    def test_returns_dict_with_expected_keys(self):
        pricing = get_pricing("claude-opus-4-6")
        self.assertIn("input", pricing)
        self.assertIn("output", pricing)
        self.assertIn("cache_read", pricing)
        self.assertIn("cache_write", pricing)

    def test_fallback_for_unknown(self):
        pricing = get_pricing("totally-unknown-model")
        self.assertIsInstance(pricing, dict)
        self.assertIn("input", pricing)


class TestCleanProjectName(unittest.TestCase):
    def test_strips_user_prefix(self):
        username = os.path.basename(os.path.expanduser("~"))
        dir_name = f"-Users-{username}-git-myorg-myrepo"
        result = clean_project_name(f"/some/path/{dir_name}")
        self.assertEqual(result, "git/myorg/myrepo")

    def test_no_prefix(self):
        result = clean_project_name("/some/path/simple-project")
        self.assertEqual(result, "simple/project")


class TestParseTimestamp(unittest.TestCase):
    def test_iso_format(self):
        ts = parse_timestamp("2026-03-15T10:30:00Z")
        self.assertIsNotNone(ts)
        self.assertEqual(ts.date(), datetime(2026, 3, 15).date())

    def test_with_timezone(self):
        ts = parse_timestamp("2026-03-15T10:30:00+02:00")
        self.assertIsNotNone(ts)

    def test_empty_string(self):
        self.assertIsNone(parse_timestamp(""))

    def test_none(self):
        self.assertIsNone(parse_timestamp(None))

    def test_invalid(self):
        self.assertIsNone(parse_timestamp("not-a-date"))


class TestFormatting(unittest.TestCase):
    def test_fmt_num(self):
        self.assertEqual(fmt_num(1234567), "1,234,567")
        self.assertEqual(fmt_num(0), "0")
        self.assertEqual(fmt_num(42), "42")

    def test_fmt_cost(self):
        self.assertEqual(fmt_cost(1234.56), "$1,234.56")
        self.assertEqual(fmt_cost(0), "$0.00")
        self.assertEqual(fmt_cost(0.1), "$0.10")


class TestComputeModelCost(unittest.TestCase):
    def test_opus_current(self):
        stats = {"input": 1_000_000, "output": 1_000_000,
                 "cache_read": 0, "cache_write": 0}
        cost = compute_model_cost("Opus (4.5/4.6)", stats)
        # input: 1M * $5/1M = $5, output: 1M * $25/1M = $25
        self.assertAlmostEqual(cost, 30.0, places=2)

    def test_zero_tokens(self):
        stats = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}
        cost = compute_model_cost("Opus (4.5/4.6)", stats)
        self.assertEqual(cost, 0.0)

    def test_cache_tokens(self):
        stats = {"input": 0, "output": 0,
                 "cache_read": 1_000_000, "cache_write": 1_000_000}
        cost = compute_model_cost("Opus (4.5/4.6)", stats)
        # cache_read: 1M * $0.50/1M = $0.50, cache_write: 1M * $6.25/1M = $6.25
        self.assertAlmostEqual(cost, 6.75, places=2)


class TestLoadPricing(unittest.TestCase):
    def test_loads_from_pricing_json(self):
        pricing, plans, fallback, updated = load_pricing()
        self.assertIn(("opus", "current"), pricing)
        self.assertIn(("sonnet", "current"), pricing)
        self.assertIn(("haiku", "current"), pricing)
        self.assertGreater(len(plans), 0)
        self.assertIn("input", fallback)

    def test_pricing_has_all_fields(self):
        pricing, _, _, _ = load_pricing()
        for key, vals in pricing.items():
            self.assertIn("input", vals, f"Missing 'input' for {key}")
            self.assertIn("output", vals, f"Missing 'output' for {key}")
            self.assertIn("cache_read", vals, f"Missing 'cache_read' for {key}")
            self.assertIn("cache_write", vals, f"Missing 'cache_write' for {key} (mapped from cache_write_5m)")

    def test_plans_have_name_and_monthly(self):
        _, plans, _, _ = load_pricing()
        for name, monthly in plans:
            self.assertIsInstance(name, str)
            self.assertIsInstance(monthly, (int, float))
            self.assertGreater(monthly, 0)


class TestPricingJsonSchema(unittest.TestCase):
    """Validate pricing.json structure and content."""

    def setUp(self):
        pricing_file = Path(__file__).resolve().parent / "pricing.json"
        with open(pricing_file) as f:
            self.data = json.load(f)

    def test_has_required_top_level_keys(self):
        self.assertIn("source", self.data)
        self.assertIn("updated", self.data)
        self.assertIn("models", self.data)
        self.assertIn("plans", self.data)

    def test_updated_is_valid_date(self):
        datetime.strptime(self.data["updated"], "%Y-%m-%d")

    def test_model_keys_have_family_and_generation(self):
        for key in self.data["models"]:
            parts = key.split(":")
            self.assertEqual(len(parts), 2, f"Invalid model key format: {key}")
            family, gen = parts
            self.assertIn(family, ["opus", "sonnet", "haiku"],
                          f"Unknown family in {key}")

    def test_model_values_have_required_fields(self):
        for key, vals in self.data["models"].items():
            for field in ("label", "input", "output", "cache_read", "cache_write_5m", "cache_write_1h"):
                self.assertIn(field, vals, f"Missing '{field}' in {key}")

    def test_all_prices_are_positive(self):
        for key, vals in self.data["models"].items():
            for field in ("input", "output", "cache_read", "cache_write_5m", "cache_write_1h"):
                self.assertGreater(vals[field], 0, f"{key}.{field} must be > 0")

    def test_cache_write_1h_greater_than_5m(self):
        for key, vals in self.data["models"].items():
            self.assertGreater(
                vals["cache_write_1h"], vals["cache_write_5m"],
                f"{key}: 1h cache write should cost more than 5m"
            )

    def test_plans_structure(self):
        self.assertIsInstance(self.data["plans"], list)
        self.assertGreater(len(self.data["plans"]), 0)
        for plan in self.data["plans"]:
            self.assertIn("name", plan)
            self.assertIn("monthly", plan)
            self.assertGreater(plan["monthly"], 0)


class TestProcessFiles(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.project_dir = os.path.join(self.tmpdir, "test-project")
        os.makedirs(self.project_dir)

    def _write_jsonl(self, filename, entries):
        filepath = os.path.join(self.project_dir, filename)
        with open(filepath, "w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")
        return filepath

    def test_processes_single_file(self):
        entry = {
            "timestamp": "2026-03-15T10:00:00Z",
            "message": {
                "model": "claude-opus-4-6",
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 200,
                    "cache_read_input_tokens": 50,
                    "cache_creation_input_tokens": 25,
                },
            },
        }
        filepath = self._write_jsonl("session.jsonl", [entry])
        files = [(filepath, self.project_dir, "main")]

        projects, daily, global_models = process_files(files)

        self.assertEqual(len(projects), 1)
        self.assertIn("Opus (4.5/4.6)", global_models)
        stats = global_models["Opus (4.5/4.6)"]
        self.assertEqual(stats["input"], 100)
        self.assertEqual(stats["output"], 200)
        self.assertEqual(stats["cache_read"], 50)
        self.assertEqual(stats["cache_write"], 25)

    def test_date_filter_excludes(self):
        entry = {
            "timestamp": "2026-01-01T10:00:00Z",
            "message": {
                "model": "claude-opus-4-6",
                "usage": {"input_tokens": 100, "output_tokens": 200,
                          "cache_read_input_tokens": 0,
                          "cache_creation_input_tokens": 0},
            },
        }
        filepath = self._write_jsonl("session.jsonl", [entry])
        files = [(filepath, self.project_dir, "main")]

        projects, daily, global_models = process_files(
            files, start_date=datetime(2026, 3, 1).date()
        )

        self.assertEqual(len(global_models), 0)

    def test_skips_zero_token_entries(self):
        entry = {
            "timestamp": "2026-03-15T10:00:00Z",
            "message": {
                "model": "claude-opus-4-6",
                "usage": {"input_tokens": 0, "output_tokens": 0,
                          "cache_read_input_tokens": 0,
                          "cache_creation_input_tokens": 0},
            },
        }
        filepath = self._write_jsonl("session.jsonl", [entry])
        files = [(filepath, self.project_dir, "main")]

        projects, daily, global_models = process_files(files)
        self.assertEqual(len(global_models), 0)

    def test_handles_malformed_json(self):
        filepath = os.path.join(self.project_dir, "bad.jsonl")
        with open(filepath, "w") as f:
            f.write("not json\n")
            f.write('{"timestamp":"2026-03-15T10:00:00Z","message":{"model":"claude-opus-4-6","usage":{"input_tokens":100,"output_tokens":50,"cache_read_input_tokens":0,"cache_creation_input_tokens":0}}}\n')
        files = [(filepath, self.project_dir, "main")]

        projects, daily, global_models = process_files(files)
        self.assertEqual(global_models["Opus (4.5/4.6)"]["input"], 100)

    def test_session_counting(self):
        entry = {
            "timestamp": "2026-03-15T10:00:00Z",
            "message": {
                "model": "claude-opus-4-6",
                "usage": {"input_tokens": 100, "output_tokens": 50,
                          "cache_read_input_tokens": 0,
                          "cache_creation_input_tokens": 0},
            },
        }
        f1 = self._write_jsonl("s1.jsonl", [entry])
        f2 = self._write_jsonl("s2.jsonl", [entry])
        files = [
            (f1, self.project_dir, "main"),
            (f2, self.project_dir, "subagent"),
        ]

        projects, _, _ = process_files(files)
        proj = projects[self.project_dir]
        self.assertEqual(len(proj["main_sessions"]), 1)
        self.assertEqual(len(proj["subagent_sessions"]), 1)


class TestScanJsonlFiles(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.project_dir = os.path.join(self.tmpdir, "test-project")
        os.makedirs(self.project_dir)

    def test_finds_main_sessions(self):
        filepath = os.path.join(self.project_dir, "session.jsonl")
        with open(filepath, "w") as f:
            f.write("{}\n")

        files = scan_jsonl_files(self.tmpdir)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0][2], "main")

    def test_finds_subagent_sessions(self):
        sub_dir = os.path.join(self.project_dir, "abc123", "subagents")
        os.makedirs(sub_dir)
        filepath = os.path.join(sub_dir, "sub.jsonl")
        with open(filepath, "w") as f:
            f.write("{}\n")

        files = scan_jsonl_files(self.tmpdir)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0][2], "subagent")

    def test_project_filter(self):
        other_dir = os.path.join(self.tmpdir, "other-project")
        os.makedirs(other_dir)
        with open(os.path.join(self.project_dir, "s.jsonl"), "w") as f:
            f.write("{}\n")
        with open(os.path.join(other_dir, "s.jsonl"), "w") as f:
            f.write("{}\n")

        files = scan_jsonl_files(self.tmpdir, "test-project")
        self.assertEqual(len(files), 1)
        self.assertIn("test-project", files[0][0])


class TestGenerateReport(unittest.TestCase):
    def test_report_contains_all_sections(self):
        global_models = {
            "Opus (4.5/4.6)": {
                "input": 1000, "output": 500,
                "cache_read": 2000, "cache_write": 100,
            }
        }
        daily = {"2026-03-15": {"tokens": 3600, "cost": 0.05}}
        projects = {
            "/tmp/proj": {
                "models": {"Opus (4.5/4.6)": {
                    "input": 1000, "output": 500,
                    "cache_read": 2000, "cache_write": 100,
                }},
                "main_sessions": {"s1.jsonl"},
                "subagent_sessions": set(),
            }
        }

        report = generate_report(projects, daily, global_models)

        self.assertIn("CLAUDE CODE USAGE REPORT", report)
        self.assertIn("PLAN ROI COMPARISON", report)
        self.assertIn("MODEL BREAKDOWN", report)
        self.assertIn("COST BREAKDOWN BY TYPE", report)
        self.assertIn("DAILY USAGE", report)
        self.assertIn("PER-PROJECT BREAKDOWN", report)
        self.assertIn("Pricing data:", report)

    def test_report_shows_all_plans(self):
        global_models = {
            "Opus (4.5/4.6)": {
                "input": 1_000_000, "output": 500_000,
                "cache_read": 0, "cache_write": 0,
            }
        }
        daily = {"2026-03-15": {"tokens": 1_500_000, "cost": 17.50}}
        projects = {
            "/tmp/proj": {
                "models": global_models,
                "main_sessions": {"s1.jsonl"},
                "subagent_sessions": set(),
            }
        }

        report = generate_report(projects, daily, global_models)

        self.assertIn("Pro", report)
        self.assertIn("Max 5x", report)
        self.assertIn("Max 20x", report)


if __name__ == "__main__":
    unittest.main()
