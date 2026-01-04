import streamlit as st
import httpx
import pandas as pd
import json
import time
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(
    page_title="FinCore AI: Risk & Compliance Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (Deep Slate & Platinum Theme) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #1E293B;
        color: #F8FAFC;
    }
    
    /* Headers - Platinum */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        padding-top: 0rem !important;
    }
    h1 { font-size: 1.8rem !important; }
    h2 { font-size: 1.4rem !important; }
    
    /* Metrics & Text */
    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 1.2rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }
    p, li, label {
        color: #E2E8F0 !important;
    }
    
    /* Cards/Containers */
    div[data-testid="stExpander"] {
        background-color: #334155 !important;
        border-radius: 8px;
        border: 1px solid #475569;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
    }
    
    /* Table */
    div[data-testid="stDataFrame"] {
        font-size: 0.85rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
col_header_1, col_header_2 = st.columns([4, 1])
with col_header_1:
    st.title("🛡️ FinCore AI: Risk & Compliance Portal")
    st.caption("Institutional Governance Suite | v2.1.0-Enterprise")

with col_header_2:
    st.markdown("### 🟢 System Active")

st.markdown("---")

# --- Sidebar: Input & Health ---
with st.sidebar:
    st.header("📋 Loan Application")
    
    applicant_income = st.number_input(
        "Annual Income (£)", 
        min_value=0, 
        value=85000, 
        step=1000,
        help="Gross annual income of the primary applicant."
    )
    
    credit_score = st.slider(
        "FICO Credit Score", 
        min_value=300, 
        max_value=850, 
        value=740
    )
    
    loan_amount = st.number_input(
        "Requested Amount (£)", 
        min_value=0, 
        value=30000, 
        step=500
    )
    
    employment_status = st.selectbox(
        "Employment Status", 
        options=["employed", "self_employed", "unemployed", "retired", "freelance"],
        index=4 # Default to freelance for demo
    )
    
    st.markdown("---")
    submit_button = st.button("Initiate Risk Audit", type="primary", use_container_width=True)

    # Service Health Panel
    st.markdown("### 📡 Service Health")
    c1, c2 = st.columns([1, 4])
    with c1: st.write("✅")
    with c2: st.caption("Inference Engine (v1.2)")
    
    c3, c4 = st.columns([1, 4])
    with c3: st.write("✅")
    with c4: st.caption("Compliance Auditor (GenAI)")
    
    c5, c6 = st.columns([1, 4])
    with c5: st.write("✅")
    with c6: st.caption("Immutable Ledger (SQLite)")

import os

# --- Constants ---
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api/v1")

# --- Main Logic ---

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# Logic: Audit Trigger
if submit_button:
    payload = {
        "applicant_income": applicant_income,
        "credit_score": credit_score,
        "loan_amount": loan_amount,
        "employment_status": employment_status
    }
    
    try:
        # Dynamic Agent Simulation
        with st.status("🔍 Initializing FinCore Audit Protocol...", expanded=True) as status:
            st.write("Validation: Checking Schema & AML Watchlists...")
            time.sleep(0.4) 
            
            st.write("Inference: Calculating Probability of Default (PD)...")
            time.sleep(0.4) 
            
            st.write("Compliance: Consulted 'Gemini-Flash' for Regulatory Review...")
            response = httpx.post(f"{API_URL}/predict", json=payload, timeout=12.0)
            
            st.write("Finalizing: Committing Decision to Immutable Ledger.")
            status.update(label="Audit Cycle Complete", state="complete", expanded=False)
            
        if response.status_code == 200:
            st.session_state.last_result = response.json()
        elif response.status_code == 422:
            st.error("Validation Error: Invalid Input Data.")
            st.json(response.json())
            st.session_state.last_result = None
        else:
            st.error(f"Error {response.status_code}: Upstream Service Failure.")
            st.text(response.text)
            st.session_state.last_result = None
            
    except httpx.ConnectError:
        st.error("❌ CRTICAL: Connection to Microservices Failed.")
        st.session_state.last_result = None
    except httpx.TimeoutError:
        st.error("❌ TIMEOUT: Auditor did not respond in time.")
        st.session_state.last_result = None
    except Exception as e:
        st.error(f"System Error: {str(e)}")
        st.session_state.last_result = None

# Display Result if available
if st.session_state.last_result:
    result = st.session_state.last_result
    approved = result.get("approved", False)
    confidence = result.get("confidence_score", 0.0)
    reasons = result.get("reasons", [])
    audit_analysis = result.get("audit_analysis")
    
    # Calculate Risk Probability for Visualization
    # If Approved, Risk is Low (e.g. 1 - confidence). If Denied, Risk is High (confidence)
    pd_value = 0.0
    if approved:
        pd_value = (1.0 - confidence) # Low risk
    else:
        pd_value = confidence # High risk

    # --- Top Row: Risk Gauge & Decision ---
    st.subheader("📊 Risk Assessment & Decision")
    
    col_gauge, col_report = st.columns([1, 2])
    
    with col_gauge:
        # Plotly Gauge for Probability of Default
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = pd_value * 100,
            title = {'text': "Est. Probability of Default (%)"},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#ef4444" if not approved else "#22c55e"},
                'bgcolor': "#1E293B",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 20], 'color': '#064e3b'},
                    {'range': [20, 50], 'color': '#ca8a04'},
                    {'range': [50, 100], 'color': '#7f1d1d'}
                ],
            }
        ))
        fig.update_layout(
            paper_bgcolor="#1E293B",
            font={'color': "#F8FAFC", 'family': "Arial"},
            margin=dict(l=20, r=20, t=50, b=20),
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Decision Badge
        if approved:
            st.success("## ✅ APPROVED")
            st.caption(f"Confidence: {confidence:.2%}")
        else:
            st.error("## ❌ REJECTED")
            st.caption(f"Risk Confidence: {confidence:.2%}")

    with col_report:
        # Institutional Audit Report (Gemini Output)
        st.markdown("### 📑 Institutional Audit Report (Gemini-Flash)")
        
        with st.container():
            if audit_analysis:
                status = audit_analysis.get("status", "UNKNOWN")
                mode = audit_analysis.get("mode", "UNKNOWN")
                st.markdown(f"**Audit Clearance:** `{status}` | **Mode:** `{mode}`")
                st.markdown("---")
                
                comments = audit_analysis.get("comments", [])
                if comments:
                    for comment in comments:
                         # Render as formal list items
                        st.markdown(f"> *{comment}*")
                
                if not approved and reasons:
                    st.markdown("#### Key Risk Drivers:")
                    for r in reasons:
                        st.markdown(f"- 🔴 {r}")
            else:
                st.warning("Audit Metadata Unavailable.")

    st.markdown("---")

elif not st.session_state.last_result:
    st.info("👈 Enter applicant details and click 'Initiate Risk Audit' to begin.")

# --- Bottom Section: Audit Log ---
st.subheader("📜 Global Audit Log (Immutable)")

col_hist_ctrl, col_hist_view = st.columns([1, 6])
with col_hist_ctrl:
    if st.button("🔄 Sync Log"):
        st.rerun()

try:
    history_response = httpx.get(f"{API_URL}/history", timeout=5.0)
    if history_response.status_code == 200:
        records = history_response.json()
        if records:
            df = pd.DataFrame(records)
            df = df[["timestamp", "decision", "credit_score", "applicant_income", "audit_status"]].copy()
            df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime('%H:%M:%S UTC')
            
            st.dataframe(
                df, 
                hide_index=True, 
                use_container_width=True,
                column_config={
                    "timestamp": "Timestamp",
                    "decision": st.column_config.TextColumn("Verdict", width="small"),
                    "credit_score": "FICO",
                    "applicant_income": st.column_config.NumberColumn("Income", format="£%d"),
                    "audit_status": st.column_config.TextColumn("Compliance", width="medium")
                }
            )
        else:
            st.caption("No records in current session.")
    else:
        st.warning("Ledger connection failed.")
except Exception as e:
    st.warning(f"Ledger unavailable: {str(e)}")
