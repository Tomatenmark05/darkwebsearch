# --- Stage 1: Build Svelte frontend ---
FROM node:20-alpine AS frontend-build

WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --silent
COPY frontend/ ./
ARG VITE_API_BASE=/analyze
ENV VITE_API_BASE=$VITE_API_BASE
RUN npm run build

# --- Stage 2: Python FastAPI runtime ---
FROM python:3.11-slim AS runtime

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend (app) code
COPY app/ ./app
# Copy built frontend assets
COPY --from=frontend-build /frontend/dist ./app/static

ENV PORT=8080
ENV DOWNSTREAM_URL=""
ENV LOG_LEVEL=info

EXPOSE 8080
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"]