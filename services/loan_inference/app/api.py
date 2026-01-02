from fastapi import APIRouter, HTTPException, Request
from .models import LoanApplication, PredictionResponse
import random
import logging
import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import get_db
from .db_models import LoanRecord
import json

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, summary="Predict Loan Approval")
async def predict_loan(application: LoanApplication, db: AsyncSession = Depends(get_db)):
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

    # --- golden Link: Call Compliance Auditor ---
    audit_data = None
    try:
        decision_reason = reasons[0] if reasons else "Met all criteria"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://127.0.0.1:8001/audit",
                json={
                    "decision_reason": decision_reason,
                    "applicant_data": application.model_dump()
                },
                timeout=10.0
            )
            if response.status_code == 200:
                audit_data = response.json()
            else:
                logger.error(f"Auditor returned {response.status_code}", extra={"body": response.text})
    except httpx.TimeoutException as e:
        logger.warning(f"Auditor timed out (GenAI Latency), proceeding with internal check only. Error: {str(e)}")
        audit_data = None
    except Exception as e:
        logger.warning(f"Auditor unavailable, proceeding with internal check only. Error: {str(e)}")
        audit_data = None

    # --- Persistence: Save to Database ---
    try:
        audit_status = "OFFLINE"
        audit_comments_str = ""
        
        if audit_data:
            audit_status = audit_data.get("status", "UNKNOWN")
            comments = audit_data.get("comments", [])
            audit_comments_str = json.dumps(comments) if comments else ""
        
        db_record = LoanRecord(
            applicant_income=application.applicant_income,
            credit_score=application.credit_score,
            decision="Approved" if approved else "Denied",
            audit_status=audit_status,
            audit_comments=audit_comments_str
        )
        db.add(db_record)
        await db.commit()
    except Exception as e:
        logger.error(f"Failed to save loan record: {str(e)}")

    return PredictionResponse(
        approved=approved,
        confidence_score=round(confidence, 2),
        reasons=reasons,
        audit_analysis=audit_data
    )

@router.get("/history", summary="Get recent loan history")
async def get_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LoanRecord).order_by(LoanRecord.timestamp.desc()).limit(10))
    records = result.scalars().all()
    return records
