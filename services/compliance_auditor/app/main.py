from fastapi import FastAPI, Request
import uuid
import logging
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Setup Environment
# Load .env from services/compliance_auditor/.env (parent of app/)
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(basedir, ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(title="Compliance Auditor Agent", version="1.1.0")
logger = logging.getLogger("compliance_auditor")

SYSTEM_PROMPT = """You are a professional Banking Compliance Auditor at FinCore AI. Your task is to review loan decisions for potential bias, discrimination, or logical errors. 
Analyze the decision reason against the applicant data. 
Look for violations of Fair Lending practices. 

CRITICAL RULE: Evaluate this loan decision strictly. If the decision is "Approved" but the metrics (Income, Credit Score) are borderline or conflicting (e.g. Low Score + High Income), you MUST flag it for review. Do NOT just agree with the inference engine. 
Return your response in JSON format with fields: "status" (CLEARED/FLAGGED), "compliance_score" (0.0 to 1.0), and "detailed_analysis" (a brief paragraph explaining your thought process)."""

def get_rule_based_decision(decision_reason: str, applicant_data: dict) -> dict:
    """Fallback logic if AI is offline."""
    flagged = False
    audit_comments = []
    
    if not decision_reason:
        flagged = True
        audit_comments.append("REDACTED: Decision lacks transparent reasoning.")
        
    if "employed" in decision_reason.lower() and applicant_data.get("credit_score", 0) > 700:
        audit_comments.append("ADVISORY: Potential bias detected. High credit score rejected due to employment status.")
        flagged = True

    return {
        "status": "FLAGGED" if flagged else "CLEARED",
        "compliance_score": 0.4 if flagged else 1.0,
        "detailed_analysis": "; ".join(audit_comments) if audit_comments else "Automated Check Cleared."
    }

async def get_ai_audit_decision(decision_reason: str, applicant_data: dict) -> dict:
    """Invokes Gemini 1.5 Flash for agentic reasoning."""
    if not GEMINI_API_KEY:
        raise ValueError("No API Key configured")

    model = genai.GenerativeModel('gemini-flash-latest')
    prompt = f"""
    Decision Reason: {decision_reason}
    Applicant Data: {json.dumps(applicant_data)}
    """
    
    # Instruct model to return JSON
    response = await model.generate_content_async(
        f"{SYSTEM_PROMPT}\n{prompt}",
        generation_config={"response_mime_type": "application/json"}
    )
    
    return json.loads(response.text)

@app.post("/audit")
async def perform_audit(audit_request: dict):
    decision_reason = audit_request.get("decision_reason", "")
    applicant_data = audit_request.get("applicant_data", {})
    
    result = None
    used_agent = False
    
    # Try AI Agent
    try:
        result = await get_ai_audit_decision(decision_reason, applicant_data)
        used_agent = True
    except Exception as e:
        logger.warning(f"AI Agent failed, falling back to rules. Error: {e}")
        result = get_rule_based_decision(decision_reason, applicant_data)
        
    # Map result to API response (preserving compatibility with Project 1)
    status = result.get("status", "UNKNOWN")
    score = result.get("compliance_score", 0.0)
    analysis = result.get("detailed_analysis", "")
    
    # Ensure comments list exists for Project 1 persistence
    comments = [analysis] if analysis else []
    
    return {
        "audit_id": str(uuid.uuid4()),
        "status": status,
        "compliance_score": score,
        "comments": comments,
        "mode": "GEN_AI" if used_agent else "RULE_BASED"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}
