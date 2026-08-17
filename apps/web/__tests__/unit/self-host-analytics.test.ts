import { describe, expect, it } from "vitest";
import { isTinybirdConfigured } from "@/lib/video-views";

describe("self-host analytics selection", () => {
	it("uses Tinybird only when both settings are non-empty", () => {
		expect(isTinybirdConfigured("https://api.tinybird.co", "token")).toBe(true);
		expect(isTinybirdConfigured("https://api.tinybird.co", undefined)).toBe(
			false,
		);
		expect(isTinybirdConfigured(undefined, "token")).toBe(false);
		expect(isTinybirdConfigured(" ", "token")).toBe(false);
	});
});
