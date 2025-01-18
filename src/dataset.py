import requests
import pandas as pd
import datetime as dt
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
    current_time = dt.datetime.now()
    closest_time_idx = (df["time"] - current_time).abs().idxmin()
    # Plot temperature
    axes[row, 0].plot(
        df["time"], df["temperature"], label="Temperature (°C)", color="blue"
    )
    axes[row, 0].set_title(f"Hourly Temperature {city_name}")
    axes[row, 0].set_xlabel("Time")
    axes[row, 0].set_ylabel("Temperature (°C)")
    axes[row, 0].grid()
    axes[row, 0].legend()

    # Annotate last temperature value
    axes[row, 0].annotate(
        f"{df['temperature'].iloc[closest_time_idx]:.2f} °C",  # Last temperature value
        xy=(
            df["time"].iloc[closest_time_idx],
            df["temperature"].iloc[closest_time_idx],
        ),
        xytext=(
            df["time"].iloc[closest_time_idx],
            df["temperature"].iloc[closest_time_idx] + 0.5,
        ),  # Adjust annotation position
        arrowprops=dict(arrowstyle="->", color="blue"),
        color="blue",
        fontsize=10,
        ha="center",
    )

    # Plot wind speed
    axes[row, 1].plot(
        df["time"], df["humidity"], label="humidity (g / m³)", color="green"
    )
    axes[row, 1].set_title(f"Hourly humidity {city_name}")
    axes[row, 1].set_xlabel("Time")
    axes[row, 1].set_ylabel("humidity (g / m³)")
    axes[row, 1].grid()
    axes[row, 1].legend()

    # Annotate last wind speed value
    axes[row, 1].annotate(
        f"{df['humidity'].iloc[closest_time_idx]:.2f} g / m³",  # Last wind speed value
        xy=(df["time"].iloc[closest_time_idx], df["humidity"].iloc[closest_time_idx]),
        xytext=(
            df["time"].iloc[closest_time_idx],
            df["humidity"].iloc[closest_time_idx] + 0.5,
        ),  # Adjust annotation position
        arrowprops=dict(arrowstyle="->", color="green"),
        color="green",
        fontsize=10,
        ha="center",
    )


def plot_overlay(df, city_name, ax):
    ax2 = ax.twinx()

    ax.plot(
        df["time"],
        df["temperature"],
        label="Temperature (°C)",
        color="blue",
        linewidth=1.5,
    )
    ax.set_ylabel("Temperature (°C)", color="blue")
    ax.tick_params(axis="y", labelcolor="blue")
    ax.grid()

    ax2.plot(
        df["time"],
        df["humidity"],
        label="humidity (g / m³)",
        color="green",
        linewidth=1.5,
    )
    ax2.set_ylabel("humidity (g / m³)", color="green")
    ax2.tick_params(axis="y", labelcolor="green")

    ax.set_title(f"Overlay: Temperature and humidity - {city_name}")

    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")


def plot_comparison(
    df1, df2, city1, city2, ax, data_type, label1, label2, color1, color2
):
    ax.plot(df1["time"], df1[data_type], label=f"{label1} ({city1})", color=color1)
    ax.plot(
        df2["time"],
        df2[data_type],
        label=f"{label2} ({city2})",
        color=color2,
        linestyle="--",
    )
    ax.set_title(f"Comparison of {label1} and {label2}")
    ax.set_xlabel("Time")
    ax.set_ylabel(label1 if data_type == "temperature" else label2)
    ax.grid()
    ax.legend()


# Fetch data for Rome and Suceava
data_rome = fetch_weather_data(41.8919, 12.5113)
data_suceava = fetch_weather_data(47.6333, 26.25)

# Create DataFrames
df_rome = create_dataframe(data_rome)
df_suceava = create_dataframe(data_suceava)

# Create a figure with 2 rows and 2 columns
fig, axes = plt.subplots(4, 2, figsize=(15, 20), sharex=True)

# Plot data for Rome and Suceava
plot_weather_data(df_rome, "Rome", axes, 0)
plot_weather_data(df_suceava, "Suceava", axes, 1)

plot_overlay(df_rome, "Rome", axes[2, 0])
plot_overlay(df_suceava, "Suceava", axes[2, 1])

plot_comparison(
    df_rome,
    df_suceava,
    "Rome",
    "Suceava",
    axes[3, 0],
    "temperature",
    "Temperature (°C)",
    "Temperature (°C)",
    "blue",
    "red",
)
plot_comparison(
    df_rome,
    df_suceava,
    "Rome",
    "Suceava",
    axes[3, 1],
    "humidity",
    "Humidity (%)",
    "Humidity (%)",
    "green",
    "orange",
)

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
