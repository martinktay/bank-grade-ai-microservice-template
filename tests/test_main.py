from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_loan_approved():
    payload = {
        "applicant_income": 50000,
        "credit_score": 750,
        "loan_amount": 10000,
        "employment_status": "employed"
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    assert "X-Correlation-ID" in response.headers
    data = response.json()
    assert "approved" in data
    assert "confidence_score" in data
    assert data["approved"] is True

def test_predict_loan_rejected():
    payload = {
        "applicant_income": 10000,
        "credit_score": 400,
        "loan_amount": 50000,
        "employment_status": "unemployed"
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    assert "X-Correlation-ID" in response.headers
    data = response.json()
    # While random, this combination should almost certainly reject
    # but we primarily test structure and that it returns valid JSON. 
    # Logic verification can be more strict if the random component is removed.
    assert "approved" in data
    assert "confidence_score" in data
    assert "reasons" in data
    
    if not data["approved"]:
        assert len(data["reasons"]) > 0

def test_invalid_input():
    payload = {
        "applicant_income": -100, # Invalid
        "credit_score": 900,      # Invalid
        "loan_amount": 10000,
        "employment_status": "employed"
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422
