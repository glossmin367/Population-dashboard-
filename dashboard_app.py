
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    data = pd.read_csv("sales_data.csv")
    data['Year'] = pd.to_datetime(data['Year'])
    return data

df = load_data()

st.sidebar.header("Filter Options")
countries = st.sidebar.multiselect("Select Country", options=df['Country'].unique(), default=df['Country'].unique())
year_range = st.sidebar.date_input("Select Year Range", [df['Year'].min(), df['Year'].max()])

filtered_df = df[
    (df['Country'].isin(countries)) &
    (df['Year'] >= pd.to_datetime(year_range[0])) &
    (df['Year'] <= pd.to_datetime(year_range[1]))
]

total_value = filtered_df['Value'].sum()
total_customers = filtered_df.shape[0]
avg_value = filtered_df['Total'].mean()

st.markdown("""
    <div style="background-color:#1f77b4;padding:20px;border-radius:10px">
    <h2 style="color:white;text-align:center;">Interactive Sales Dashboard</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Overview")
st.write(f"{len(filtered_df)} records match your filters")

col1, col2, col3 = st.columns(3)
col1.metric("Total Value", f"${total_value:,.2f}")
col2.metric("Transactions", f"{total_customers:,}")
col3.metric("Avg Value", f"${avg_value:,.2f}")

tabs = st.tabs(["Sales Trend", "Best Sellers", "Data Table"])

with tabs[0]:
    st.subheader("Sales Over Time")
    sales_over_time = filtered_df.groupby(['Date'])['Total'].sum().reset_index()
    fig = px.line(sales_over_time, x='Date', y='Total', title="Daily Sales Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("Top 5 Best-Selling Products")
    top_products = filtered_df.groupby('Product')['Total'].sum().sort_values(ascending=False).reset_index()
    fig_product = px.bar(top_products.head(5), x='Product', y='Total', color='Total',
                         color_continuous_scale='Blues', title="Top 5 Products by Sales")
    st.plotly_chart(fig_product, use_container_width=True)

with tabs[2]:
    st.subheader("Raw Sales Data")
    st.dataframe(filtered_df)
    st.download_button("Download CSV", filtered_df.to_csv(index=False), file_name="filtered_sales.csv")
