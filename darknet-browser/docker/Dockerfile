FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json ./
COPY svelte.config.js ./
COPY vite.config.js ./

# Copy environment variables if they exist
COPY .env* ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy source code
COPY src ./src

# Build the application
RUN npm run build

FROM node:18-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000
ENV PUBLIC_SUPABASE_URL=https://owddlfgtopfeqbkmwsox.supabase.co
ENV PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im93ZGRsZmd0b3BmZXFia213c294Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ2ODg1MTAsImV4cCI6MjA4MDI2NDUxMH0.mMKdgjR0bItJ3Kxrcn6FDWWnlSPAOq1IxodwFb2C0Ak

# Copy package.json
COPY package.json ./

# Install only production dependencies
RUN npm install --only=production --legacy-peer-deps

# Copy built application from builder stage
COPY --from=builder /app/build ./build

EXPOSE 3000

CMD ["node", "build"]