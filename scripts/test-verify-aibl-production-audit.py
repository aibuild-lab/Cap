#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("verify-aibl-production-audit.py")
SPEC = importlib.util.spec_from_file_location("verify_aibl_production_audit", MODULE_PATH)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def advisory(
	advisory_id: str,
	module: str,
	severity: str,
	path: str,
) -> dict[str, object]:
	return {
		"github_advisory_id": advisory_id,
		"module_name": module,
		"severity": severity,
		"findings": [{"version": "test", "paths": [path]}],
	}


class ProductionAuditTests(unittest.TestCase):
	def test_known_unpatched_ip_advisory_is_accepted_for_media_only(self) -> None:
		payload = {
			"advisories": {
				"1": advisory(
					AUDIT.ALLOWED_IP_HIGH_ADVISORY,
					"ip",
					"high",
					"apps/media-server > node-av@5.2.4 > werift@0.23.0 > ip@2.0.1",
				),
			},
		}
		errors, accepted = AUDIT.validate_audit(payload)
		self.assertEqual(errors, [])
		self.assertEqual(len(accepted), 1)

	def test_new_deployed_high_advisory_is_rejected(self) -> None:
		payload = {
			"advisories": {
				"1": advisory(
					"GHSA-new-risk",
					"example",
					"high",
					"apps/web > example@1.0.0",
				),
			},
		}
		errors, accepted = AUDIT.validate_audit(payload)
		self.assertEqual(accepted, [])
		self.assertTrue(any("GHSA-new-risk" in error for error in errors))

	def test_critical_advisory_is_rejected_even_outside_deployed_scope(self) -> None:
		payload = {
			"advisories": {
				"1": advisory(
					"GHSA-critical",
					"example",
					"critical",
					"apps/mobile > example@1.0.0",
				),
			},
		}
		errors, accepted = AUDIT.validate_audit(payload)
		self.assertEqual(accepted, [])
		self.assertTrue(any("critical" in error for error in errors))

	def test_known_advisory_is_rejected_outside_exact_media_path(self) -> None:
		payload = {
			"advisories": {
				"1": advisory(
					AUDIT.ALLOWED_IP_HIGH_ADVISORY,
					"ip",
					"high",
					"apps/web > werift@0.23.0 > ip@2.0.1",
				),
			},
		}
		errors, accepted = AUDIT.validate_audit(payload)
		self.assertEqual(accepted, [])
		self.assertTrue(errors)

	def test_build_only_postcss_advisory_is_accepted_for_tailwind_path(self) -> None:
		payload = {
			"advisories": {
				"1": advisory(
					AUDIT.ALLOWED_POSTCSS_HIGH_ADVISORY,
					"postcss",
					"high",
					"apps/web > @cap/ui@link:../../packages/ui > tailwindcss@3.4.19 > postcss@8.5.16",
				),
			},
		}
		errors, accepted = AUDIT.validate_audit(payload)
		self.assertEqual(errors, [])
		self.assertEqual(len(accepted), 1)

	def test_postcss_advisory_is_rejected_outside_exact_build_path(self) -> None:
		payload = {
			"advisories": {
				"1": advisory(
					AUDIT.ALLOWED_POSTCSS_HIGH_ADVISORY,
					"postcss",
					"high",
					"apps/web > runtime-package@1.0.0 > postcss@8.5.16",
				),
			},
		}
		errors, accepted = AUDIT.validate_audit(payload)
		self.assertEqual(accepted, [])
		self.assertTrue(errors)


if __name__ == "__main__":
	unittest.main()
