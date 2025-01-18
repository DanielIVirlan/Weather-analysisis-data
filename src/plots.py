import datetime as dt


def plot_weather_data(df, city_name, axes, row):
    current_time = dt.datetime.now()
    closest_time_idx = (df["time"] - current_time).abs().idxmin()

    axes[row, 0].plot(
        df["time"], df["temperature"], label="Temperature (°C)", color="blue"
    )
    axes[row, 0].set_title(f"Hourly Temperature {city_name}")
    axes[row, 0].set_xlabel("Time")
    axes[row, 0].set_ylabel("Temperature (°C)")
    axes[row, 0].grid()
    axes[row, 0].legend()

    axes[row, 0].annotate(
        f"{df['temperature'].iloc[closest_time_idx]:.2f} °C",
        xy=(
            df["time"].iloc[closest_time_idx],
            df["temperature"].iloc[closest_time_idx],
        ),
        xytext=(
            df["time"].iloc[closest_time_idx],
            df["temperature"].iloc[closest_time_idx] + 0.5,
        ),
        arrowprops=dict(arrowstyle="->", color="blue"),
        color="blue",
        fontsize=10,
        ha="center",
    )

    axes[row, 1].plot(
        df["time"], df["humidity"], label="humidity (g / m³)", color="green"
    )
    axes[row, 1].set_title(f"Hourly humidity {city_name}")
    axes[row, 1].set_xlabel("Time")
    axes[row, 1].set_ylabel("humidity (g / m³)")
    axes[row, 1].grid()
    axes[row, 1].legend()

    axes[row, 1].annotate(
        f"{df['humidity'].iloc[closest_time_idx]:.2f} g / m³",
        xy=(df["time"].iloc[closest_time_idx], df["humidity"].iloc[closest_time_idx]),
        xytext=(
            df["time"].iloc[closest_time_idx],
            df["humidity"].iloc[closest_time_idx] + 0.5,
        ),
        arrowprops=dict(arrowstyle="->", color="green"),
        color="green",
        fontsize=10,
        ha="center",
    )


def plot_wind_data(df, city_name, ax):
    current_time = dt.datetime.now()
    closest_time_idx = (df["time"] - current_time).abs().idxmin()

    ax.plot(df["time"], df["wind_speed"], label="Wind Speed (m/s)", color="purple")
    ax.set_title(f"Hourly Wind Speed {city_name}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Wind Speed (m/s)")
    ax.grid()
    ax.legend()

    ax.annotate(
        f"{df['wind_speed'].iloc[closest_time_idx]:.2f} m/s",
        xy=(df["time"].iloc[closest_time_idx], df["wind_speed"].iloc[closest_time_idx]),
        xytext=(
            df["time"].iloc[closest_time_idx],
            df["wind_speed"].iloc[closest_time_idx] + 0.5,
        ),
        arrowprops=dict(arrowstyle="->", color="purple"),
        color="purple",
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
    ax.set_title(f"Comparison of {label1}")
    ax.set_xlabel("Time")
    ax.set_ylabel(label1 if data_type == "temperature" else label2)
    ax.grid()
    ax.legend()
