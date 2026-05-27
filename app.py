import streamlit as st
import pandas as pd
import os
import plotly.express as px
from src.utils import generate_synthetic_transactions
from src.rules import AMLRulesEngine, large_amount, structuring, high_risk_country, rapid_movement

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Vigilia - AML Monitor",
    layout="wide",
    page_icon="🛡️"
)

st.title("🛡️ Vigilia - AML Transaction Monitoring Dashboard")
st.markdown("**Anti-Money Laundering** transaction monitoring tool")

# ====================== SIDEBAR CONTROLS ======================
st.sidebar.header("Controls")

# Button to generate new data
if st.sidebar.button("Generate New Synthetic Data"):
    with st.spinner("Generating new transactions..."):
        df = generate_synthetic_transactions(1200)
    st.sidebar.success("New data generated!")

# File uploader - allows user to upload their own CSV
uploaded_file = st.sidebar.file_uploader("Upload your own transaction CSV", type=["csv"])

# ====================== LOAD DATA ======================
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Uploaded file loaded!")
else:
    data_file = 'data/sample_transactions.csv'
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
    else:
        df = generate_synthetic_transactions(800)

# ====================== APPLY RULES ENGINE ======================
engine = AMLRulesEngine()

# Adding rules with their weights (importance)
engine.add_rule(large_amount, 40)
engine.add_rule(structuring, 35)
engine.add_rule(high_risk_country, 30)
engine.add_rule(rapid_movement, 25)

enriched_df = engine.apply_rules(df)

# ====================== FILTERS ======================
st.sidebar.header("Filters")
country_filter = st.sidebar.multiselect(
    "Filter by Country",
    options=sorted(df['country'].unique()),
    default=[]
)

risk_filter = st.sidebar.slider("Minimum Risk Score", 0, 100, 0)

# Apply filters
filtered_df = enriched_df.copy()
if country_filter:
    filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]
if risk_filter > 0:
    filtered_df = filtered_df[filtered_df['risk_score'] >= risk_filter]

# ====================== MAIN DASHBOARD ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transactions", len(df))
col2.metric("Flagged Transactions", len(enriched_df[enriched_df['flagged']]))
col3.metric("Avg Risk Score", f"{enriched_df['risk_score'].mean():.1f}")
col4.metric("Filtered Rows", len(filtered_df))

# ====================== CHARTS ======================
st.subheader("Risk Distribution")
fig = px.histogram(enriched_df, x='risk_score', nbins=20, title="Risk Score Distribution")
st.plotly_chart(fig, use_container_width=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Transactions by Country")
    country_counts = enriched_df['country'].value_counts()
    fig2 = px.pie(names=country_counts.index, values=country_counts.values)
    st.plotly_chart(fig2, use_container_width=True)

with col_chart2:
    st.subheader("Flagged vs Normal")
    fig3 = px.bar(
        x=['Normal', 'Flagged'],
        y=[len(enriched_df[~enriched_df['flagged']]), len(enriched_df[enriched_df['flagged']])],
        color=['Normal', 'Flagged']
    )
    st.plotly_chart(fig3, use_container_width=True)

# ====================== FLAGGED TRANSACTIONS TABLE ======================
st.subheader("Flagged Suspicious Transactions")
flagged = enriched_df[enriched_df['flagged']].sort_values('risk_score', ascending=False)

if not flagged.empty:
    st.dataframe(
        flagged[['transaction_id', 'amount', 'country', 'type', 'risk_score', 'reasons']],
        use_container_width=True
    )
else:
    st.info("No transactions flagged yet.")

# ====================== ALL TRANSACTIONS ======================
st.subheader("All Transactions (Filtered)")
st.dataframe(filtered_df, use_container_width=True)

# Export button
if st.button("Export Flagged Transactions to CSV"):
    flagged.to_csv('flagged_transactions.csv', index=False)
    st.success("Exported to flagged_transactions.csv")