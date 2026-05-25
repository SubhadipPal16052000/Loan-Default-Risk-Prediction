import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from st_aggrid import AgGrid

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Executive Dashboard")

# =========================
# DATABASE CONNECTION
# =========================

DATABASE_URL = st.secrets["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

# =========================
# LOAD DATA
# =========================

df = pd.read_sql(
    "SELECT * FROM loan_data",
    engine
)

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("Filters")

purpose_filter = st.sidebar.multiselect(
    "Loan Purpose",
    options=df["purpose"].unique(),
    default=df["purpose"].unique()
)

filtered_df = df[
    df["purpose"].isin(purpose_filter)
]

# =========================
# KPI SECTION
# =========================

total_loans = len(filtered_df)

default_rate = round(
    filtered_df["not_fully_paid"].mean() * 100,
    2
)

avg_fico = round(
    filtered_df["fico"].mean(),
    2
)

avg_interest = round(
    filtered_df["int_rate"].mean(),
    4
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Loans", total_loans)

col2.metric("Default Rate", f"{default_rate}%")

col3.metric("Average FICO", avg_fico)

col4.metric("Average Interest Rate", avg_interest)

st.divider()

# =========================
# EXCEL-LIKE TABLE
# =========================

st.subheader("📄 Loan Dataset")

AgGrid(
    filtered_df,
    height=400,
    fit_columns_on_grid_load=True
)

# =========================
# CHART 1
# =========================

col1, col2 = st.columns(2)

with col1:

    purpose_summary = filtered_df.groupby(
        "purpose"
    )["not_fully_paid"].mean().reset_index()

    fig1 = px.bar(
        purpose_summary,
        x="purpose",
        y="not_fully_paid",
        title="Default Rate by Purpose"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    fig2 = px.histogram(
        filtered_df,
        x="fico",
        nbins=30,
        title="FICO Score Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =========================
# CHART 2
# =========================

col3, col4 = st.columns(2)

with col3:

    fig3 = px.scatter(
        filtered_df,
        x="fico",
        y="int_rate",
        color="not_fully_paid",
        title="FICO vs Interest Rate"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col4:

    fig4 = px.box(
        filtered_df,
        x="not_fully_paid",
        y="dti",
        title="DTI by Loan Status"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =========================
# RISK SEGMENTATION
# =========================

st.subheader("📌 Risk Segmentation")

filtered_df["risk_category"] = filtered_df["fico"].apply(

    lambda x:
    "Low Risk" if x >= 750
    else "Medium Risk" if x >= 650
    else "High Risk"
)

risk_df = filtered_df.groupby(
    "risk_category"
).size().reset_index(name="count")

fig5 = px.pie(
    risk_df,
    names="risk_category",
    values="count",
    title="Borrower Risk Segmentation"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)