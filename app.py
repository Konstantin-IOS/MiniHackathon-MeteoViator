import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
from retry_requests import retry
import openmeteo_requests
import requests_cache
import numpy as np
import altair as alt
from geopy.geocoders import Nominatim
from streamlit_extras.let_it_rain import rain


col1, col2 = st.columns([3, 1])

with col1:
    st.title("Meteo Viator")
    st.subheader("Der Virtuelle-Wetter-Zeitreisende")
    st.write("Ein Projekt von Konstantin Guba für den MiniHackathon")

with col2:
    st.image("cloudy.png", use_column_width=True)

st.divider()

# Benutzereingaben für Stadt, Postleitzahl, Land und Datum
city = st.text_input("Stadt", value="Freiburg")
zip_code = st.text_input("Postleitzahl", value="79")
start_date = st.date_input("Startdatum", value=datetime.now() - timedelta(days=3))
end_date = st.date_input("Enddatum", value=datetime.now())

# Umwandeln der Daten in das benötigte Format
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# Geocoder initialisieren
geolocator = Nominatim(user_agent="my_geocoder")

# Funktion zur Ermittlung der Koordinaten
def get_coordinates(city, zip_code):
    if city:
        location = geolocator.geocode(f"{city}, Deutschland")
    else:
        location = None
    
    if not location and zip_code:
        location = geolocator.geocode(f"Deutschland {zip_code}")

    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Koordinaten ermitteln
latitude, longitude = get_coordinates(city, zip_code)

if latitude is not None and longitude is not None:
    

    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date_str,
        "end_date": end_date_str,
        "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m,sunshine_duration"
    }

    
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    
    if st.button("Wetterdaten abrufen"):
        try:
            rain(emoji='🌤️', font_size=54, falling_speed=6, animation_length="1")
            
            responses = openmeteo.weather_api(url, params=params)

            
            response = responses[0]

            
            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_wind_speed_10m = hourly.Variables(1).ValuesAsNumpy()
            hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()
            hourly_sunshine_duration = hourly.Variables(3).ValuesAsNumpy()

            hourly_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive="left"
                ),
                "temperature_2m": hourly_temperature_2m,
                "wind_speed_10m": hourly_wind_speed_10m,
                "relative_humidity_2m": hourly_relative_humidity_2m,
                "sunshine_duration": hourly_sunshine_duration
            }

            hourly_dataframe = pd.DataFrame(data=hourly_data)
            

            # Durchschnittswerte und Änderungen berechnen
            avg_temp = hourly_dataframe["temperature_2m"].mean()
            avg_wind_speed = hourly_dataframe["wind_speed_10m"].mean()

            # Sonnenstunden pro Tag berechnen
            daily_sunshine = hourly_dataframe.groupby(hourly_dataframe['date'].dt.date)["sunshine_duration"].sum()
            avg_sunshine_duration_per_day = daily_sunshine.mean()

            col1, col2, col3 = st.columns(3)
            col1.metric(label="Durchschnitts-Temperatur", value=f"{avg_temp:.2f} °C")
            col2.metric(label="Durchschnitts-Windgeschwindigkeit", value=f"{avg_wind_speed:.2f} km/h")
            col3.metric(label="Durchschnittliche Sonnenstunden", value=f"{avg_sunshine_duration_per_day / 3600:.2f} h/Tag")
            st.divider()
            # Layout mit zwei Spalten auf gleicher Höhe anordnen
            
            col1, col2 = st.columns(2)

            with col1:
                st.write("#### Wetterdaten-Tabelle")
                st.write(hourly_dataframe)
                

            with col2:
                st.write("#### Temperaturverlauf")
                
                # Altair Chart erstellen
                chart = alt.Chart(hourly_dataframe).mark_line().encode(
                    x='date:T',
                    y=alt.Y('temperature_2m:Q', scale=alt.Scale(domain=[-40, 50]))
                ).properties(
                    width=600,
                    height=425
                )
                st.altair_chart(chart, use_container_width=True)

        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")
else:
    st.error("Koordinaten konnten nicht ermittelt werden. Bitte überprüfe die Eingaben für Stadt und Postleitzahl.")
