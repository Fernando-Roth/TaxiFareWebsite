import streamlit as st
import requests
import numpy as np
import pandas as pd
import datetime
import urllib.parse



'''
# NY Taxi Fare prediction interface
'''
expander = st.expander("Optional controls")

expander = expander.radio("Type ", ["Lat and lon", "Address"])

if expander == 'Address':
    columns = st.columns(7)

    pickup_date = columns[0].date_input("pickup datetime",
                                value=datetime.datetime(2012, 10, 6, 12, 10, 20))
    pickup_time = columns[1].time_input("pickup datetime",
                                value=datetime.datetime(2012, 10, 6, 12, 10, 20))
    pickup_datetime = f'{pickup_date} {pickup_time}'

    start_point =columns[2].text_input("Starting point", "Empire State Building, New York")

    ending_point = columns[3].text_input("Ending point", "Central Park, New York")

    dropoff_longitude = columns[4].text_input("dropoff_longitude" ,'40.6513111' )

    dropoff_latitude = columns[5].text_input('dropoff latitude', "-73.8803331")

    passenger_count = columns[6].text_input('passenger count',"2" )

    #Strating point:
    url_location_sp = "https://nominatim.openstreetmap.org/search/" + urllib.parse.quote(
        start_point) + "?format=json"
    response_sp = requests.get(url_location_sp).json()
    pickup_longitude = response_sp[0]["lat"]
    pickup_latitude = response_sp[0]["lon"]

    # Ending point:
    url_location_ep = "https://nominatim.openstreetmap.org/search/" + urllib.parse.quote(
        ending_point) + "?format=json"
    response_ep = requests.get(url_location_ep).json()
    dropoff_longitude = response_ep[0]["lat"]
    dropoff_latitude = response_ep[0]["lon"]


else:
    columns = st.columns(7)

    pickup_date = columns[0].date_input("pickup datetime",
                                value=datetime.datetime(2012, 10, 6, 12, 10, 20))
    pickup_time = columns[1].time_input("pickup datetime",
                                value=datetime.datetime(2012, 10, 6, 12, 10, 20))
    pickup_datetime = f'{pickup_date} {pickup_time}'

    pickup_longitude = columns[2].text_input('pickup longitude',"40.7614327")

    pickup_latitude = columns[3].text_input('pickup latitude', "-73.9798156")

    dropoff_longitude = columns[4].text_input("dropoff_longitude" ,'40.6513111' )

    dropoff_latitude = columns[5].text_input('dropoff latitude', "-73.8803331")

    passenger_count = columns[6].text_input('passenger count',"2" )





@st.cache
def get_map_data():

    return pd.DataFrame([(float(pickup_longitude), float(pickup_latitude)),
                         (float(dropoff_longitude), float(pickup_latitude))],
                        columns=['lat', 'lon'])


df = get_map_data()

st.map(df)


url = 'https://taxifare.lewagon.ai/predict'


parameters = {
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}
x = requests.get(url, params=parameters)
st.write("Taxi Fare prediction : " , x.json()["prediction"])
