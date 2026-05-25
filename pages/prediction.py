import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Loan Prediction",
    page_icon="💳",
    layout="wide"
)

# =========================
# PAGE TITLE
# =========================

st.title("💳 Loan Default Prediction System")

st.markdown("""
Predict whether a borrower is likely to default on a loan using machine learning.

The prediction is based on:
- Credit score
- Debt-to-Income Ratio
- Credit utilization
- Delinquencies
- Financial behavior
""")

# =========================
# MODEL FILE PATHS
# =========================

MODEL_PATH = "models/loan_default_logistic_model.pkl"

SCALER_PATH = "models/loan_scaler.pkl"

THRESHOLD_PATH = "models/loan_threshold.pkl"

TRAINING_COLUMNS_PATH = "models/training_columns.pkl"

# =========================
# CHECK FILE EXISTENCE
# =========================

required_files = [
    MODEL_PATH,
    SCALER_PATH,
    THRESHOLD_PATH,
    TRAINING_COLUMNS_PATH
]

for file in required_files:

    if not os.path.exists(file):

        st.error(f"❌ File not found: {file}")

        st.stop()

# =========================
# LOAD MODEL FILES
# =========================

model = joblib.load(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)

threshold = joblib.load(THRESHOLD_PATH)

training_columns = joblib.load(TRAINING_COLUMNS_PATH)

# =========================
# PAGE SECTION
# =========================

st.subheader("📋 Borrower Information")

# =========================
# SAMPLE PROFILES
# =========================

profile = st.selectbox(
    "Choose Sample Borrower Profile",
    [
        "Custom",
        "Low Risk Borrower",
        "Medium Risk Borrower",
        "High Risk Borrower"
    ]
)

# =========================
# DEFAULT VALUES
# =========================

if profile == "Low Risk Borrower":

    default_values = {
        "credit_policy": 1,
        "purpose": "credit_card",
        "int_rate": 0.08,
        "installment": 200.0,
        "log_annual_inc": 11.5,
        "dti": 10.0,
        "fico": 780,
        "days_with_cr_line": 5000.0,
        "revol_bal": 5000.0,
        "revol_util": 20.0,
        "inq_last_6mths": 1,
        "delinq_2yrs": 0,
        "pub_rec": 0
    }

elif profile == "Medium Risk Borrower":

    default_values = {
        "credit_policy": 1,
        "purpose": "debt_consolidation",
        "int_rate": 0.14,
        "installment": 350.0,
        "log_annual_inc": 10.7,
        "dti": 18.0,
        "fico": 670,
        "days_with_cr_line": 4000.0,
        "revol_bal": 12000.0,
        "revol_util": 55.0,
        "inq_last_6mths": 3,
        "delinq_2yrs": 1,
        "pub_rec": 0
    }

elif profile == "High Risk Borrower":

    default_values = {
        "credit_policy": 0,
        "purpose": "small_business",
        "int_rate": 0.20,
        "installment": 500.0,
        "log_annual_inc": 10.2,
        "dti": 28.0,
        "fico": 580,
        "days_with_cr_line": 3000.0,
        "revol_bal": 20000.0,
        "revol_util": 85.0,
        "inq_last_6mths": 6,
        "delinq_2yrs": 3,
        "pub_rec": 1
    }

else:

    default_values = {
        "credit_policy": 1,
        "purpose": "debt_consolidation",
        "int_rate": 0.12,
        "installment": 300.0,
        "log_annual_inc": 10.5,
        "dti": 15.0,
        "fico": 700,
        "days_with_cr_line": 4000.0,
        "revol_bal": 10000.0,
        "revol_util": 50.0,
        "inq_last_6mths": 1,
        "delinq_2yrs": 0,
        "pub_rec": 0
    }

# =========================
# INPUT FORM
# =========================

col1, col2 = st.columns(2)

with col1:

    credit_policy = st.selectbox(
        "Credit Policy",
        [0, 1],
        index=[0, 1].index(default_values["credit_policy"]),
        help="1 = Meets credit policy"
    )

    purpose = st.selectbox(
        "Loan Purpose",
        [
            "debt_consolidation",
            "credit_card",
            "all_other",
            "home_improvement",
            "small_business",
            "major_purchase",
            "educational"
        ],
        index=[
            "debt_consolidation",
            "credit_card",
            "all_other",
            "home_improvement",
            "small_business",
            "major_purchase",
            "educational"
        ].index(default_values["purpose"])
    )

    int_rate = st.slider(
        "Interest Rate",
        0.0,
        0.30,
        float(default_values["int_rate"]),
        0.01
    )

    installment = st.number_input(
        "Installment Amount",
        value=float(default_values["installment"])
    )

    log_annual_inc = st.number_input(
        "Log Annual Income",
        value=float(default_values["log_annual_inc"])
    )

    dti = st.slider(
        "Debt-to-Income Ratio",
        0.0,
        40.0,
        float(default_values["dti"]),
        help="""
        Healthy: Below 15
        Moderate: 15-20
        High Risk: Above 20
        """
    )

