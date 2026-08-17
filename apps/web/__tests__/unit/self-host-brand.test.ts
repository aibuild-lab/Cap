import { resolveSelfHostBrandProfile } from "@cap/env";
import { describe, expect, it } from "vitest";

describe("self-host brand profile", () => {
	it("selects the AI Build Lab assets only for the explicit profile", () => {
		expect(resolveSelfHostBrandProfile("ai-build-lab")).toMatchObject({
			id: "ai-build-lab",
			name: "AI Build Lab",
			logoPath: "/aibl-brand.svg",
		});
	});

	it("preserves Cap branding for every other build", () => {
		expect(resolveSelfHostBrandProfile()).toMatchObject({
			id: "cap",
			name: "Cap",
		});
		expect(resolveSelfHostBrandProfile("unknown")).toMatchObject({ id: "cap" });
	});
});
