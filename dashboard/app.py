"""
Armani Middle East Trading
Executive KPI Dashboard — Professional Light Edition
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sqlalchemy import create_engine
from pathlib import Path

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Armani Trading | Executive Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Custom CSS — Light Professional Theme
# -------------------------------------------------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    div[data-testid="metric-container"] label {
        color: #64748b !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 8px;
        color: #64748b;
        padding: 8px 18px;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }

    /* Divider */
    hr {
        border-color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Data Loading
# -------------------------------------------------
DB_URL = "postgresql+psycopg2://armani:armani123@localhost:5432/armani_trading"

@st.cache_data(ttl=300)
def load_data():
    try:
        engine = create_engine(DB_URL)
        df = pd.read_sql("SELECT * FROM vw_sales_enriched ORDER BY week_key", engine)
        return df
    except Exception:
        path = Path("data/processed/cleaned_sales.parquet")
        if path.exists():
            return pd.read_parquet(path)
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_forecast():
    path = Path("data/processed/demand_forecast_26w.csv")
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

df = load_data()
forecast_df = load_forecast()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("""
<div style="display:flex; align-items:center; gap:14px; margin-bottom:6px;">
    <div style="font-size:2rem;">📈</div>
    <div>
        <h1 style="margin:0; padding:0; font-size:1.8rem; color:#1e293b;">Armani Middle East Trading</h1>
        <p style="margin:0; color:#64748b; font-size:0.95rem;">Executive Performance Dashboard • Demand • Inventory • Profitability • Risk</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

