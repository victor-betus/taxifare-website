import streamlit as st
import requests
import pandas as pd
import datetime


st.markdown("""
    <style>
    .stApp {
        background-image: url("https://www.civitatis.com/f/estados-unidos/nueva-york/galeria/carteles-publicitarios-times-square.jpg");
        background-size: cover;
        background-color: rgba(255,255,255,0.8);
        background-blend-mode: lighten;
    }
    </style>
""", unsafe_allow_html=True)

'''
# TaxiFare AI

## Enter your ride details and get your fare estimate!
'''

pickup_date = st.date_input('date and time', min_value=datetime.date(2009, 1, 1), value=datetime.date(2019, 7, 6))
pickup_time = st.time_input('time', value=datetime.time(8, 45))
pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)
pickup_longitude = st.number_input('pickup longitude', format="%.6f",value=-73.950655 )
pickup_latitude = st.number_input('pickup latitude', format="%.6f", value=40.783282)
dropoff_longitude = st.number_input('dropoff longitude', format="%.6f", value=-73.984365)
dropoff_latitude = st.number_input('dropoff latitude', format="%.6f", value=40.769802)
passenger_count = st.number_input('passenger count', value=2)


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
        st.success(f"Estimated fare: ${data['fare']:.2f}")
    else:
        st.error("Failed to fetch data")
