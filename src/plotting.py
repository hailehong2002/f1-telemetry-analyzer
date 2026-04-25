import matplotlib.pyplot as plt
import numpy as np


def plot_racing_map(telemetry_data, drivers):
    plt.figure(figsize=(10, 10))

    base_tel = telemetry_data[drivers[0]]

    plt.plot(
        base_tel["X"],
        base_tel["Y"],
        color="black",
        linewidth=10,
        alpha=0.25,
        solid_capstyle="round"
    )

    colors = {
        "VER": "red",
        "HAM": "cyan"
    }

    for driver in drivers:
        tel = telemetry_data[driver]
        plt.plot(
            tel["X"],
            tel["Y"],
            color=colors.get(driver, None),
            linewidth=1.4,
            label=driver
        )

    all_x = np.concatenate([telemetry_data[d]["X"] for d in drivers])
    all_y = np.concatenate([telemetry_data[d]["Y"] for d in drivers])

    padding_x = (all_x.max() - all_x.min()) * 0.03
    padding_y = (all_y.max() - all_y.min()) * 0.03

    plt.xlim(all_x.min() - padding_x, all_x.max() + padding_x)
    plt.ylim(all_y.min() - padding_y, all_y.max() + padding_y)

    plt.title("Racing Map")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.axis("off")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_telemetry_dashboard(
    common_distance,
    interpolated,
    driver_a,
    driver_b,
    speed_delta,
    time_delta
):
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))

    a = interpolated[driver_a]
    b = interpolated[driver_b]

    axs[0, 0].plot(common_distance, a["speed"], label=f"{driver_a} Speed")
    axs[0, 0].plot(common_distance, b["speed"], label=f"{driver_b} Speed")
    axs[0, 0].set_title("Speed Comparison")
    axs[0, 0].set_xlabel("Distance (m)")
    axs[0, 0].set_ylabel("Speed (km/h)")
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    axs[0, 1].plot(common_distance, speed_delta)
    axs[0, 1].axhline(0, color="black", linewidth=1)
    axs[0, 1].set_title(f"Speed Delta ({driver_a} - {driver_b})")
    axs[0, 1].set_xlabel("Distance (m)")
    axs[0, 1].set_ylabel("Speed Delta (km/h)")
    axs[0, 1].grid(True)

    axs[1, 0].plot(common_distance, a["throttle"], label=f"{driver_a} Throttle")
    axs[1, 0].plot(common_distance, b["throttle"], label=f"{driver_b} Throttle")
    axs[1, 0].set_title("Throttle Comparison")
    axs[1, 0].set_xlabel("Distance (m)")
    axs[1, 0].set_ylabel("Throttle (%)")
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    axs[1, 1].plot(common_distance, a["brake"], label=f"{driver_a} Brake")
    axs[1, 1].plot(common_distance, b["brake"], label=f"{driver_b} Brake")
    axs[1, 1].set_title("Brake Comparison")
    axs[1, 1].set_xlabel("Distance (m)")
    axs[1, 1].set_ylabel("Brake On/Off")
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    plt.tight_layout()
    plt.show()


def plot_time_delta(common_distance, time_delta, driver_a, driver_b):
    plt.figure(figsize=(14, 5))

    plt.plot(common_distance, time_delta)
    plt.axhline(0, color="black", linewidth=1)

    plt.fill_between(
        common_distance,
        time_delta,
        0,
        where=(time_delta < 0),
        alpha=0.3,
        label=f"{driver_a} faster"
    )

    plt.fill_between(
        common_distance,
        time_delta,
        0,
        where=(time_delta > 0),
        alpha=0.3,
        label=f"{driver_b} faster"
    )

    plt.title(f"Lap Time Delta ({driver_a} - {driver_b})")
    plt.xlabel("Distance (m)")
    plt.ylabel("Time Delta (s)")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_detected_corners(common_distance, speed_a, speed_b, corners, driver_a, driver_b):
    plt.figure(figsize=(14, 5))

    plt.plot(common_distance, speed_a, label=f"{driver_a} Speed")
    plt.plot(common_distance, speed_b, label=f"{driver_b} Speed")

    for idx, (_, _, start_d, end_d) in enumerate(corners, start=1):
        plt.axvspan(start_d, end_d, alpha=0.2)
        plt.text(
            (start_d + end_d) / 2,
            min(speed_a.min(), speed_b.min()) + 10,
            f"C{idx}",
            ha="center"
        )

    plt.title("Detected Corners on Speed Trace")
    plt.xlabel("Distance (m)")
    plt.ylabel("Speed (km/h)")
    plt.grid(True)
    plt.legend()
    plt.show()