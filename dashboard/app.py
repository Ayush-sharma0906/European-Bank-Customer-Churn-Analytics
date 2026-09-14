import streamlit as st
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="European Bank Churn Analytics",
    page_icon="🏦",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🏦 European Bank")
st.sidebar.markdown("### Customer Churn Analytics")

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    **Dashboard Sections**

    📊 Executive Overview  
    🌍 Geographic Analysis  
    👥 Age Analysis  
    🔥 Engagement Analysis  
    💰 High-Value Customers  
    ⚠️ Risk Explorer  
    🎯 Strategic Insights
    """
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Customer Segmentation & Churn Pattern Analytics"
)

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "European_Bank_Processed.csv"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


df = load_data()

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_customers = len(df)

total_churners = df["Exited"].sum()

overall_churn_rate = (
    total_churners / total_customers
) * 100

germany_churn_rate = (
    df.loc[df["Geography"] == "Germany", "Exited"].mean()
) * 100

high_value_customers = (
    df["BalanceSegment"] == "High-balance"
).sum()

high_value_churners = (
    (df["BalanceSegment"] == "High-balance") &
    (df["Exited"] == 1)
).sum()

high_value_churn_rate = (
    high_value_churners / high_value_customers
) * 100

high_value_exposure = df.loc[
    (df["BalanceSegment"] == "High-balance") &
    (df["Exited"] == 1),
    "Balance"
].sum()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏦 European Bank")
st.subheader("Customer Churn & Segmentation Analytics")

st.markdown(
    """
    This dashboard provides an interactive analysis of customer churn,
    customer segmentation, engagement patterns, and high-value customer risk.
    """
)

st.divider()


# --------------------------------------------------
# EXECUTIVE KPIs
# --------------------------------------------------

st.header("📊 Executive Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Overall Churn Rate",
        f"{overall_churn_rate:.2f}%"
    )

with col3:
    st.metric(
        "Total Churners",
        f"{total_churners:,}"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Germany Churn Rate",
        f"{germany_churn_rate:.2f}%"
    )

with col5:
    st.metric(
        "High-Value Churn Rate",
        f"{high_value_churn_rate:.2f}%"
    )

with col6:
    st.metric(
        "High-Value Financial Exposure",
        f"€{high_value_exposure / 1_000_000:.2f}M"
    )


# --------------------------------------------------
# GEOGRAPHIC CHURN ANALYSIS
# --------------------------------------------------

st.header("🌍 Geographic Churn Analysis")

geo_summary = (
    df.groupby("Geography")["Exited"]
    .agg(
        Customers="count",
        Churners="sum",
        ChurnRate="mean"
    )
    .reset_index()
)

geo_summary["ChurnRate"] = geo_summary["ChurnRate"] * 100

geo_summary

st.subheader("Churn Rate by Country")

st.bar_chart(
    geo_summary.set_index("Geography")["ChurnRate"]
)

st.info(
    "Germany has the highest observed churn rate at "
    f"{germany_churn_rate:.2f}%, substantially above France and Spain. "
    "This indicates that Germany should receive particular attention "
    "in customer-retention analysis."
)

# --------------------------------------------------
# AGE-BASED CHURN ANALYSIS
# --------------------------------------------------

st.header("👥 Age-Based Churn Analysis")

age_summary = (
    df.groupby("AgeGroup")["Exited"]
    .agg(
        Customers="count",
        Churners="sum",
        ChurnRate="mean"
    )
    .reset_index()
)

age_summary["ChurnRate"] = age_summary["ChurnRate"] * 100

age_order = ["<30", "30-45", "46-60", "60+"]

age_summary["AgeGroup"] = pd.Categorical(
    age_summary["AgeGroup"],
    categories=age_order,
    ordered=True
)

age_summary = age_summary.sort_values("AgeGroup")

age_summary

st.subheader("Churn Rate by Age Group")

st.bar_chart(
    age_summary.set_index("AgeGroup")["ChurnRate"]
)

st.subheader("Customer Distribution by Age Group")

st.bar_chart(
    age_summary.set_index("AgeGroup")["Customers"]
)

st.warning(
    "Customers aged 46–60 show the highest observed churn rate "
    f"at {age_summary.loc[age_summary['AgeGroup'] == '46-60', 'ChurnRate'].iloc[0]:.2f}%. "
    "This segment should receive particular attention in retention analysis. "
    "The relationship is observational and does not establish that age itself causes churn."
)

# --------------------------------------------------
# ENGAGEMENT & CHURN ANALYSIS
# --------------------------------------------------

st.header("🔥 Engagement & Churn Analysis")

engagement_summary = (
    df.groupby("EngagementStatus")["Exited"]
    .agg(
        Customers="count",
        Churners="sum",
        ChurnRate="mean"
    )
    .reset_index()
)

engagement_summary["ChurnRate"] = (
    engagement_summary["ChurnRate"] * 100
)

engagement_summary

st.subheader("Churn Rate by Engagement Status")

st.bar_chart(
    engagement_summary.set_index("EngagementStatus")["ChurnRate"]
)

engagement_summary["ChurnContribution"] = (
    engagement_summary["Churners"]
    / total_churners
) * 100

st.subheader("Contribution to Total Churn")

st.bar_chart(
    engagement_summary.set_index("EngagementStatus")[
        "ChurnContribution"
    ]
)

st.warning(
    "Inactive customers have an observed churn rate of "
    f"{engagement_summary.loc[engagement_summary['EngagementStatus'] == 'Inactive', 'ChurnRate'].iloc[0]:.2f}%, "
    "compared with 14.27% among active customers. "
    "Inactive customers account for approximately 63.92% of all churners, "
    "making customer re-engagement an important retention priority."
)


# --------------------------------------------------
# HIGH-VALUE CUSTOMER ANALYSIS
# --------------------------------------------------

st.header("💰 High-Value Customer Analysis")

high_value_df = df[
    df["BalanceSegment"] == "High-balance"
].copy()

high_value_churned = high_value_df[
    high_value_df["Exited"] == 1
].copy()

high_value_customers = len(high_value_df)
high_value_churners = len(high_value_churned)

high_value_churn_rate = (
    high_value_churners / high_value_customers
) * 100

high_value_contribution = (
    high_value_churners / total_churners
) * 100

high_value_exposure = high_value_churned["Balance"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "High-Value Customers",
        f"{high_value_customers:,}"
    )

with col2:
    st.metric(
        "High-Value Churners",
        f"{high_value_churners:,}"
    )

with col3:
    st.metric(
        "High-Value Churn Rate",
        f"{high_value_churn_rate:.2f}%"
    )

with col4:
    st.metric(
        "Financial Exposure",
        f"€{high_value_exposure / 1_000_000:.2f}M"
    )

st.subheader("High-Value Churn by Geography")

high_value_geo = (
    high_value_df.groupby("Geography")["Exited"]
    .agg(
        Customers="count",
        Churners="sum",
        ChurnRate="mean"
    )
    .reset_index()
)

high_value_geo["ChurnRate"] = (
    high_value_geo["ChurnRate"] * 100
)

high_value_geo

st.bar_chart(
    high_value_geo.set_index("Geography")["ChurnRate"]
)

high_value_exposure_geo = (
    high_value_churned.groupby("Geography")["Balance"]
    .sum()
    .reset_index()
)

high_value_exposure_geo["Exposure_Million"] = (
    high_value_exposure_geo["Balance"] / 1_000_000
)

st.subheader("Financial Exposure of Churned High-Value Customers")

st.bar_chart(
    high_value_exposure_geo.set_index("Geography")[
        "Exposure_Million"
    ]
)

st.info(
    "Germany has the highest high-value customer churn rate at "
    f"{high_value_geo.loc[high_value_geo['Geography'] == 'Germany', 'ChurnRate'].iloc[0]:.2f}%. "
    "Churned high-value customers in Germany are associated with approximately "
    f"€{high_value_exposure_geo.loc[high_value_exposure_geo['Geography'] == 'Germany', 'Exposure_Million'].iloc[0]:.2f}M "
    "in financial exposure."
)

# --------------------------------------------------
# RISK EXPLORER
# --------------------------------------------------

st.header("⚠️ Customer Risk Explorer")

st.markdown(
    "Use the filters below to investigate churn within specific "
    "customer segments."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_geo = st.multiselect(
        "🌍 Geography",
        options=sorted(df["Geography"].unique()),
        default=sorted(df["Geography"].unique())
    )

with col2:
    selected_age = st.multiselect(
        "👥 Age Group",
        options=["<30", "30-45", "46-60", "60+"],
        default=["<30", "30-45", "46-60", "60+"]
    )

with col3:
    selected_engagement = st.multiselect(
        "🔥 Engagement",
        options=sorted(df["EngagementStatus"].unique()),
        default=sorted(df["EngagementStatus"].unique())
    )

with col4:
    selected_balance = st.multiselect(
        "💰 Balance Segment",
        options=sorted(df["BalanceSegment"].unique()),
        default=sorted(df["BalanceSegment"].unique())
    )

filtered_df = df[
    df["Geography"].isin(selected_geo) &
    df["AgeGroup"].isin(selected_age) &
    df["EngagementStatus"].isin(selected_engagement) &
    df["BalanceSegment"].isin(selected_balance)
].copy()

filtered_customers = len(filtered_df)

filtered_churners = filtered_df["Exited"].sum()

if filtered_customers > 0:
    filtered_churn_rate = (
        filtered_churners / filtered_customers
    ) * 100
else:
    filtered_churn_rate = 0

filtered_exposure = filtered_df.loc[
    filtered_df["Exited"] == 1,
    "Balance"
].sum()

st.subheader("Selected Segment")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Customers",
        f"{filtered_customers:,}"
    )

with col2:
    st.metric(
        "Churners",
        f"{filtered_churners:,}"
    )

with col3:
    st.metric(
        "Churn Rate",
        f"{filtered_churn_rate:.2f}%"
    )

with col4:
    st.metric(
        "Churned Balance Exposure",
        f"€{filtered_exposure / 1_000_000:.2f}M"
    )

if filtered_churn_rate >= 50:
    st.error(
        f"⚠️ High observed churn risk: {filtered_churn_rate:.2f}%"
    )
elif filtered_churn_rate >= 30:
    st.warning(
        f"⚠️ Elevated observed churn risk: {filtered_churn_rate:.2f}%"
    )
else:
    st.success(
        f"Observed churn rate for this segment: {filtered_churn_rate:.2f}%"
    )

# --------------------------------------------------
# CUSTOMER DRILL-DOWN
# --------------------------------------------------

st.subheader("🔎 Customer Drill-Down")

if len(filtered_df) > 0:

    display_columns = [
        "Geography",
        "Gender",
        "Age",
        "AgeGroup",
        "CreditScore",
        "Balance",
        "BalanceSegment",
        "Tenure",
        "TenureGroup",
        "NumOfProducts",
        "IsActiveMember",
        "EngagementStatus",
        "EstimatedSalary",
        "Exited"
    ]

    st.dataframe(
        filtered_df[display_columns],
        width='stretch',
        hide_index=True
    )

else:

    st.info(
        "No customers match the selected filters. "
        "Try expanding the segment selection."
    )

# --------------------------------------------------
# DOWNLOAD FILTERED CUSTOMERS
# --------------------------------------------------

csv_data = filtered_df[display_columns].to_csv(index=False)

st.download_button(
    label="📥 Download Selected Customers",
    data=csv_data,
    file_name="selected_customer_segment.csv",
    mime="text/csv"
)

# --------------------------------------------------
# GEOGRAPHY × AGE ANALYSIS
# --------------------------------------------------

st.header("🌍 Geography × Age Churn Analysis")

geo_age = (
    df.groupby(["Geography", "AgeGroup"])["Exited"]
    .mean()
    .reset_index()
)

geo_age["ChurnRate"] = geo_age["Exited"] * 100

geo_age_pivot = geo_age.pivot(
    index="Geography",
    columns="AgeGroup",
    values="ChurnRate"
)

age_order = ["<30", "30-45", "46-60", "60+"]
geo_age_pivot = geo_age_pivot.reindex(columns=age_order)

st.dataframe(
    geo_age_pivot.style.format("{:.2f}%"),
    width='stretch'
)

st.subheader("Churn Rate by Geography and Age")

st.bar_chart(geo_age_pivot)

# --------------------------------------------------
# BALANCE SEGMENT ANALYSIS
# --------------------------------------------------

st.header("💰 Balance Segment Churn Analysis")

balance_summary = (
    df.groupby("BalanceSegment")["Exited"]
    .agg(
        Customers="count",
        Churners="sum",
        ChurnRate="mean"
    )
    .reset_index()
)

balance_summary["ChurnRate"] = (
    balance_summary["ChurnRate"] * 100
)

st.dataframe(
    balance_summary.style.format({
        "ChurnRate": "{:.2f}%"
    }),
    width='stretch'
)

st.subheader("Churn Rate by Balance Segment")

st.bar_chart(
    balance_summary.set_index("BalanceSegment")["ChurnRate"]
)

# --------------------------------------------------
# PRODUCT ANALYSIS
# --------------------------------------------------

st.header("📦 Products vs Churn")

product_summary = (
    df.groupby("NumOfProducts")["Exited"]
    .agg(
        Customers="count",
        Churners="sum",
        ChurnRate="mean"
    )
    .reset_index()
)

product_summary["ChurnRate"] = (
    product_summary["ChurnRate"] * 100
)

st.dataframe(
    product_summary.style.format({
        "ChurnRate": "{:.2f}%"
    }),
    width='stretch'
)

st.subheader("Churn Rate by Number of Products")

st.bar_chart(
    product_summary.set_index("NumOfProducts")["ChurnRate"]
)


# --------------------------------------------------
# STRATEGIC INSIGHTS
# --------------------------------------------------

st.header("🎯 Strategic Insights & Recommendations")

st.markdown(
    "The following insights are derived from the observed churn patterns "
    "in the customer dataset."
)

# --------------------------------------------------
# INSIGHT 1 — GERMANY
# --------------------------------------------------

st.subheader("🇩🇪 1. Germany is the highest-risk geography")

st.write(
    f"Germany has an observed churn rate of "
    f"{germany_churn_rate:.2f}%, making it the highest-risk geography "
    "among the three countries."
)

st.info(
    "Recommended action: Prioritize customer-retention analysis and "
    "targeted engagement strategies for German customers."
)

# --------------------------------------------------
# INSIGHT 2 — AGE
# --------------------------------------------------

st.subheader("👥 2. Customers aged 46–60 require attention")

age_46_60_rate = (
    df.loc[df["AgeGroup"] == "46-60", "Exited"].mean()
) * 100

st.write(
    f"The 46–60 age group has the highest observed age-segment "
    f"churn rate at {age_46_60_rate:.2f}%."
)

st.info(
    "Recommended action: Investigate service usage, product needs, "
    "and engagement patterns among customers aged 46–60."
)

# --------------------------------------------------
# INSIGHT 3 — ENGAGEMENT
# --------------------------------------------------

inactive_rate = (
    df.loc[df["EngagementStatus"] == "Inactive", "Exited"].mean()
) * 100

st.subheader("🔥 3. Customer engagement is a major churn signal")

st.write(
    f"Inactive customers have an observed churn rate of "
    f"{inactive_rate:.2f}%, compared with 14.27% among active customers."
)

st.info(
    "Recommended action: Develop re-engagement campaigns for "
    "inactive customers before they become churned customers."
)

# --------------------------------------------------
# INSIGHT 4 — HIGH-VALUE CUSTOMERS
# --------------------------------------------------

st.subheader("💰 4. High-value customers represent significant financial exposure")

st.write(
    f"High-balance customers account for "
    f"{high_value_churners:,} churners and approximately "
    f"€{high_value_exposure / 1_000_000:.2f}M in associated balance exposure."
)

st.info(
    "Recommended action: Prioritize retention efforts for high-balance "
    "customers, particularly when combined with other risk indicators."
)

# --------------------------------------------------
# INSIGHT 5 — COMBINED RISK PROFILE
# --------------------------------------------------

st.subheader("⚠️ 5. Combined risk factors reveal the highest-risk segment")

st.write(
    "The strongest observed customer profile combines Germany, "
    "age 46–60, inactive engagement status, and high balance."
)

st.warning(
    "This segment should be considered a high-priority group for "
    "retention investigation. The observed churn rate is 82.28% "
    "among the 237 customers matching this profile."
)

# --------------------------------------------------
# MANAGEMENT PRIORITIES
# --------------------------------------------------

st.subheader("📌 Management Priorities")

priorities = pd.DataFrame({
    "Priority": [
        "1",
        "2",
        "3",
        "4"
    ],
    "Focus Area": [
        "German customers",
        "Inactive customers",
        "High-balance customers",
        "Customers aged 46–60"
    ],
    "Recommended Strategy": [
        "Investigate country-specific churn drivers",
        "Launch targeted re-engagement campaigns",
        "Prioritize retention of financially exposed customers",
        "Review customer needs and service engagement"
    ]
})

st.dataframe(
    priorities,
    width='stretch',
    hide_index=True
)


print("run sucessfully")