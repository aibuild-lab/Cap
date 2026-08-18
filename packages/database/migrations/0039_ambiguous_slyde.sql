CREATE TABLE `video_page_views` (
	`id` bigint AUTO_INCREMENT NOT NULL,
	`videoId` varchar(15) NOT NULL,
	`orgId` varchar(15),
	`sessionId` varchar(128) NOT NULL,
	`userId` varchar(15),
	`pathname` varchar(255),
	`country` varchar(64),
	`region` varchar(64),
	`city` varchar(128),
	`browser` varchar(64),
	`device` varchar(64),
	`os` varchar(64),
	`timestamp` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `video_page_views_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE INDEX `video_page_views_video_timestamp_idx` ON `video_page_views` (`videoId`,`timestamp`);--> statement-breakpoint
CREATE INDEX `video_page_views_video_session_idx` ON `video_page_views` (`videoId`,`sessionId`);