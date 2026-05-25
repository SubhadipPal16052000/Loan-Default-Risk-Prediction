import streamlit as st

# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="Loan Default Risk Prediction",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# MAIN TITLE
# =========================

st.title("💳 Loan Default Risk Prediction System")

st.markdown("""
Welcome to the **FinTech Risk Analytics Platform**.

This application helps financial institutions:
- Predict borrower default risk
- Analyze financial risk patterns
- Generate SQL-based business insights
- Support data-driven lending decisions

---

## 📌 Project Overview

Loan default prediction is a critical problem in the financial industry.  
Approving risky borrowers can lead to significant financial losses, while rejecting good borrowers may reduce business opportunities.

This platform combines:
- Machine Learning
- SQL Analytics
- Business Intelligence
- Cloud Database Integration
- Interactive Dashboards

to create an end-to-end credit risk management solution.

---

## 🚀 Available Modules
""")

# =========================
# FEATURE CARDS
# =========================

col1, col2, col3 = st.columns(3)

with col1:

    st.info("""
    ### 🔍 Loan Prediction
    
    Predict whether a borrower is likely to default based on:
    - FICO score
    - Income
    - DTI ratio
    - Credit utilization
    - Delinquencies
    - Credit inquiries
    
    Generates:
    - Default probability
    - Risk category
    - Lending recommendation
    """)

with col2:

    st.success("""
    ### 📊 Business Insights
    
    Run PostgreSQL analytics queries to:
    - Analyze default trends
    - Identify risky borrowers
    - Segment borrower profiles
    - Evaluate lending performance
    
    Includes:
    - SQL views
    - Charts
    - Risk analysis
    """)

with col3:

    st.warning("""
    ### 📈 Executive Dashboard
    
    Interactive dashboard with:
    - KPI cards
    - Excel-style analytics
    - Risk segmentation
    - Loan portfolio insights
    - Interactive filtering
    """)

st.divider()

# =========================
# SIDEBAR INFO
# =========================

st.sidebar.title("📂 Navigation")

st.sidebar.markdown("""
Use the sidebar to navigate between modules:

- 🔍 Prediction
- 📊 Insights
- 📈 Dashboard
""")

# =========================
# BUSINESS OBJECTIVE
# =========================

st.subheader("🎯 Business Objective")

st.markdown("""
The primary objective of this project is to reduce financial risk by accurately identifying high-risk borrowers before loan approval.

### Key Goals
- Minimize loan defaults
- Improve lending decisions
- Reduce financial losses
- Enhance borrower risk assessment
- Increase profitability
- Support explainable AI in finance
""")

# =========================
# MODEL INFORMATION
# =========================

st.subheader("🤖 Machine Learning Models Used")

model_col1, model_col2, model_col3 = st.columns(3)

with model_col1:

    st.markdown("""
    ### Logistic Regression
    
    Used for:
    - High interpretability
    - Explainable predictions
    - Regulatory transparency
    """)

with model_col2:

    st.markdown("""
    ### Random Forest
    
    Used for:
    - Non-linear learning
    - Feature importance
    - Better predictive power
    """)

with model_col3:

    st.markdown("""
    ### XGBoost
    
    Used for:
    - Advanced boosting
    - High recall performance
    - Improved classification accuracy
    """)

st.divider()

# =========================
# RISK FACTORS
# =========================

st.subheader("⚠️ Important Risk Indicators")

risk_col1, risk_col2 = st.columns(2)

with risk_col1:

    st.markdown("""
    ### Financial Indicators
    - Debt-to-Income Ratio (DTI)
    - Interest Rate
    - Revolving Credit Utilization
    - Annual Income
    
    These features reflect:
    - repayment capacity
    - financial stability
    - debt burden
    """)

with risk_col2:

    st.markdown("""
    ### Credit Behavior Indicators
    - FICO Score
    - Credit Inquiries
    - Delinquencies
    - Public Records
    
    These features indicate:
    - borrower reliability
    - repayment history
    - financial discipline
    """)

st.divider()

# =========================
# PROJECT WORKFLOW
# =========================

st.subheader("🔄 Project Workflow")

st.markdown("""
### 1️⃣ Data Collection
Loan borrower information was collected and stored in a PostgreSQL cloud database.

### 2️⃣ Data Cleaning & Preprocessing
- Missing value handling
- Feature engineering
- One-hot encoding
- Scaling & transformation

### 3️⃣ Exploratory Data Analysis
Business insights were extracted using:
- default rate analysis,
- correlation analysis,
- borrower segmentation,
- financial risk analysis.

### 4️⃣ Predictive Modeling
Multiple machine learning models were trained and evaluated using:
- Recall
- Precision
- ROC-AUC
- F1-score

### 5️⃣ Business Intelligence Dashboard
Interactive dashboards and SQL analytics were developed for stakeholders and decision-makers.
""")

st.divider()

# =========================
# TECHNOLOGY STACK
# =========================

st.subheader("🛠 Technology Stack")

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:
    st.code("Python")

with tech2:
    st.code("Streamlit")

with tech3:
    st.code("PostgreSQL")

with tech4:
    st.code("Scikit-learn")

# =========================
# FOOTER
# =========================

st.divider()

st.markdown("""
<center>

### 💡 FinTech Loan Risk Intelligence Platform

Built using:
- Machine Learning
- SQL Analytics
- Cloud Database
- Interactive Dashboards

</center>
""", unsafe_allow_html=True)