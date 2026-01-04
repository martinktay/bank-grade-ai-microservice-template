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

# Copy Dashboard Code
COPY services/dashboard/app.py ./app.py

RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
