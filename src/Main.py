import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dataset import df_rome, df_suceava
from plots import plot_weather_data, plot_overlay, plot_comparison

# Creazione dei grafici
fig, axes = plt.subplots(4, 2, figsize=(15, 20), sharex=True)

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
    "",
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
    "Humidity (g / m³)",
    "",
    "green",
    "orange",
)

# Personalizzazione dell'asse X per tutti i subplot
for ax_row in axes:
    for ax in ax_row:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=7))
        ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.show()
