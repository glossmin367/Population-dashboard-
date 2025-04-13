import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("population data.csv")

# App title
st.title("Interactive Population Dashboard")

df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Population'] = pd.to_numeric(df['Population'], errors='coerce')

# Sidebar filters
st.sidebar.header("Filter the data")

countries = st.sidebar.multiselect("Select Country", df['Country'].unique(), default=df['Country'].unique())
years = st.sidebar.multiselect("Select Year", df['Year'].unique(), default=df['Year'].unique())

# Filtered data
filtered_df = df[(df['Country'].isin(countries)) & (df['Year'].isin(years))]

# Display data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Line chart
st.subheader("Population Trend")
fig = px.line(
    filtered_df,
    x='Year',
    y='Population',
    color='Country',
    markers=True,
    title='Population over Time'
)
st.plotly_chart(fig)

# Bar chart

st.subheader("Population by Country")
bar_fig = px.bar(
    filtered_df,
    x='Country',
    y='Population',
    color='Country',
    barmode='group',
    title='Population Comparison'
)
st.plotly_chart(bar_fig)

# Footer
st.markdown("Data Source: World Bank")
