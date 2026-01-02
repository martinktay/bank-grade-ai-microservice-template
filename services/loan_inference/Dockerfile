# Multi-stage build for security and size optimization

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final Image
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Ensure local bin is in PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code
COPY ./app ./app

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
