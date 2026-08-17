# AI Build Lab self-host profile

This fork remains an AGPL-licensed Cap distribution. Its public source is
available at <https://github.com/aibuild-lab/Cap>.

The AI Build Lab profile is enabled at image build time with
`NEXT_PUBLIC_SELF_HOST_BRAND=ai-build-lab`. Runtime deployments must also set
`SELF_HOST_BRAND_NAME` and `SELF_HOST_SOURCE_URL`; no organization-specific
credentials are built into the image.

The AIBL web and media release workflows build only `linux/amd64` images,
publish immutable GHCR digests, generate SPDX SBOMs, and attach GitHub build
provenance and SBOM attestations. A digest is not deployable until the AIBL
distribution gate verifies both attestations against this repository and the
exact source revision.

`apps/web/public/aibl-brand.svg` comes from the authoritative public AI Build
Lab Studio repository at revision
`f2ef81497d933cc41bdcb2e6a1e25177c4a2fbf8`, path `assets/logo.svg`. It was
whitespace-normalized without changing the mark, colors, or geometry.
