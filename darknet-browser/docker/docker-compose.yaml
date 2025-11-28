FROM node:20-alpine AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --silent || npm install --no-audit --no-fund --silent
COPY frontend/ ./
ARG VITE_API_BASE=/analyze
ENV VITE_API_BASE=$VITE_API_BASE
RUN npm run build

FROM python:3.11-slim AS runtime
WORKDIR /app

# Add this line so 'from routers ...' works (routers lives under /app/src)
ENV PYTHONPATH=/app/src

COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY --from=frontend-build /frontend/dist ./static

ENV PORT=8080 DOWNSTREAM_URL="" LOG_LEVEL=info
EXPOSE 8080
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]