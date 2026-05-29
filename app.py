import streamlit as st
import requests
import pandas as pd
import datetime

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''
pickup_date = st.date_input('date and time', min_value=datetime.date(2009, 1, 1))
pickup_time = st.time_input('time')
pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)
pickup_longitude = st.number_input('pickup longitude', format="%.6f")
pickup_latitude = st.number_input('pickup latitude', format="%.6f")
dropoff_longitude = st.number_input('dropoff longitude', format="%.6f")
dropoff_latitude = st.number_input('dropoff latitude', format="%.6f")
passenger_count = st.number_input('passenger count')


'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''


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


st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''


st.title("API Data Fetcher")
if st.button("Fetch Data"):
    with st.spinner("Loading..."):
        data = get_data()

    if data:
        st.success("Data fetched successfully!")
        st.json(data)
    else:
        st.error("Failed to fetch data")
