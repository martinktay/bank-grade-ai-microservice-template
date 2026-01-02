from fastapi import APIRouter, HTTPException
from app.models import LoanApplication, PredictionResponse
import random

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, summary="Predict Loan Approval")
async def predict_loan(application: LoanApplication):
    """
    Simulate a loan approval prediction model.
    """
    # Dummy logic simulation
    # In a real scenario, this would load a model and run inference
    
    score = 0
    if application.credit_score > 700:
        score += 0.5
    if application.applicant_income > 30000:
        score += 0.3
    if application.employment_status == "employed":
        score += 0.2
        
    # Add some randomness for simulation
    confidence = min(score + random.uniform(-0.1, 0.1), 1.0) # nosec
    approved = confidence > 0.6
    
    reasons = []
    if not approved:
        if application.credit_score <= 600:
            reasons.append("Credit score below 600")
        if application.applicant_income < 30000:
            reasons.append("Income too low for loan amount")
        if application.employment_status not in ["employed", "self_employed"]:
            reasons.append("Employment status required")
            
    # Struct log info
    import logging
    logger = logging.getLogger()
    logger.info("Prediction made", extra={
        "approved": approved,
        "confidence": confidence,
        "loan_amount": application.loan_amount
    })

    return PredictionResponse(
        approved=approved,
        confidence_score=round(confidence, 2),
        reasons=reasons
    )
