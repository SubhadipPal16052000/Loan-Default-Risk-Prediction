import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Business Insights",
    page_icon="📊",
    layout="wide"
)

st.title("📊 SQL Business Insights")

# =========================
# DATABASE CONNECTION
# =========================

DATABASE_URL = st.secrets["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

# =========================
# AVAILABLE VIEWS
# =========================

views = {

    "1. Executive Summary" : "SELECT * FROM executive_summary",
    "2. Purpose Default Analysis" : "SELECT * FROM purpose_default_analysis",
    "3. Risk Segmentation" : "SELECT * FROM risk_segmentation",
    "4. Financial Stress Analysis" : "SELECT * FROM financial_stress_analysis",
    "5. FICO Distribution" : "SELECT * FROM fico_distribution",
    "6. Risky Purposes" : "SELECT * FROM risky_purposes",
    "7. Inquiry Analysis" : "SELECT * FROM inquiry_analysis",
    "8. Revolving Utilization" : "SELECT * FROM revol_util_analysis",
    "9. Debt-to-Income Risk Analysis" : "SELECT * FROM dti_risk_analysis",
    "10. Delinquency Analysis" : "SELECT * FROM delinquency_analysis",
    "11. Public Record Analysis" : "SELECT * FROM public_record_analysis",
    "12. Installment Analysis" : "SELECT * FROM installment_analysis",
    "13. Loan Approval Recommendation" : "SELECT * FROM approval_recommendation",
    "14. High Risk Borrowers" : "SELECT * FROM high_risk_borrowers",
    "15. Safe Borrower Analysis" : "SELECT * FROM safe_borrowers",
    "16. Credit Policy Analysis" : "SELECT * FROM credit_policy_analysis",
    "17. Overall Default Rate" : "SELECT * FROM overall_default_rate",
    "18. Average FICO Score Analysis" : "SELECT * FROM fico_analysis"
}

selected_view = st.selectbox(
    "Select Business Insight",
    list(views.keys())
)

query = views[selected_view]

df = pd.read_sql(query, engine)

# =========================
# DISPLAY DATA
# =========================

st.subheader(f"📄 {selected_view}")

st.dataframe(df, use_container_width=True)

# =========================
# CHARTS
# =========================

if len(df.columns) >= 2:

    x_col = df.columns[0]
    y_col = df.columns[-1]

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        text=y_col,
        title=selected_view
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# DOWNLOAD CSV
# =========================

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name=f"{selected_view}.csv",
    mime="text/csv"
)