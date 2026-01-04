# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final Image
FROM python:3.11-slim
WORKDIR /app
RUN adduser --disabled-password --gecos '' appuser
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy Service Code
COPY services/compliance_auditor/app ./app
# Copy .env if needed, though safer to pass via docker-compose
# COPY services/compliance_auditor/.env .env

RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
