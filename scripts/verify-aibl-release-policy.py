#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED_ACTION_RE = re.compile(r"^\s*uses:\s*([^\s]+)@([0-9a-f]{40})(?:\s+#.*)?$")
WORKFLOWS = (
	".github/workflows/aibl-release-policy.yml",
	".github/workflows/docker-build-web.yml",
	".github/workflows/docker-build-media-server.yml",
)


def validate(root: Path) -> list[str]:
	errors: list[str] = []
	for relative in WORKFLOWS:
		path = root / relative
		if not path.is_file():
			errors.append(f"missing workflow {relative}")
			continue
		for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
			if "uses:" not in line or "uses: ./" in line:
				continue
			if not PINNED_ACTION_RE.fullmatch(line):
				errors.append(f"{relative}:{line_number}: action must be pinned to a 40-character commit")

	for relative in (
		".github/workflows/docker-build-web.yml",
		".github/workflows/docker-build-media-server.yml",
	):
		text = (root / relative).read_text(encoding="utf-8")
		for required in (
			"attest-build-provenance@",
			"anchore/sbom-action@",
			"actions/attest@",
			"push-to-registry: true",
			"platforms: linux/amd64",
			"python3 scripts/verify-aibl-production-audit.py",
			"aquasecurity/trivy-action@",
			"severity: CRITICAL",
			"severity: HIGH",
		):
			if required not in text:
				errors.append(f"{relative}: missing {required}")

	release_policy = (root / ".github/workflows/aibl-release-policy.yml").read_text(encoding="utf-8")
	for required in (
		"bun test",
		"pnpm --filter=@cap/web build",
		"NODE_ENV: production",
		"pnpm --filter=@cap/web exec vitest run",
		"python3 scripts/verify-aibl-production-audit.py",
		"python3 scripts/test-verify-aibl-production-audit.py",
	):
		if required not in release_policy:
			errors.append(f".github/workflows/aibl-release-policy.yml: missing {required}")

	for relative in ("apps/web/Dockerfile", "apps/media-server/Dockerfile.standalone"):
		text = (root / relative).read_text(encoding="utf-8")
		from_lines = [line for line in text.splitlines() if line.startswith("FROM ")]
		stage_aliases: set[str] = set()
		for from_line in from_lines:
			parts = from_line.split()
			image = parts[1]
			if image not in stage_aliases and not re.search(r"@sha256:[0-9a-f]{64}$", image):
				errors.append(
					f"{relative}: every external base image must be pinned to a sha256 digest"
				)
			if len(parts) >= 4 and parts[-2].lower() == "as":
				stage_aliases.add(parts[-1])
		if not re.search(r"(?m)^USER\s+[1-9][0-9]*(?::[1-9][0-9]*)?\s*$", text):
			errors.append(f"{relative}: final image must declare a numeric non-root USER")

	self_host = (root / "AIBL-SELF-HOST.md").read_text(encoding="utf-8")
	if "https://github.com/aibuild-lab/Cap" not in self_host:
		errors.append("AIBL-SELF-HOST.md: missing public AGPL source link")
	return errors


def main() -> int:
	errors = validate(ROOT)
	if errors:
		for error in errors:
			print(f"AIBL RELEASE POLICY ERROR {error}")
		return 1
	print("AIBL RELEASE POLICY PASS provenance=REQUIRED sbom=REQUIRED actions=PINNED")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
