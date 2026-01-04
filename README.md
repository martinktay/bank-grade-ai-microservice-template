# FinCore: Governance-First AI Credit Suite

**FinCore** is an institutional-grade AI banking suite designed for automated credit risk assessment and regulatory compliance auditing. It leverages Agentic AI (Gemini) to provide explainable, auditable loan decisions.

![FinCore Status](https://img.shields.io/badge/Status-Active-success)
![MLOps](https://img.shields.io/badge/MLOps-Docker%20%7C%20GitHub%20Actions-blue)
![Compliance](https://img.shields.io/badge/Compliance-FCA%20%7C%20Fair%20Lending-purple)

## 🏗️ Architecture & Microservices

The suite follows a **Governance-First MLOps Pattern**, orchestrated via Docker Compose:

1.  **Loan Inference Engine** (`port:8000`):
    *   **Function**: Calculates Probability of Default (PD) and rules-based eligibility.
    *   **Tech**: FastAPI, Pydantic, Structured Logging, SQLite Immutable Ledger.
2.  **Compliance Auditor Agent** (`port:8001`):
    *   **Function**: An autonomous GenAI agent (Gemini-Flash) that reviews loan decisions against "internal policy" for bias and risk.
    *   **Pattern**: *Asynchronous Audit Trigger*.
3.  **FinCore Portal** (`port:8501`):
    *   **Function**: Executive Dashboard for Loan Officers.
    *   **Tech**: Streamlit, Plotly Risk Gauges, Deep Slate UI Theme.

## 🚀 Quick Start (Docker MLOps)

The entire suite is containerized for Linux/WSL environments.

1.  **Configure Credentials**:
    Ensure your `services/compliance_auditor/.env` contains your `GEMINI_API_KEY`.

2.  **Launch Suite**:
    ```bash
    docker-compose up --build -d
    ```

3.  **Access Interfaces**:
    *   **FinCore Portal**: [http://localhost:8501](http://localhost:8501)
    *   **Inference API**: [http://localhost:8000/docs](http://localhost:8000/docs)
    *   **Auditor API**: [http://localhost:8001/docs](http://localhost:8001/docs)

## 🧠 Technical Patterns

### 1. LLM-Based Risk Reasoning
Unlike "Black Box" AI, FinCore uses a dedicated **Auditor Agent** that generates human-readable "Institutional Reports". It evaluates complex factors (e.g., "Freelance" status vs High Income) via semantic reasoning, not just numerical thresholds.

### 2. Asynchronous Audit Triggers
The Inference Engine makes a preliminary decision and *immediately* dispatches the context to the Auditor service. This decouples the operational latency:
*   **Fast Path**: Rules-based decision returns instantly (simulated).
*   **Audit Path**: The Agent reviews the decision and logs its findings to the shared immutable ledger.

### 3. Immutable Audit Persistence
All decisions and their corresponding AI critiques are stored in an append-only SQLite ledger, enabling full regulatory replayability.

## 🧪 CI/CD & Testing

The project uses GitHub Actions (`.github/workflows/mlops_pipeline.yml`) to enforce quality:
*   **Linting**: `flake8` ensures PEP8 compliance.
*   **Testing**: `pytest` validates inference logic and API contracts.

```bash
# Run tests locally
pytest services/loan_inference/tests/
```
