import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";

describe("share theme bootstrap", () => {
	it("themes share and embed routes before hydration", () => {
		const source = fs.readFileSync(
			path.join(process.cwd(), "public/theme-script.js"),
			"utf8",
		);
		expect(source).toContain('pathname.indexOf("/s/") === 0');
		expect(source).toContain('pathname.indexOf("/embed/") === 0');
		expect(source).toContain("prefers-color-scheme: dark");
	});
});
