import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("./data/GlobalWeatherRepository.csv")
df['last_updated'] = pd.to_datetime(df['last_updated'])
df_us = df[df['country'].isin(['United States of America', 'USA United States of America'])]

# Streamlit UI
st.title("US Air Quality & Weather Dashboard")

# City selection dropdown
selected_city = st.selectbox("Select a City:", df_us['location_name'].unique())

# Date range selector
start_date, end_date = st.date_input(
    "Select Date Range:",
    [df_us['last_updated'].min().date(), df_us['last_updated'].max().date()],
    min_value=df_us['last_updated'].min().date(),
    max_value=df_us['last_updated'].max().date()
)

# Filter data based on user selection
filtered_df = df_us[(df_us['location_name'] == selected_city) &
                    (df_us['last_updated'].dt.date >= start_date) &
                    (df_us['last_updated'].dt.date <= end_date)]

# Temperature Trend
st.subheader(f"Temperature Trend in {selected_city}")
temp_fig = px.line(filtered_df, x='last_updated', y='temperature_celsius',
                    title=f'Temperature Trend in {selected_city}', markers=True)
st.plotly_chart(temp_fig)

# Wind Speed vs. Humidity Scatter Plot
st.subheader("Wind Speed vs. Humidity (Colored by AQI)")
scatter_fig = px.scatter(filtered_df, x='wind_kph', y='humidity',
                          color='air_quality_us-epa-index',
                          title='Wind Speed vs. Humidity (Colored by AQI)')
st.plotly_chart(scatter_fig)

# Air Quality Map
st.subheader("US Air Quality Index")
map_fig = px.scatter_geo(df_us, lat='latitude', lon='longitude',
                          color='air_quality_us-epa-index',
                          size='air_quality_PM2.5',
                          hover_name='location_name',
                          title='Air Quality Index',
                          scope='usa')
st.plotly_chart(map_fig)

st.write("Data Source: GlobalWeatherRepository.csv")
