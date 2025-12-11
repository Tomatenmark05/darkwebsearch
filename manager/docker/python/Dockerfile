# Use an official lightweight Python image
FROM python:3.11-slim

# Do not generate .pyc files and ensure output is unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy application code
COPY src/python /app

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Run as non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose default FastAPI port
EXPOSE 8000



COPY --chmod=0755 docker/python/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]