with col2:

    fico = st.slider(
        "FICO Score",
        300,
        850,
        int(default_values["fico"]),
        help="""
        Excellent: 750+
        Good: 700-749
        Fair: 650-699
        Risky: Below 650
        """
    )

    days_with_cr_line = st.number_input(
        "Days with Credit Line",
        value=float(default_values["days_with_cr_line"])
    )

    revol_bal = st.number_input(
        "Revolving Balance",
        value=float(default_values["revol_bal"])
    )

    revol_util = st.slider(
        "Revolving Utilization (%)",
        0.0,
        150.0,
        float(default_values["revol_util"]),
        help="""
        Low Risk: Below 30%
        Medium Risk: 30-70%
        High Risk: Above 70%
        """
    )

    inq_last_6mths = st.slider(
        "Inquiries Last 6 Months",
        0,
        10,
        int(default_values["inq_last_6mths"])
    )

    delinq_2yrs = st.slider(
        "Delinquencies in 2 Years",
        0,
        10,
        int(default_values["delinq_2yrs"])
    )

    pub_rec = st.slider(
        "Public Records",
        0,
        10,
        int(default_values["pub_rec"])
    )

# =========================
# PREDICTION BUTTON
# =========================

if st.button("🔍 Predict Default Risk"):

    # =========================
    # CREATE INPUT DATAFRAME
    # =========================

    input_df = pd.DataFrame({

        "credit_policy": [credit_policy],
        "purpose": [purpose],
        "int_rate": [int_rate],
        "installment": [installment],
        "log_annual_inc": [log_annual_inc],
        "dti": [dti],
        "fico": [fico],
        "days_with_cr_line": [days_with_cr_line],
        "revol_bal": [revol_bal],
        "revol_util": [revol_util],
        "inq_last_6mths": [inq_last_6mths],
        "delinq_2yrs": [delinq_2yrs],
        "pub_rec": [pub_rec]

    })

    # =========================
    # ONE-HOT ENCODING
    # =========================

    input_df = pd.get_dummies(input_df)

    # =========================
    # MATCH TRAINING FEATURES
    # =========================

    for col in training_columns:

        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[training_columns]

    # =========================
    # SCALE INPUT
    # =========================

    scaled_input = scaler.transform(input_df)

    # =========================
    # MODEL PREDICTION
    # =========================

    probability = model.predict_proba(
        scaled_input
    )[0][1]

    prediction = 1 if probability >= threshold else 0

    # =========================
    # BUSINESS RULE OVERRIDE
    # =========================

    high_risk_flags = 0

    if fico < 650:
        high_risk_flags += 1

    if dti > 20:
        high_risk_flags += 1

    if revol_util > 70:
        high_risk_flags += 1

    if delinq_2yrs >= 2:
        high_risk_flags += 1

    # =========================
    # FINAL RISK CATEGORY
    # =========================

    if probability >= 0.75 or high_risk_flags >= 3:

        risk_level = "HIGH"

    elif probability >= 0.40 or high_risk_flags >= 2:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    # =========================
    # OUTPUT SECTION
    # =========================

    st.divider()

    st.subheader("📊 Prediction Result")

    st.metric(
        "Default Probability",
        f"{probability * 100:.2f}%"
    )

    st.info(
        f"Model Decision Threshold: {threshold:.2f}"
    )

    # =========================
    # RISK DISPLAY
    # =========================

    if risk_level == "HIGH":

        st.error("🔴 HIGH RISK BORROWER")

    elif risk_level == "MEDIUM":

        st.warning("🟠 MEDIUM RISK BORROWER")

    else:

        st.success("🟢 LOW RISK BORROWER")

    # =========================
    # BUSINESS RECOMMENDATION
    # =========================

    if risk_level == "HIGH":

        st.error("⚠️ Loan Default Highly Likely")

        st.markdown("""
        ### Business Recommendation
        
        - Reject loan application
        - Require collateral
        - Manual underwriting review required
        - Additional financial verification recommended
        """)

    elif risk_level == "MEDIUM":

        st.warning("⚠️ Moderate Risk Borrower")

        st.markdown("""
        ### Business Recommendation
        
        - Additional income verification recommended
        - Consider reducing loan amount
        - Moderate approval risk
        """)

    else:

        st.success("✅ Borrower Appears Financially Stable")

        st.markdown("""
        ### Business Recommendation
        
        - Eligible for approval
        - Low probability of default
        - Standard lending process recommended
        """)

    # =========================
    # RISK SCORE
    # =========================

    st.subheader("📈 Risk Score")

    st.progress(float(probability))

    # =========================
    # BUSINESS INTERPRETATION
    # =========================

    st.subheader("💡 Risk Interpretation")

    if fico < 650:
        st.warning(
            "Low FICO score indicates elevated credit risk."
        )

    if dti > 20:
        st.warning(
            "High Debt-to-Income ratio suggests financial stress."
        )

    if revol_util > 70:
        st.warning(
            "High revolving utilization indicates excessive credit usage."
        )

    if inq_last_6mths > 5:
        st.warning(
            "Multiple recent credit inquiries may indicate financial instability."
        )

    if delinq_2yrs > 1:
        st.warning(
            "Previous delinquencies increase default probability."
        )