import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dataset import df_rome, df_suceava
from plots import plot_weather_data, plot_overlay, plot_comparison, plot_wind_data
from tabulate import tabulate


table_rome = tabulate(df_rome, headers="keys", tablefmt="pretty")
table_suceava = tabulate(df_suceava, headers="keys", tablefmt="pretty")

folder_path = "data"

file_name1 = "Rome"
file_name2 = "Suceava"

file_path1 = os.path.join(folder_path, file_name1 + ".csv")
file_path2 = os.path.join(folder_path, file_name2 + ".csv")

with open(file_path1, "w") as f:
    f.write(table_rome)

with open(file_path2, "w") as f:
    f.write(table_suceava)


fig, axes = plt.subplots(5, 2, figsize=(15, 25), sharex=True)

plot_weather_data(df_rome, "Rome", axes, 0)
plot_weather_data(df_suceava, "Suceava", axes, 1)


plot_overlay(df_rome, "Rome", axes[3, 0])
plot_overlay(df_suceava, "Suceava", axes[3, 1])

plot_comparison(
    df_rome,
    df_suceava,
    "Rome",
    "Suceava",
    axes[4, 0],
    "temperature",
    "Temperature (°C)",
    "",
    "blue",
    "red",
)
plot_comparison(
    df_rome,
    df_suceava,
    "Rome",
    "Suceava",
    axes[4, 1],
    "humidity",
    "Humidity (g / m³)",
    "",
    "green",
    "orange",
)

plot_wind_data(df_rome, "Rome", axes[2, 0])
plot_wind_data(df_suceava, "Suceava", axes[2, 1])

for ax_row in axes:
    for ax in ax_row:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=7))
        ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.show()
