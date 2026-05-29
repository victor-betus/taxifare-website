import streamlit as st
import requests
import pandas as pd
import datetime

'''
# TaxiFarel AI

## Enter your ride details and get your fare estimate!
'''

pickup_date = st.date_input('date and time', min_value=datetime.date(2009, 1, 1))
pickup_time = st.time_input('time')
pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)
pickup_longitude = st.number_input('pickup longitude', format="%.6f")
pickup_latitude = st.number_input('pickup latitude', format="%.6f")
dropoff_longitude = st.number_input('dropoff longitude', format="%.6f")
dropoff_latitude = st.number_input('dropoff latitude', format="%.6f")
passenger_count = st.number_input('passenger count')


params = {
    'pickup_datetime': pd.Timestamp(pickup_datetime),
    'pickup_longitude': float(pickup_longitude),
    'pickup_latitude': float(pickup_latitude),
    'dropoff_longitude': float(dropoff_longitude),
    'dropoff_latitude': float(dropoff_latitude),
    'passenger_count': int(passenger_count)
    }


url = 'https://taxifare.lewagon.ai/predict'


def get_data():
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None


st.title("Get your fare estimate !")
if st.button("Estimate"):
    with st.spinner("Loading..."):
        data = get_data()

    if data:
        st.success("Data fetched successfully!")
        st.json(data)
    else:
        st.error("Failed to fetch data")
