import streamlit as st
import pandas as pd

st.set_page_config(page_title="SAR Monitoring Dashboard", layout="wide")

# -------------------------------
# Custom Styling
# -------------------------------
st.markdown("""
    <style>
    .kpi-card {
        padding:20px;
        border-radius:12px;
        color:white;
        text-align:center;
        font-size:20px;
        font-weight:bold;
    }
    .red {background-color:#e74c3c;}
    .green {background-color:#2ecc71;}
    .blue {background-color:#3498db;}
    .orange {background-color:#e67e22;}
    </style>
""", unsafe_allow_html=True)

st.title("🔎 Suspicious Activity Report (SAR) Monitoring Dashboard")

mode = st.sidebar.radio("Select Mode", ["System View", "Admin View"])

# -------------------------------
# Sample Data (Session State)
# -------------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Account ID": ["A101","A202","A303","A404"],
        "Amount": [200000,150000,300000,120000],
        "Risk": ["High","Medium","High","Low"],
        "Reason": ["Structuring","Rapid Transfers","Large Deposit","Unusual Location"],
        "Status": ["Pending","Pending","Pending","Monitoring"]
    })

data = st.session_state.data

# KPI Calculations
total_transactions = 1000
suspicious = len(data[data["Risk"] == "High"])
sar_generated = len(data[data["Status"] == "Approved"])
risk_score = 78

# ==================================================
# SYSTEM VIEW
# ==================================================
if mode == "System View":

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f'<div class="kpi-card blue">Total Transactions<br>{total_transactions}</div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="kpi-card red">High Risk<br>{suspicious}</div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="kpi-card orange">SAR Approved<br>{sar_generated}</div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="kpi-card green">Risk Score<br>{risk_score}%</div>', unsafe_allow_html=True)

    st.subheader("📋 Suspicious Accounts Overview")
    st.dataframe(data, use_container_width=True)

# ==================================================
# ADMIN VIEW
# ==================================================
elif mode == "Admin View":

    st.subheader("🛡 Admin Review Panel")

    for index, row in data.iterrows():
        with st.expander(f"Account {row['Account ID']} - {row['Risk']} Risk"):

            st.write(f"💰 Amount: ₹{row['Amount']}")
            st.write(f"⚠ Reason: {row['Reason']}")
            st.write(f"📌 Current Status: {row['Status']}")

            col1, col2 = st.columns(2)

            if col1.button(f"Approve {row['Account ID']}", key=f"approve_{index}"):
                st.session_state.data.at[index, "Status"] = "Approved"
                st.success("SAR Approved Successfully ✅")

            if col2.button(f"Reject {row['Account ID']}", key=f"reject_{index}"):
                st.session_state.data.at[index, "Status"] = "Rejected"
                st.error("Transaction Rejected ❌")
