import os
import fastf1
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")

# Load session
session = fastf1.get_session(2023, "Hungary", "Q")
session.load()

drivers = ["VER", "HAM"]
telemetry_data = {}

# =========================
# 1. Get drivers data
# =========================
for driver in drivers:
    # Pick fastest lap
    lap = session.laps.pick_drivers(driver).pick_fastest()
    # Get telemetry
    tel = lap.get_telemetry().add_distance()
    telemetry_data[driver] = tel
    print(f"{driver} fastest lap: {lap['LapTime']}")

tel_ver = telemetry_data["VER"]
tel_ham = telemetry_data["HAM"]

common_distance = np.linspace(
    0,
    min(tel_ver["Distance"].max(), tel_ham["Distance"].max()),
    1000
)

# Interpolated data
speed_ver = np.interp(common_distance, tel_ver["Distance"], tel_ver["Speed"])
speed_ham = np.interp(common_distance, tel_ham["Distance"], tel_ham["Speed"])

delta = speed_ver - speed_ham

throttle_ver = np.interp(common_distance, tel_ver["Distance"], tel_ver["Throttle"])
throttle_ham = np.interp(common_distance, tel_ham["Distance"], tel_ham["Throttle"])

brake_ver = np.interp(common_distance, tel_ver["Distance"], tel_ver["Brake"].astype(int))
brake_ham = np.interp(common_distance, tel_ham["Distance"], tel_ham["Brake"].astype(int))

time_ver = np.interp(common_distance, tel_ver["Distance"], tel_ver["Time"].dt.total_seconds())
time_ham = np.interp(common_distance, tel_ham["Distance"], tel_ham["Time"].dt.total_seconds())

# =========================
# 2. Separate Racing Line Plot
# =========================
plt.figure(figsize=(10, 10))

for driver in drivers:
    tel = telemetry_data[driver]
    plt.plot(tel["X"], tel["Y"], label=driver, linewidth=2)

plt.title("Racing Line - VER vs HAM")
plt.axis("equal")
plt.axis("off")
plt.legend()
plt.show()

# =========================
# 3. Telemetry Dashboard: Speed, Throttle, Brake, Delta
# =========================
fig, axs = plt.subplots(2, 2, figsize=(16, 10))

# 1. Speed comparison
axs[0, 0].plot(common_distance, speed_ver, label="VER Speed")
axs[0, 0].plot(common_distance, speed_ham, label="HAM Speed")
axs[0, 0].set_title("Speed Comparison")
axs[0, 0].set_xlabel("Distance (m)")
axs[0, 0].set_ylabel("Speed (km/h)")
axs[0, 0].grid(True)
axs[0, 0].legend()

# 2. Speed delta
axs[0, 1].plot(common_distance, delta)
axs[0, 1].axhline(0, color="black", linewidth=1)
axs[0, 1].set_title("Speed Delta (VER - HAM)")
axs[0, 1].set_xlabel("Distance (m)")
axs[0, 1].set_ylabel("Delta (km/h)")
axs[0, 1].grid(True)

# 3. Throttle comparison
axs[1, 0].plot(common_distance, throttle_ver, label="VER Throttle")
axs[1, 0].plot(common_distance, throttle_ham, label="HAM Throttle")
axs[1, 0].set_title("Throttle Comparison")
axs[1, 0].set_xlabel("Distance (m)")
axs[1, 0].set_ylabel("Throttle (%)")
axs[1, 0].grid(True)
axs[1, 0].legend()

# 4. Brake comparison
axs[1, 1].plot(common_distance, brake_ver, label="VER Brake")
axs[1, 1].plot(common_distance, brake_ham, label="HAM Brake")
axs[1, 1].set_title("Brake Comparison")
axs[1, 1].set_xlabel("Distance (m)")
axs[1, 1].set_ylabel("Brake On/Off")
axs[1, 1].grid(True)
axs[1, 1].legend()

plt.tight_layout()
plt.show()

# =========================
# 4. Ghost replay animation
# =========================
replay_distance = common_distance 

x_ver = np.interp(replay_distance, tel_ver["Distance"], tel_ver["X"])
y_ver = np.interp(replay_distance, tel_ver["Distance"], tel_ver["Y"])
s_ver = np.interp(replay_distance, tel_ver["Distance"], tel_ver["Speed"])

x_ham = np.interp(replay_distance, tel_ham["Distance"], tel_ham["X"])
y_ham = np.interp(replay_distance, tel_ham["Distance"], tel_ham["Y"])
s_ham = np.interp(replay_distance, tel_ham["Distance"], tel_ham["Speed"])

fig, ax = plt.subplots(figsize=(8, 8))

ax.plot(tel_ver["X"], tel_ver["Y"], color="lightgray", linewidth=1)
ax.plot(tel_ham["X"], tel_ham["Y"], color="gray", linewidth=1, alpha=0.5)

ax.set_title("Ghost Replay - VER vs HAM")
ax.set_aspect("equal")
ax.axis("off")

car_ver, = ax.plot([], [], "o", markersize=10, label="VER")
car_ham, = ax.plot([], [], "o", markersize=10, label="HAM")

trail_ver, = ax.plot([], [], linewidth=2, alpha=0.7)
trail_ham, = ax.plot([], [], linewidth=2, alpha=0.7)

info_text = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes,
    fontsize=10,
    verticalalignment="top"
)

ax.legend(loc="upper right")

def update(frame):
    car_ver.set_data([x_ver[frame]], [y_ver[frame]])
    car_ham.set_data([x_ham[frame]], [y_ham[frame]])

    trail_start = max(0, frame - 25)

    trail_ver.set_data(x_ver[trail_start:frame], y_ver[trail_start:frame])
    trail_ham.set_data(x_ham[trail_start:frame], y_ham[trail_start:frame])

    speed_delta = s_ver[frame] - s_ham[frame]
    time_delta = time_ver[frame] - time_ham[frame]

    if time_delta > 0:
        faster_now = "VER"
    elif time_delta < 0:
        faster_now = "HAM"
    else:
        faster_now = "Equal"

    info_text.set_text(
        f"Distance: {replay_distance[frame]:.0f} m\n"
        f"VER speed: {s_ver[frame]:.1f} km/h\n"
        f"HAM speed: {s_ham[frame]:.1f} km/h\n"
        f"Speed delta: {speed_delta:+.2f} km/h\n"
        f"Time delta: {time_delta:+.3f} s\n"
        f"Currently faster: {faster_now}"
    )

    return car_ver, car_ham, trail_ver, trail_ham, info_text

ani = FuncAnimation(
    fig,
    update,
    frames=len(replay_distance),
    interval=30,
    blit=True
)

plt.show()
