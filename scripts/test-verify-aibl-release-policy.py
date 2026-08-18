#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("verify-aibl-release-policy.py")
SPEC = importlib.util.spec_from_file_location("verify_aibl_release_policy", MODULE_PATH)
assert SPEC and SPEC.loader
POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLICY)


class ReleasePolicyTests(unittest.TestCase):
	def test_repository_policy_passes(self) -> None:
		self.assertEqual(POLICY.validate(POLICY.ROOT), [])

	def test_mutable_action_reference_is_rejected(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			for relative in POLICY.WORKFLOWS:
				destination = root / relative
				destination.parent.mkdir(parents=True, exist_ok=True)
				shutil.copy2(POLICY.ROOT / relative, destination)
			for relative in (
				"apps/web/Dockerfile",
				"apps/media-server/Dockerfile.standalone",
				"AIBL-SELF-HOST.md",
			):
				destination = root / relative
				destination.parent.mkdir(parents=True, exist_ok=True)
				shutil.copy2(POLICY.ROOT / relative, destination)
			workflow = root / ".github/workflows/docker-build-web.yml"
			workflow.write_text(
				workflow.read_text(encoding="utf-8").replace(
					"actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
					"actions/checkout@v4",
				),
				encoding="utf-8",
			)
			errors = POLICY.validate(root)
			self.assertTrue(any("40-character commit" in error for error in errors))

	def test_mutable_base_image_reference_is_rejected(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			for relative in POLICY.WORKFLOWS:
				destination = root / relative
				destination.parent.mkdir(parents=True, exist_ok=True)
				shutil.copy2(POLICY.ROOT / relative, destination)
			for relative in (
				"apps/web/Dockerfile",
				"apps/media-server/Dockerfile.standalone",
				"AIBL-SELF-HOST.md",
			):
				destination = root / relative
				destination.parent.mkdir(parents=True, exist_ok=True)
				shutil.copy2(POLICY.ROOT / relative, destination)
			web_dockerfile = root / "apps/web/Dockerfile"
			lines = web_dockerfile.read_text(encoding="utf-8").splitlines()
			from_index = next(index for index, line in enumerate(lines) if line.startswith("FROM "))
			lines[from_index] = "FROM node:24-alpine AS base"
			web_dockerfile.write_text("\n".join(lines) + "\n", encoding="utf-8")
			errors = POLICY.validate(root)
			self.assertTrue(any("base image must be pinned" in error for error in errors))


if __name__ == "__main__":
	unittest.main()
