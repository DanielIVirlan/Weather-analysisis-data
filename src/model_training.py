import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt


def fetch_weather_data(
    latitude, longitude, start_date="2020-01-01", end_date="2024-12-31"
):
    url = "https://archive-api.open-meteo.com/v1/era5"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data")
        exit()


def fetch_future_weather_data(
    latitude, longitude, start_date="2025-01-01", end_date="2025-01-31"
):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
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


def prepare_features(df):
    df["hour"] = df["time"].dt.hour
    df["day_of_week"] = df["time"].dt.dayofweek
    df["month"] = df["time"].dt.month
    return df[["hour", "day_of_week", "month", "humidity", "wind_speed"]], df[
        "temperature"
    ]


# loading hystorical data
data_rome = fetch_weather_data(41.8919, 12.5113)
df = create_dataframe(data_rome)

# loading future data
data_future = fetch_future_weather_data(41.8919, 12.5113)
df_future = create_dataframe(data_future)

# processing future data
X_future, _ = prepare_features(df_future)

# processing hystorical data
X, y = prepare_features(df)

# data split for training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# standardization of the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_future_scaled = scaler.transform(X_future)

# creating the random forest model and training it on the data from the past
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# prediction on the test data and future data
y_pred = model.predict(X_test_scaled)
y_pred_future = model.predict(X_future_scaled)

df_future["predicted_temperature"] = y_pred_future

# model evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

# error evaluation
print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")


# graph of the real and predicted temperatures
plt.figure(figsize=(14, 6))

# sub plot 1: historical data
plt.subplot(1, 2, 1)
plt.plot(
    df["time"],
    df["temperature"],
    label="Real Temperatures (Historical Data)",
    color="blue",
)
plt.plot(
    df["time"],
    model.predict(scaler.transform(X)),
    label="Predicted Temperatures (Model)",
    color="red",
)
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Training model and testing on historical data predictions")
plt.legend()
plt.grid(True)

# sub plot 2: future data
plt.subplot(1, 2, 2)
plt.plot(
    df_future["time"],
    df_future["temperature"],
    label="Real Temperatures (API)",
    color="blue",
)
plt.plot(
    df_future["time"],
    df_future["predicted_temperature"],
    label="Predicted Temperatures (Model)",
    color="red",
)
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Future Predictions: Real vs Predicted Temperatures")
plt.legend()
plt.grid(True)

# graph display
plt.tight_layout()
plt.show()
