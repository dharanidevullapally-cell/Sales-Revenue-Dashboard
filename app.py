import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Sales & Revenue Analysis Dashboard")

# Load Data
df = pd.read_csv("sales_data.csv")

# Create Revenue Column
df["Revenue"] = df["Quantity"] * df["Price"]

# Sidebar Filters
st.sidebar.header("Filters")

selected_products = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Filter Data
filtered_df = df[
    (df["Product"].isin(selected_products)) &
    (df["Category"].isin(selected_categories))
]

# KPIs
total_revenue = filtered_df["Revenue"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_orders = len(filtered_df)
total_products = filtered_df["Product"].nunique()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("📦 Total Quantity", total_quantity)
col3.metric("🛒 Total Orders", total_orders)
col4.metric("🏷️ Products", total_products)

st.markdown("---")

# Charts Row
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue Trend")

    trend = (
        filtered_df.groupby("Date")["Revenue"]
        .sum()
        .reset_index()
    )

    fig_line = px.line(
        trend,
        x="Date",
        y="Revenue",
        markers=True
    )

    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Revenue by Product")

    product_revenue = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .reset_index()
    )

    fig_bar = px.bar(
        product_revenue,
        x="Product",
        y="Revenue"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# Second Row
col3, col4 = st.columns(2)

with col3:
    st.subheader("Revenue by Category")

    category_revenue = (
        filtered_df.groupby("Category")["Revenue"]
        .sum()
        .reset_index()
    )

    fig_pie = px.pie(
        category_revenue,
        names="Category",
        values="Revenue"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.subheader("Top Products")

    top_products = (
        product_revenue.sort_values(
            by="Revenue",
            ascending=False
        )
    )

    st.dataframe(
        top_products,
        use_container_width=True
    )

st.markdown("---")

st.subheader("Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)