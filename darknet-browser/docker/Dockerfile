FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json ./
COPY svelte.config.js ./
COPY vite.config.js ./

# Install ALL dependencies (including dev dependencies for build)
# Using npm install instead of npm ci to avoid package-lock.json requirement
RUN npm install --legacy-peer-deps

# Copy source code
COPY src ./src

# Build the application
RUN npm run build

FROM node:18-alpine

WORKDIR /app

# Environment variables (will be set at runtime via docker-compose)
ENV NODE_ENV=production
ENV PORT=3000

# Copy package.json
COPY package.json ./

# Install production dependencies only
RUN npm install --only=production --legacy-peer-deps

# Copy built application from builder
COPY --from=builder /app/build ./build

EXPOSE 3000

CMD ["node", "build"]