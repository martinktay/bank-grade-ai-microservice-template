# Multi-Service AI Banking Suite

A bank-grade monorepo containing AI microservices for loan inference and compliance auditing.

## Architecture

The project is structured as a monorepo with multiple microservices:

1.  **Loan Inference Service** (`services/loan_inference`):
    -   Predicts loan approval probabilities.
    -   Features: AI Explainability, Correlation IDs, Structured Logging, **SQLite Persistence**.
    -   Port: `8000`
    -   History: [http://127.0.0.1:8000/api/v1/history](http://127.0.0.1:8000/api/v1/history)

2.  **Compliance Auditor Service** (`services/compliance_auditor`):
    -   Audits loan decisions for regulatory compliance.
    -   Port: `8001`

## Setup

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Services

You can run each service in a separate terminal.

### Service 1: Loan Inference
```bash
uvicorn services.loan_inference.app.main:app --port 8000 --reload
```
Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Service 2: Compliance Auditor
```bash
uvicorn services.compliance_auditor.app.main:app --port 8001 --reload
```
Docs: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

## Testing

Run tests from the root directory:
```bash
pytest services/loan_inference/tests/
```

## 🚀 Live Showcase: The "Bait" Request

We tested the system with a subtle scenario to prove the **Gemini Agent's** reasoning capabilities.

**Scenario**: High Income (£85,000), Excellent Credit (740), but Employment is **"freelance"**.

**Agent's Audit Response:**
> *"The applicant exhibits a very strong financial profile... The 'freelance' status acts as a variable income indicator, but the high credit score suggests reliable debt management. The decision to approve is logically sound and consistent with risk appetite."*

### 📊 Dashboard
The full banking portal is available to visualize these decisions.
```bash
streamlit run services/dashboard/app.py
```
Access: [http://localhost:8501](http://localhost:8501)
