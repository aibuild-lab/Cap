import "@/app/globals.css";
import { buildEnv, getSelfHostBrandProfile } from "@cap/env";
import { OpenPanelComponent } from "@openpanel/nextjs";
import type { Metadata } from "next";
import localFont from "next/font/local";
import Script from "next/script";
import type { PropsWithChildren } from "react";

const defaultFont = localFont({
	src: [
		{
			path: "../public/fonts/NeueMontreal-Bold.woff2",
			weight: "700",
			style: "normal",
		},
		{
			path: "../public/fonts/NeueMontreal-Regular.woff2",
			weight: "400",
			style: "normal",
		},
		{
			path: "../public/fonts/NeueMontreal-Medium.woff2",
			weight: "500",
			style: "normal",
		},
		{
			path: "../public/fonts/NeueMontreal-MediumItalic.woff2",
			weight: "500",
			style: "italic",
		},
		{
			path: "../public/fonts/NeueMontreal-Italic.woff2",
			weight: "400",
			style: "italic",
		},
		{
			path: "../public/fonts/NeueMontreal-BoldItalic.woff2",
			weight: "700",
			style: "italic",
		},
	],
	preload: false,
});

const brand = getSelfHostBrandProfile();
const isAiBuildLab = brand.id === "ai-build-lab";
const title = isAiBuildLab
	? "AI Build Lab Video — Private screen recordings"
	: "Cap — Beautiful screen recordings, owned by you.";
const description = isAiBuildLab
	? "Private-by-default screen recording and sharing for the AI Build Lab team."
	: "Cap is the open source alternative to Loom. Lightweight, powerful, and cross-platform. Record and share in seconds.";

export const metadata: Metadata = {
	metadataBase: new URL(
		isAiBuildLab ? buildEnv.NEXT_PUBLIC_WEB_URL : "https://cap.so",
	),
	title,
	description,
	openGraph: {
		title,
		description,
		type: "website",
		url: isAiBuildLab ? buildEnv.NEXT_PUBLIC_WEB_URL : "https://cap.so",
		siteName: brand.name,
		images: [
			{
				url: "/api/og",
				width: 1200,
				height: 630,
				alt: title,
			},
		],
	},
	twitter: {
		card: "summary_large_image",
		title,
		description,
		images: ["/api/og"],
	},
};

export default function RootLayout({ children }: PropsWithChildren) {
	return (
		// suppressHydrationWarning: the Cap Chrome extension stamps
		// data-cap-chrome-extension-installed on <html> at document_idle,
		// which can land before hydration finishes.
		<html className={defaultFont.className} lang="en" suppressHydrationWarning>
			<head>
				<link
					rel="apple-touch-icon"
					sizes="180x180"
					href={isAiBuildLab ? brand.logoPath : "/apple-touch-icon.png"}
				/>
				<link
					rel="icon"
					type="image/png"
					sizes="32x32"
					href={isAiBuildLab ? brand.logoPath : "/favicon-32x32.png"}
				/>
				<link
					rel="icon"
					type="image/png"
					sizes="16x16"
					href={isAiBuildLab ? brand.logoPath : "/favicon-16x16.png"}
				/>
				<link rel="manifest" href={brand.manifestPath} />
				<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5" />
				<link
					rel="shortcut icon"
					href={isAiBuildLab ? brand.logoPath : "/favicon.ico"}
				/>
				<meta name="msapplication-TileColor" content="#da532c" />
				<meta name="theme-color" content={brand.themeColor} />
			</head>
			<body suppressHydrationWarning>
				<Script src="/theme-script.js" strategy="beforeInteractive" />
				{buildEnv.NEXT_PUBLIC_OPENPANEL_CLIENT_ID ? (
					<OpenPanelComponent
						apiUrl="/api/op"
						clientId={buildEnv.NEXT_PUBLIC_OPENPANEL_CLIENT_ID}
						scriptUrl="/api/op/op1.js"
						trackOutgoingLinks
						trackScreenViews
					/>
				) : null}
				<main className="w-full">{children}</main>
			</body>
		</html>
	);
}
