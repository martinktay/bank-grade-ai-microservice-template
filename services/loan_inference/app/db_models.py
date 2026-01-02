from sqlalchemy import Column, Integer, Float, String, DateTime
from .database import Base
import uuid
from datetime import datetime

class LoanRecord(Base):
    __tablename__ = "loan_records"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    applicant_income = Column(Float)
    credit_score = Column(Integer)
    decision = Column(String)  # Approved / Denied
    audit_status = Column(String)  # CLEARED / FLAGGED / OFFLINE
    audit_comments = Column(String, nullable=True)
