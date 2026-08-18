#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEPLOYED_PATH_PREFIXES = (
	"apps/web >",
	"apps/media-server >",
	"packages/database >",
	"packages/web-backend >",
)
ALLOWED_IP_HIGH_ADVISORY = "GHSA-2p57-rm9w-gvfp"
ALLOWED_POSTCSS_HIGH_ADVISORY = "GHSA-r28c-9q8g-f849"
ALLOWED_IP_PATH_PARTS = (
	"apps/media-server >",
	"werift@0.23.0",
	"ip@2.0.1",
)


def _deployed_paths(advisory: dict[str, Any]) -> list[str]:
	paths: list[str] = []
	for finding in advisory.get("findings", []):
		for path in finding.get("paths", []):
			if path.startswith(DEPLOYED_PATH_PREFIXES):
				paths.append(path)
	return sorted(set(paths))


def _allowed_unpatched_ip(advisory: dict[str, Any], paths: list[str]) -> bool:
	if advisory.get("github_advisory_id") != ALLOWED_IP_HIGH_ADVISORY:
		return False
	if advisory.get("module_name") != "ip" or advisory.get("severity") != "high":
		return False
	if not paths:
		return False
	return all(all(part in path for part in ALLOWED_IP_PATH_PARTS) for path in paths)


def _allowed_build_only_postcss(advisory: dict[str, Any], paths: list[str]) -> bool:
	if advisory.get("github_advisory_id") != ALLOWED_POSTCSS_HIGH_ADVISORY:
		return False
	if advisory.get("module_name") != "postcss" or advisory.get("severity") != "high":
		return False
	if not paths:
		return False
	return all("tailwindcss@3.4.19" in path and "postcss@8.5.16" in path for path in paths)


def validate_audit(payload: dict[str, Any]) -> tuple[list[str], list[str]]:
	errors: list[str] = []
	accepted: list[str] = []
	advisories = payload.get("advisories")
	if not isinstance(advisories, dict):
		return ["audit JSON is missing the advisories object"], accepted

	for advisory in advisories.values():
		severity = advisory.get("severity")
		advisory_id = advisory.get("github_advisory_id") or str(advisory.get("id"))
		module = advisory.get("module_name", "unknown")
		if severity == "critical":
			errors.append(f"critical advisory {advisory_id} affects {module}")
			continue
		if severity != "high":
			continue
		paths = _deployed_paths(advisory)
		if not paths:
			continue
		if _allowed_unpatched_ip(advisory, paths):
			accepted.append(
				f"{ALLOWED_IP_HIGH_ADVISORY} ip@2.0.1 via media WebRTC; vulnerable isPublic API is not used",
			)
			continue
		if _allowed_build_only_postcss(advisory, paths):
			accepted.append(
				f"{ALLOWED_POSTCSS_HIGH_ADVISORY} postcss@8.5.16 via Tailwind build tooling; final runtime image scan must exclude it",
			)
			continue
		errors.append(
			f"unaccepted high advisory {advisory_id} affects {module}: " + "; ".join(paths),
		)

	return errors, accepted


def verify_allowed_api_is_unreachable(root: Path) -> list[str]:
	errors: list[str] = []
	package_root = root / "node_modules" / ".pnpm"
	for pattern in ("werift@0.23.0/node_modules/werift", "werift-ice@0.2.2/node_modules/werift-ice"):
		package = package_root / pattern
		if not package.is_dir():
			errors.append(f"missing installed package needed to verify {pattern}")
			continue
		for path in package.rglob("*"):
			if path.suffix not in {".js", ".mjs", ".cjs"} or not path.is_file():
				continue
			if ".isPublic(" in path.read_text(encoding="utf-8", errors="ignore"):
				errors.append(f"allowed vulnerable ip.isPublic API became reachable in {path.relative_to(root)}")
	return errors


def run_audit(root: Path) -> dict[str, Any]:
	result = subprocess.run(
		["pnpm", "audit", "--prod", "--audit-level=high", "--json"],
		cwd=root,
		capture_output=True,
		text=True,
		check=False,
	)
	try:
		return json.loads(result.stdout)
	except json.JSONDecodeError as error:
		detail = result.stderr.strip() or result.stdout[-1000:]
		raise RuntimeError(f"pnpm audit did not return valid JSON: {detail}") from error


def main() -> int:
	try:
		payload = run_audit(ROOT)
	except RuntimeError as error:
		print(f"AIBL PRODUCTION AUDIT ERROR {error}")
		return 1
	errors, accepted = validate_audit(payload)
	if any(item.startswith(ALLOWED_IP_HIGH_ADVISORY) for item in accepted):
		errors.extend(verify_allowed_api_is_unreachable(ROOT))
	if errors:
		for error in errors:
			print(f"AIBL PRODUCTION AUDIT ERROR {error}")
		return 1
	for item in accepted:
		print(f"AIBL PRODUCTION AUDIT ACCEPTED {item}")
	print(
		"AIBL PRODUCTION AUDIT PASS critical=0 unaccepted_deployed_high=0 "
		f"accepted_scoped_high={len(accepted)}",
	)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
