import requests
import pandas as pd


# Funzioni per gestire i dati (rimangono qui)
def fetch_weather_data(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data")
        exit()


def create_dataframe(data):
    hourly_data = data["hourly"]
    return pd.DataFrame(
        {
            "time": pd.to_datetime(hourly_data["time"]),
            "temperature": hourly_data["temperature_2m"],
            "humidity": hourly_data["relative_humidity_2m"],
            "wind_speed": hourly_data["wind_speed_10m"],
        }
    )


# Fetch data
data_rome = fetch_weather_data(41.8919, 12.5113)
data_suceava = fetch_weather_data(47.6333, 26.25)

df_rome = create_dataframe(data_rome)
df_suceava = create_dataframe(data_suceava)
