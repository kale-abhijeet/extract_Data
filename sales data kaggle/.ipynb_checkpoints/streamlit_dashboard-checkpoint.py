import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import datetime as dt

# Set page config
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv', encoding='ISO-8859-1')
    df.dropna(subset=['CustomerID'], inplace=True)
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M').dt.to_timestamp()
    return df

# Load the data
df = load_data()

st.title("📊 E-commerce Sales Dashboard")

# Tabs
overview, sales_tab, products_tab, rfm_tab, country_tab = st.tabs(["Overview", "Monthly Sales", "Top Products", "RFM Segmentation", "Country-wise Sales"])

# --- Monthly Sales ---
with sales_tab:
    st.header("📈 Monthly Sales Trend")
    monthly_sales = df.groupby('InvoiceMonth')['TotalPrice'].sum().reset_index()
    fig = px.line(monthly_sales, x='InvoiceMonth', y='TotalPrice', title='Total Sales Over Time')
    st.plotly_chart(fig, use_container_width=True)

# --- Top Products ---
with products_tab:
    st.header("🏆 Top 10 Products by Revenue")
    top_products = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_products, x='TotalPrice', y='Description', orientation='h', title='Top Products', color='TotalPrice')
    st.plotly_chart(fig, use_container_width=True)

# --- RFM Segmentation ---
with rfm_tab:
    st.header("🔍 RFM Segmentation")
    snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    }).reset_index()
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    
    fig1 = px.histogram(rfm, x='Recency', nbins=20, title='Recency Distribution')
    fig2 = px.histogram(rfm, x='Frequency', nbins=20, title='Frequency Distribution')
    fig3 = px.histogram(rfm, x='Monetary', nbins=20, title='Monetary Distribution')

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

# --- Country-wise Sales ---
with country_tab:
    st.header("🌍 Country-wise Sales")
    country_sales = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(country_sales, x='TotalPrice', y='Country', orientation='h', title='Top Countries by Sales', color='TotalPrice')
    st.plotly_chart(fig, use_container_width=True)

# --- Overview tab (optional) ---
with overview:
    st.header("🧾 Data Overview")
    st.write(df.head())
    st.metric("Total Revenue", f"£{df['TotalPrice'].sum():,.2f}")
    st.metric("Unique Customers", df['CustomerID'].nunique())
    st.metric("Total Invoices", df['InvoiceNo'].nunique())
