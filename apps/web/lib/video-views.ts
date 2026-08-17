import { db } from "@cap/database";
import { videoPageViews } from "@cap/database/schema";
import { serverEnv } from "@cap/env";
import type { Organisation, User, Video } from "@cap/web-domain";
import { and, eq, gte, sql } from "drizzle-orm";

export const isTinybirdConfigured = (host?: string, token?: string) =>
	Boolean(host?.trim() && token?.trim());

export const tinybirdConfigured = () => {
	const env = serverEnv();
	return isTinybirdConfigured(env.TINYBIRD_HOST, env.TINYBIRD_TOKEN);
};

export interface VideoPageViewRow {
	videoId: Video.VideoId;
	orgId?: string | null;
	sessionId: string;
	userId?: string | null;
	pathname?: string | null;
	country?: string | null;
	region?: string | null;
	city?: string | null;
	browser?: string | null;
	device?: string | null;
	os?: string | null;
	timestamp: Date;
}

const NANO_ID_MAX_LENGTH = 15;
const asNanoIdOrNull = (value?: string | null) =>
	value && value.length <= NANO_ID_MAX_LENGTH ? value : null;

export const insertVideoPageView = async (row: VideoPageViewRow) => {
	await db()
		.insert(videoPageViews)
		.values({
			videoId: row.videoId,
			orgId: asNanoIdOrNull(row.orgId) as Organisation.OrganisationId | null,
			sessionId: row.sessionId.slice(0, 128),
			userId: asNanoIdOrNull(row.userId) as User.UserId | null,
			pathname: row.pathname?.slice(0, 255) ?? null,
			country: row.country?.slice(0, 64) || null,
			region: row.region?.slice(0, 64) || null,
			city: row.city?.slice(0, 128) || null,
			browser: row.browser?.slice(0, 64) || null,
			device: row.device?.slice(0, 64) || null,
			os: row.os?.slice(0, 64) || null,
			timestamp: row.timestamp,
		});
};

export const countVideoPageViews = async (
	videoId: Video.VideoId,
	from: Date,
): Promise<number> => {
	const [row] = await db()
		.select({
			views: sql<number>`count(distinct ${videoPageViews.sessionId})`,
		})
		.from(videoPageViews)
		.where(
			and(
				eq(videoPageViews.videoId, videoId),
				gte(videoPageViews.timestamp, from),
			),
		);

	const count = Number(row?.views ?? 0);
	return Number.isFinite(count) ? count : 0;
};
