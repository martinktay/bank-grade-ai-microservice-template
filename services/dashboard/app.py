import streamlit as st
import httpx
import pandas as pd
import json
import time

# --- Page Config ---
st.set_page_config(
    page_title="Automated AI Loan Governance Suite",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Compact Headers */
    h1 { font-size: 1.5rem !important; padding-top: 1rem !important; }
    h2 { font-size: 1.3rem !important; padding-top: 0rem !important; }
    h3 { font-size: 1.1rem !important; padding-top: 0rem !important; }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.0rem !important;
    }
    
    /* Block Spacing */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Table Font */
    div[data-testid="stDataFrame"] {
        font-size: 0.8rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
col_header_1, col_header_2 = st.columns([3, 1])
with col_header_1:
    st.title("🏦 Automated AI Loan Governance Suite")
with col_header_2:
    st.caption("v1.0.0 | System Status: 🟢 Online")

st.markdown("---")

# --- Sidebar: Input Form ---
with st.sidebar:
    st.header("📋 New Application")
    
    applicant_income = st.number_input(
        "Applicant Income (£)", 
        min_value=0, 
        value=50000, 
        step=1000
    )
    
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        credit_score = st.number_input(
            "Credit Score", 
            min_value=300, 
            max_value=850, 
            value=720
        )
    with col_sb2:
        loan_amount = st.number_input(
            "Amount (£)", 
            min_value=0, 
            value=15000, 
            step=500
        )
    
    employment_status = st.selectbox(
        "Employment Status", 
        options=["employed", "self_employed", "unemployed", "retired", "freelance"]
    )
    
    st.markdown("---")
    submit_button = st.button("Submit for Audit", type="primary", use_container_width=True)

# --- Constants ---
API_URL = "http://127.0.0.1:8000/api/v1"

# --- Main Logic ---

# Initialize session state 
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# Logic: Only run when button is clicked
if submit_button:
    payload = {
        "applicant_income": applicant_income,
        "credit_score": credit_score,
        "loan_amount": loan_amount,
        "employment_status": employment_status
    }
    
    try:
        # Dynamic Agent Simulation
        with st.status("🔍 Initializing Bank-Grade Audit...", expanded=True) as status:
            st.write("Checking Applicant Data Schema...")
            time.sleep(0.5) 
            
            st.write("📡 Creating Secure Tunnel to Auditor Microservice...")
            time.sleep(0.5) 
            
            st.write("🤖 AI Agent Analysis in Progress (Consulting Knowledge Base)...")
            response = httpx.post(f"{API_URL}/predict", json=payload, timeout=12.0)
            
            st.write("✅ Decision Finalized.")
            status.update(label="Audit Complete", state="complete", expanded=False)
            
        if response.status_code == 200:
            st.session_state.last_result = response.json()
        elif response.status_code == 422:
            st.error("Validation Error: Please check input values.")
            st.json(response.json())
            st.session_state.last_result = None
        else:
            st.error(f"Error: {response.status_code}")
            st.text(response.text)
            st.session_state.last_result = None
            
    except httpx.ConnectError:
        st.error("❌ Connection Failed. Is the Loan Service (Port 8000) running?")
        st.session_state.last_result = None
    except httpx.TimeoutError:
        st.error("❌ Timeout. AI Agent took too long.")
        st.session_state.last_result = None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.last_result = None

# Display Result if available
if st.session_state.last_result:
    st.subheader("📊 audit_metrics") # Used variable name style for unique header if needed, or just plain text
    
    result = st.session_state.last_result
    approved = result.get("approved", False)
    confidence = result.get("confidence_score", 0.0)
    reasons = result.get("reasons", [])
    audit_analysis = result.get("audit_analysis")

    # Layout: 3 Columns
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if approved:
            st.metric("Decision", "APPROVED", delta="PASS", delta_color="normal")
        else:
            st.metric("Decision", "DENIED", delta="RISK", delta_color="inverse")
            
    with c2:
        st.metric("Model Confidence", f"{confidence:.1%}")
        
    with c3:
        if audit_analysis:
            status = audit_analysis.get("status", "UNKNOWN")
            st.metric("Audit Status", status, delta="AI Active" if status in ["CLEARED", "FLAGGED"] else "Offline", delta_color="off")

    st.markdown("---")
    
    # Analysis Panel
    with st.container():
        col_analysis_1, col_analysis_2 = st.columns([1, 1])
        
        with col_analysis_1:
            st.markdown("### 📝 Auditor Insights")
            if audit_analysis:
                comments = audit_analysis.get("comments", [])
                mode = audit_analysis.get("mode", "UNKNOWN")
                
                if mode == "GEN_AI":
                    st.success(f"**AI Reasoning ({mode})**")
                    for comment in comments:
                        st.info(f"{comment}")
                else:
                    st.warning(f"**Fallback Logic ({mode})**")
                    for comment in comments:
                        st.write(f"• {comment}")
            else:
                st.warning("No audit analysis returned.")

        with col_analysis_2:
             st.markdown("### ⚖️ Risk Factors")
             if reasons:
                 st.error("The following negative factors were identified:")
                 for reason in reasons:
                     st.write(f"❌ {reason}")
             else:
                 st.success("No critical risk factors identified.")

    st.markdown("---")

elif not st.session_state.last_result:
    st.info("Enter details in the sidebar and click Submit to start the audit process.")

# 2. Bottom Section: History
st.subheader("📜 Recent Activity Log")

col_hist_ctrl, col_hist_view = st.columns([1, 5])
with col_hist_ctrl:
    if st.button("🔄 Refresh Data"):
        st.rerun()

try:
    history_response = httpx.get(f"{API_URL}/history", timeout=5.0)
    if history_response.status_code == 200:
        records = history_response.json()
        if records:
            df = pd.DataFrame(records)
            # Reorder and rename for "Nice" display
            display_df = df[[
                "timestamp", "decision", "credit_score", "applicant_income", "audit_status"
            ]].copy()
            
            # Format timestamp nicely
            display_df["timestamp"] = pd.to_datetime(display_df["timestamp"]).dt.strftime('%H:%M:%S')
            
            st.dataframe(
                display_df, 
                hide_index=True, 
                use_container_width=True,
                column_config={
                    "timestamp": "Time",
                    "decision": st.column_config.TextColumn("Decision", width="small"),
                    "credit_score": "Score",
                    "applicant_income": st.column_config.NumberColumn("Income", format="£%d"),
                    "audit_status": st.column_config.TextColumn("Audit", width="medium")
                }
            )
        else:
            st.info("No records found in database.")
    else:
        st.warning(f"Could not fetch history (Status: {history_response.status_code})")
except Exception as e:
    st.warning(f"History unavailable: {str(e)}")
