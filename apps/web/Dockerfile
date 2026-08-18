# syntax=docker.io/docker/dockerfile:1

FROM node:22-alpine@sha256:c610fcdfb1d5b4740dd70c284ed3cb16bb857e0f7166196e36a5501df7a3aa32 AS builder
WORKDIR /app
COPY . .

RUN corepack enable
RUN corepack enable pnpm
RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store pnpm i --frozen-lockfile

ARG NEXT_PUBLIC_DOCKER_BUILD=true
ARG NEXT_PUBLIC_SELF_HOST_BRAND
ARG NEXT_PUBLIC_WEB_URL=http://localhost:3000
ARG DATABASE_URL=mysql://cap:build-only@127.0.0.1:3306/cap
ARG WEB_URL=http://localhost:3000
ARG NEXTAUTH_URL=http://localhost:3000
ARG CAP_AWS_BUCKET=build-only
ARG CAP_AWS_REGION=auto
ARG SELF_HOST_BRAND_NAME=AI Build Lab
ARG SELF_HOST_SOURCE_URL=https://github.com/aibuild-lab/Cap
ARG CAP_VIDEOS_DEFAULT_PUBLIC=false
ARG CAP_ALLOWED_SIGNUP_DOMAINS=aibuildlab.com
ENV NEXT_PUBLIC_DOCKER_BUILD=$NEXT_PUBLIC_DOCKER_BUILD
ENV NEXT_PUBLIC_SELF_HOST_BRAND=$NEXT_PUBLIC_SELF_HOST_BRAND
ENV NEXT_PUBLIC_WEB_URL=$NEXT_PUBLIC_WEB_URL
ENV DATABASE_URL=$DATABASE_URL
ENV WEB_URL=$WEB_URL
ENV NEXTAUTH_URL=$NEXTAUTH_URL
ENV CAP_AWS_BUCKET=$CAP_AWS_BUCKET
ENV CAP_AWS_REGION=$CAP_AWS_REGION
ENV SELF_HOST_BRAND_NAME=$SELF_HOST_BRAND_NAME
ENV SELF_HOST_SOURCE_URL=$SELF_HOST_SOURCE_URL
ENV CAP_VIDEOS_DEFAULT_PUBLIC=$CAP_VIDEOS_DEFAULT_PUBLIC
ENV CAP_ALLOWED_SIGNUP_DOMAINS=$CAP_ALLOWED_SIGNUP_DOMAINS

RUN NEXTAUTH_SECRET=build-only-not-for-runtime pnpm run build:web


# 3. Production image, copy all the files and run next
FROM node:24-alpine@sha256:d32cdf619f63fe0471182d08996dd516c6275bb5fd31ae06e55a570bd9e1ad43 AS runner
WORKDIR /app

RUN rm -rf \
	/usr/local/lib/node_modules/corepack \
	/usr/local/lib/node_modules/npm \
	/opt/yarn-v1.22.22 \
	&& rm -f \
	/usr/local/bin/corepack \
	/usr/local/bin/npm \
	/usr/local/bin/npx \
	/usr/local/bin/pnpm \
	/usr/local/bin/pnpx \
	/usr/local/bin/yarn \
	/usr/local/bin/yarnpkg

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001


# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/static ./apps/web/.next/static
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/public ./apps/web/public
COPY --from=builder --chown=nextjs:nodejs /app/packages/database/migrations ./apps/web/migrations


USER 1001:1001

EXPOSE 3000

ENV HOSTNAME=0.0.0.0
CMD ["node", "apps/web/server.js"]
