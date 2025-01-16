import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Function to fetch data from the API
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


# Function to create a DataFrame from the fetched data
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


# Function to plot the data
def plot_weather_data(df, city_name, axes, row):
    axes[row, 0].plot(
        df["time"], df["temperature"], label="Temperature (°C)", color="blue"
    )
    axes[row, 0].set_title(f"Hourly Temperature {city_name}")
    axes[row, 0].set_xlabel("Time")
    axes[row, 0].set_ylabel("Temperature (°C)")
    axes[row, 0].grid()
    axes[row, 0].legend()

    axes[row, 1].plot(
        df["time"], df["wind_speed"], label="Wind Speed (m/s)", color="green"
    )
    axes[row, 1].set_title(f"Hourly Wind Speed {city_name}")
    axes[row, 1].set_xlabel("Time")
    axes[row, 1].set_ylabel("Wind Speed (m/s)")
    axes[row, 1].grid()
    axes[row, 1].legend()


# Fetch data for Rome and Suceava
data_rome = fetch_weather_data(41.8919, 12.5113)
data_suceava = fetch_weather_data(47.6333, 26.25)

# Create DataFrames
df_rome = create_dataframe(data_rome)
df_suceava = create_dataframe(data_suceava)

# Create a figure with 2 rows and 2 columns
fig, axes = plt.subplots(2, 2, figsize=(15, 10), sharex=True)

# Plot data for Rome and Suceava
plot_weather_data(df_rome, "Rome", axes, 0)
plot_weather_data(df_suceava, "Suceava", axes, 1)

# Customize the X-axis for all subplots
for ax_row in axes:
    for ax in ax_row:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=7))
        ax.tick_params(axis="x", rotation=45)

# Adjust the layout
plt.tight_layout()

# Show the plots
plt.show()
