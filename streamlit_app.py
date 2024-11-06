!pip install plotly

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Streamlit page configuration
st.set_page_config(page_title="Interactive Visualisation Dashboard", page_icon="🌍", layout="wide")
st.header("Global Metrics Analysis: Trends, Insights, and Predictions")

df = pd.read_csv('Dataset.csv') 
st.write("Data loaded successfully!")

# Filter options in the sidebar
st.sidebar.header("Filters")
    
# Country selection
countries = st.sidebar.multiselect(
    "Select Countries", 
    options=df["Country"].unique(),
    default=df["Country"].unique()[:5] 
)

# Year selection 
year_range = st.sidebar.slider(
    "Select Year Range", 
    min_value=int(df["Year"].min()), 
    max_value=int(df["Year"].max()), 
    value=(int(df["Year"].min()), int(df["Year"].max()))  # Default to the full range
)

# Select a feature from the columns
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
feature_to_plot = st.sidebar.selectbox(
    "Select Feature to Plot", 
    options=numeric_columns,
    index=numeric_columns.index("GDP (in Trillions USD)")  # Default to GDP if present
)

# Plot type selection
plot_type = st.sidebar.radio(
    "Select Plot Type", 
    options=["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"]
)

# Filtering the dataset based on selections
df_filtered = df[
    (df["Country"].isin(countries)) & 
    (df["Year"] >= year_range[0]) & 
    (df["Year"] <= year_range[1])
]

# Plotting based on selected plot type
if plot_type == "Bar Chart":
    fig = px.bar(
        df_filtered, 
        x="Country", 
        y=feature_to_plot, 
        title=f"{feature_to_plot} by Country", 
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Line Chart":
    fig = px.line(
        df_filtered, 
        x="Year", 
        y=feature_to_plot, 
        color="Country", 
        title=f"{feature_to_plot} Over Time by Country", 
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Scatter Plot":
    other_feature = st.sidebar.selectbox(
        "Select another feature for Scatter Plot",
        options=[col for col in numeric_columns if col != feature_to_plot]
    )
    fig = px.scatter(
        df_filtered, 
        x=feature_to_plot, 
        y=other_feature, 
        color="Country", 
        size="Population (in Millions)", 
        title=f"{feature_to_plot} vs {other_feature} by Country", 
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Pie Chart":
    fig = px.pie(
        df_filtered, 
        names="Country", 
        values=feature_to_plot, 
        title=f"{feature_to_plot} Distribution by Country", 
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.subheader("Advanced Customization Options")
if st.sidebar.checkbox("Show Raw Data"):
    # Show only the selected columns (Country, Year, and the selected feature)
    raw_data = df_filtered[["Country", "Year", feature_to_plot]]
    st.write(raw_data)

csv = df_filtered.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)
