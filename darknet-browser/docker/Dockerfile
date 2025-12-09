FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json ./
COPY svelte.config.js ./
COPY vite.config.js ./

RUN npm install --legacy-peer-deps

COPY src ./src

RUN npm run build

FROM node:18-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

COPY package.json ./

RUN npm install --only=production --legacy-peer-deps

COPY --from=builder /app/build ./build

EXPOSE 3000

CMD ["node", "build"]