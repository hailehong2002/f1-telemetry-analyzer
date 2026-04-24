import os
import fastf1
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

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


# =========================
# 2. Compare racing line
# =========================
plt.figure(figsize=(10, 6))

for driver in drivers:
    tel = telemetry_data[driver]
    plt.plot(tel["X"], tel["Y"], label=driver, linewidth=2)

plt.title("Racing Line Comparison - 2023 Hungary Qualifying")
plt.axis("equal")
plt.axis("off")
plt.legend()
plt.show()

# =========================
# 3. Compare speed
# =========================
plt.figure(figsize=(12, 6))
for driver in drivers:
    tel = telemetry_data[driver]
    plt.plot(tel["Distance"], tel["Speed"], label=f"{driver} Speed")

plt.title("Speed Comparison Over Lap Distance")
plt.xlabel("Distance around lap (m)")
plt.ylabel("Speed km/h")
plt.grid(True)
plt.legend()
plt.show()

# =========================
# 3. Delta speed to see who is faster
# =========================
tel_ver = telemetry_data["VER"]
tel_ham = telemetry_data["HAM"]

common_distance = np.linspace(
    0,
    min(tel_ver["Distance"].max(), tel_ham["Distance"].max()),
    1000
)

speed_ver = np.interp(common_distance, tel_ver["Distance"], tel_ver["Speed"])
speed_ham = np.interp(common_distance, tel_ham["Distance"], tel_ham["Speed"])

delta = speed_ver - speed_ham  #delta > 0: ver faster else delta < 0: ham faster
#plotting delta
plt.figure(figsize=(12, 6))

plt.plot(common_distance, delta)
plt.axhline(0)

plt.title("Speed Delta (VER - HAM)")
plt.xlabel("Distance (m)")
plt.ylabel("Speed Difference (km/h)")
plt.grid(True)

plt.show()