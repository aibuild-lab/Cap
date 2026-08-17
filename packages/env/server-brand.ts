import { getSelfHostBrandProfile } from "./brand.ts";
import { serverEnv } from "./server.ts";

export const getSelfHostBrandName = () =>
	serverEnv().SELF_HOST_BRAND_NAME?.trim() || getSelfHostBrandProfile().name;

export const getSelfHostSourceUrl = () =>
	serverEnv().SELF_HOST_SOURCE_URL?.trim() || null;

export const getSelfHostEmailLogoUrl = () =>
	new URL(getSelfHostBrandProfile().logoPath, serverEnv().WEB_URL).toString();