if df.empty:
    st.error("No data available. Please run the ETL pipeline first.")
    st.stop()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Filters")
    st.markdown("")

    product_col = "product_name" if "product_name" in df.columns else "Product"
    week_col = "week_key" if "week_key" in df.columns else "Week"

    products = sorted(df[product_col].unique())
    selected_products = st.multiselect(
        "Products",
        products,
        default=products[:6] if len(products) > 6 else products
    )

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This dashboard provides visibility into:
    - Financial performance
    - Inventory efficiency
    - Demand forecasts
    - Operational risk alerts
    """)

filtered = df[df[product_col].isin(selected_products)].copy() if selected_products else df.copy()

# Derived KPI
if "inventory_turnover_ratio" in filtered.columns:
    filtered["dsi"] = np.where(
        filtered["inventory_turnover_ratio"] > 0,
        7 / filtered["inventory_turnover_ratio"],
        np.nan
    )

# -------------------------------------------------
# KPI Row
# -------------------------------------------------
st.markdown("### Key Performance Indicators")

total_revenue = filtered["revenue"].sum()
avg_margin = filtered["gross_profit_margin"].mean() * 100
total_op_profit = filtered["operating_profit"].sum()
avg_turnover = filtered["inventory_turnover_ratio"].mean()
avg_dsi = filtered["dsi"].mean() if "dsi" in filtered.columns else 0
total_units = filtered["sales_units"].sum()

k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Total Revenue", f"${total_revenue/1e6:.2f}M")
k2.metric("Gross Margin", f"{avg_margin:.1f}%")
k3.metric("Operating Profit", f"${total_op_profit/1e6:.2f}M")
k4.metric("Inventory Turnover", f"{avg_turnover:.2f}x")
k5.metric("Days Sales Inventory", f"{avg_dsi:.1f}d")
k6.metric("Units Sold", f"{total_units/1e3:.1f}K")

st.markdown("")

# -------------------------------------------------
# Tabs
# -------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Financial Performance",
    "📦 Inventory Intelligence",
    "🔮 Demand Forecast",
    "⚠️ Risk Alerts"
])

COLOR_SEQ = px.colors.qualitative.Set2

def style_chart(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=20, l=10, r=10),
        legend_title_text="",
        font=dict(color="#334155")
    )
    return fig

# ===================== FINANCIAL =====================
with tab1:
    st.markdown("#### Revenue & Profitability Trends")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.line(
            filtered, x=week_col, y="revenue", color=product_col,
            color_discrete_sequence=COLOR_SEQ,
            title="Weekly Revenue"
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    with c2:
        fig = px.line(
            filtered, x=week_col, y="gross_profit_margin", color=product_col,
            color_discrete_sequence=COLOR_SEQ,
            title="Gross Profit Margin"
        )
        fig.update_layout(yaxis_tickformat=".0%")
        st.plotly_chart(style_chart(fig), width="stretch")

    op_summary = (
        filtered.groupby(product_col)["operating_profit"]
        .sum()
        .reset_index()
        .sort_values("operating_profit", ascending=False)
    )

    fig = px.bar(
        op_summary, x=product_col, y="operating_profit",
        color="operating_profit",
        color_continuous_scale="Blues",
        title="Total Operating Profit by Product"
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(style_chart(fig), width="stretch")

# ===================== INVENTORY =====================
with tab2:
    st.markdown("#### Inventory Health & Efficiency")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.line(
            filtered, x=week_col, y="inventory_level", color=product_col,
            color_discrete_sequence=COLOR_SEQ,
            title="Inventory Level Over Time"
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    with c2:
        fig = px.line(
            filtered, x=week_col, y="inventory_turnover_ratio", color=product_col,
            color_discrete_sequence=COLOR_SEQ,
            title="Inventory Turnover Ratio"
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    if "dsi" in filtered.columns:
        fig = px.line(
            filtered, x=week_col, y="dsi", color=product_col,
            color_discrete_sequence=COLOR_SEQ,
            title="Days Sales of Inventory (DSI)"
        )
        st.plotly_chart(style_chart(fig), width="stretch")

# ===================== FORECAST =====================
with tab3:
    st.markdown("#### 6-Month Demand Forecast (26 Weeks)")

    if forecast_df.empty:
        st.info("Forecast data not available. Please run the forecasting module first.")
    else:
        fc_products = st.multiselect(
            "Select products to display",
            sorted(forecast_df["product_name"].unique()),
            default=sorted(forecast_df["product_name"].unique())[:5],
            key="fc_products"
        )

        fc_filtered = forecast_df[forecast_df["product_name"].isin(fc_products)]

        fig = px.line(
            fc_filtered,
            x="forecast_week",
            y="predicted_demand",
            color="product_name",
            color_discrete_sequence=COLOR_SEQ,
            title="Predicted Demand — Next 26 Weeks"
        )
        st.plotly_chart(style_chart(fig), width="stretch")

        with st.expander("View Forecast Data"):
            st.dataframe(
                fc_filtered.sort_values(["product_name", "forecast_week"]),
                width="stretch",
                height=300
            )

# ===================== RISK =====================
with tab4:
    st.markdown("#### Operational Risk Alerts")

    col_left, col_right = st.columns(2)

    high_inv = filtered[
        (filtered["inventory_level"] > filtered["inventory_level"].quantile(0.85)) &
        (filtered["inventory_turnover_ratio"] < filtered["inventory_turnover_ratio"].quantile(0.30))
    ]

    with col_left:
        st.markdown("##### 🔴 High Inventory / Low Turnover")
        if high_inv.empty:
            st.success("No critical inventory risk detected.")
        else:
            st.warning(f"{len(high_inv)} risk records found")
            st.dataframe(
                high_inv[[product_col, week_col, "inventory_level", "inventory_turnover_ratio", "sales_units"]]
                .drop_duplicates()
                .head(30),
                width="stretch",
                height=280
            )

    low_margin = filtered[filtered["gross_profit_margin"] < 0.10]

    with col_right:
        st.markdown("##### 🟠 Low Gross Margin (< 10%)")
        if low_margin.empty:
            st.success("No low-margin risk detected.")
        else:
            st.warning(f"{len(low_margin)} low-margin records found")
            st.dataframe(
                low_margin[[product_col, week_col, "gross_profit_margin", "revenue", "gross_profit"]]
                .drop_duplicates()
                .head(30),
                width="stretch",
                height=280
            )

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#94a3b8; font-size:0.85rem;'>"
    "Armani Middle East Trading • Data Science Assessment • Executive Dashboard"
    "</div>",
    unsafe_allow_html=True
)