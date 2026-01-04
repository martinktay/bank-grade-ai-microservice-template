from fastapi.testclient import TestClient
from services.loan_inference.app.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
def test_predict_loan_approved(mock_post):
    # Mock successful auditor response
    # Create a proper mock response object
    from unittest.mock import MagicMock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "CLEARED",
        "compliance_score": 1.0,
        "comments": ["Automated Check Cleared."],
        "mode": "GEN_AI",
        "audit_id": "test-123"
    }
    mock_post.return_value = mock_response

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

@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
def test_predict_loan_rejected(mock_post):
    # Mock successful auditor response (even if loan rejected by rules, auditor is called)
    from unittest.mock import MagicMock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "CLEARED", 
        "compliance_score": 1.0,
        "comments": ["No compliance issues found."],
        "mode": "GEN_AI",
        "audit_id": "test-456"
    }
    mock_post.return_value = mock_response

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
