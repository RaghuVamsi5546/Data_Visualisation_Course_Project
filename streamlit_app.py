import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from PIL import Image

# Streamlit page configuration
st.set_page_config(page_title="Interactive Visualisation Dashboard", page_icon="🌍", layout="wide")
st.header("Global Metrics Analysis: Trends, Insights, and Predictions")

# Load data
df = pd.read_csv('Dataset.csv')
st.write("Data loaded successfully!")

# Sidebar filters
st.sidebar.header("Filters")

# Country selection
countries = st.sidebar.multiselect("Select Countries", options=df["Country"].unique(), default=df["Country"].unique()[:5])

# Year range selection
default_year_range = (int(df["Year"].min()), int(df["Year"].max()))
year_range = st.sidebar.slider("Select Year Range", min_value=default_year_range[0], max_value=default_year_range[1], value=default_year_range)

# Feature selection
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
feature_to_plot = st.sidebar.selectbox("Select Feature to Plot", options=numeric_columns, index=numeric_columns.index("GDP (in Trillions USD)") if "GDP (in Trillions USD)" in numeric_columns else 0)

# Plot type selection
plot_type = st.sidebar.radio("Select Plot Type", options=["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"])

# Filter data based on selections
df_filtered = df[(df["Country"].isin(countries)) & (df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# Guide image
with st.sidebar.expander("Guide Image to Feature Relationships", expanded=False):
    st.write("This image explains the relationship between two key features to help you interpret the graphs more effectively.")
    guide_image = Image.open("images/phase1_output.png")  # Make sure the image is in the "images" folder or specify the correct path
    st.image(guide_image, caption="Guide to Feature Relationships", use_column_width=True)

# Check if the filtered data is empty
if df_filtered.empty:
    st.warning("No data available for the selected filters. Please adjust the filters.")
else:
    # Plotting based on selected plot type
    if plot_type == "Bar Chart":
        # Check if the year range is a single year or multiple years
        if year_range[0] == year_range[1]:  # Single year selected
            fig = px.bar(df_filtered, x="Country", y=feature_to_plot, title=f"{feature_to_plot} by Country for {year_range[0]}", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:  # Multiple years selected
            fig = go.Figure()
            for country in countries:
                country_data = df_filtered[df_filtered["Country"] == country]
                fig.add_trace(go.Bar(x=country_data["Year"], y=country_data[feature_to_plot], name=country))
            
            fig.update_layout(
                barmode="group",
                title=f"Grouped Bar Chart of {feature_to_plot} by Country Over Time",
                xaxis_title="Year",
                yaxis_title=feature_to_plot,
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Line Chart":
        fig = px.line(df_filtered, x="Year", y=feature_to_plot, color="Country", title=f"{feature_to_plot} Over Time by Country", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Scatter Plot":
        other_feature = st.sidebar.selectbox("Select another feature for Scatter Plot", options=[col for col in numeric_columns if col != feature_to_plot])
        fig = px.scatter(df_filtered, x=feature_to_plot, y=other_feature, color="Country", size="Population (in Millions)", title=f"{feature_to_plot} vs {other_feature} by Country", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Pie Chart":
        fig = px.pie(df_filtered, names="Country", values=feature_to_plot, title=f"{feature_to_plot} Distribution by Country", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

# Advanced customization options
st.sidebar.subheader("Advanced Customization Options")
if st.sidebar.checkbox("Show Raw Data"):
    st.write(df_filtered[["Country", "Year", feature_to_plot]])

# Download button for filtered data
csv = df_filtered.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(label="Download Filtered Data", data=csv, file_name="filtered_data.csv", mime="text/csv")
