import { buildEnv } from "./build.ts";

export type SelfHostBrandProfile = {
	id: "cap" | "ai-build-lab";
	name: string;
	logoPath: string;
	manifestPath: string;
	themeColor: string;
};

const CAP_PROFILE: SelfHostBrandProfile = {
	id: "cap",
	name: "Cap",
	logoPath: "/favicon-32x32.png",
	manifestPath: "/site.webmanifest",
	themeColor: "#ffffff",
};

const AI_BUILD_LAB_PROFILE: SelfHostBrandProfile = {
	id: "ai-build-lab",
	name: "AI Build Lab",
	logoPath: "/aibl-brand.svg",
	manifestPath: "/aibl-site.webmanifest",
	themeColor: "#000000",
};

export const resolveSelfHostBrandProfile = (
	brand?: string,
): SelfHostBrandProfile =>
	brand === "ai-build-lab" ? AI_BUILD_LAB_PROFILE : CAP_PROFILE;

export const getSelfHostBrandProfile = () =>
	resolveSelfHostBrandProfile(buildEnv.NEXT_PUBLIC_SELF_HOST_BRAND);
