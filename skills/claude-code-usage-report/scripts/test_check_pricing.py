#!/usr/bin/env python3
"""Tests for check_pricing.py."""

import json
import tempfile
import unittest
from pathlib import Path

from check_pricing import format_pr_body


class TestFormatPrBody(unittest.TestCase):
    def test_no_alerts_file(self):
        """PR body without alerts file contains summary only."""
        body = format_pr_body(Path("/nonexistent/alerts.json"))
        self.assertIn("## Summary", body)
        self.assertIn("pricing.json", body)
        self.assertNotIn("Maintainer action required", body)

    def test_empty_alerts(self):
        """PR body with empty alerts has no maintainer section."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump({"structure_alerts": [], "extraction_errors": []}, f)
            path = Path(f.name)

        try:
            body = format_pr_body(path)
            self.assertNotIn("Maintainer action required", body)
        finally:
            path.unlink()

    def test_structure_alerts(self):
        """PR body includes structure alerts when present."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(
                {
                    "structure_alerts": ["Column order changed."],
                    "extraction_errors": [],
                },
                f,
            )
            path = Path(f.name)

        try:
            body = format_pr_body(path)
            self.assertIn("Maintainer action required", body)
            self.assertIn("Structure alerts", body)
            self.assertIn("Column order changed.", body)
            self.assertIn("Action items", body)
        finally:
            path.unlink()

    def test_extraction_errors(self):
        """PR body includes extraction errors when present."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(
                {
                    "structure_alerts": [],
                    "extraction_errors": ["  opus:current: no match"],
                },
                f,
            )
            path = Path(f.name)

        try:
            body = format_pr_body(path)
            self.assertIn("Maintainer action required", body)
            self.assertIn("Extraction errors", body)
            self.assertIn("opus:current: no match", body)
        finally:
            path.unlink()

    def test_logs_url_included(self):
        """PR body includes logs URL when provided."""
        body = format_pr_body(
            Path("/nonexistent/alerts.json"),
            logs_url="https://example.com/logs",
        )
        self.assertIn("https://example.com/logs", body)

    def test_logs_url_omitted(self):
        """PR body omits logs line when no URL provided."""
        body = format_pr_body(Path("/nonexistent/alerts.json"))
        self.assertNotIn("workflow logs", body)


if __name__ == "__main__":
    unittest.main()
