FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Build the application
RUN npm run build

FROM node:18-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Copy package.json
COPY package.json ./

# Install only production dependencies
RUN npm install --only=production --legacy-peer-deps

# Copy built application
COPY --from=builder /app/build ./build

EXPOSE 3000

CMD ["node", "build"]