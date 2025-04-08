{}
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Load data
data = pd.read_csv("sales data.csv")

# Sidebar
st.sidebar.title("Filters")
year = st.sidebar.slider("Select Year", int(data["Year"].min()), int(data["Year"].max()), int(data["Year"].min()))
country = st.sidebar.selectbox("Select Country", sorted(data["Country"].unique()))

# Main content
st.title("Population Dashboard")
st.write("Select a year and country to view population data by category.")

# Filtered data
filtered_data = data[(data["Year"] == year) & (data["Country"] == country)]

if filtered_data.empty:
    st.warning("No data available for this selection.")
else:
    st.subheader(f"Population in {country} - {year}")

    # Plot bar chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(filtered_data["Category"], filtered_data["Value"], color='steelblue')
    ax.set_xlabel("Category")
    ax.set_ylabel("Value (mn)")
    ax.set_title(f"{country} - {year}")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)