from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, conint, confloat

class EmploymentStatus(str, Enum):
    employed = "employed"
    self_employed = "self_employed"
    unemployed = "unemployed"
    retired = "retired"
    freelance = "freelance"

class LoanApplication(BaseModel):
    applicant_income: confloat(gt=0) = Field(..., description="Annual income of the applicant in GBP")
    credit_score: conint(ge=300, le=850) = Field(..., description="Credit score of the applicant")
    loan_amount: confloat(gt=0) = Field(..., description="Requested loan amount in GBP")
    employment_status: EmploymentStatus = Field(..., description="Employment status of the applicant")

class PredictionResponse(BaseModel):
    approved: bool = Field(..., description="Whether the loan is approved")
    confidence_score: float = Field(..., description="Confidence score of the model (0-1)")
    reasons: List[str] = Field(default=[], description="List of reasons for the decision, especially if rejected")
    audit_analysis: Optional[Dict[str, Any]] = Field(default=None, description="Audit results from the Compliance Auditor Agent")
