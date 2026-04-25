import numpy as np

def create_common_distance(telemetry_data, drivers, n_points=1000):
    max_distance = min(
        telemetry_data[driver]["Distance"].max()
        for driver in drivers
    )

    return np.linspace(0, max_distance, n_points)

def interpolate_driver_data(tel, common_distance):
    data = {
        "x": np.interp(common_distance, tel["Distance"], tel["X"]),
        "y": np.interp(common_distance, tel["Distance"], tel["Y"]),
        "speed": np.interp(common_distance, tel["Distance"], tel["Speed"]),
        "throttle": np.interp(common_distance, tel["Distance"], tel["Throttle"]),
        "brake": np.interp(
            common_distance,
            tel["Distance"],
            tel["Brake"].astype(int)
        ),
        "time": np.interp(
            common_distance,
            tel["Distance"],
            tel["Time"].dt.total_seconds()
        )
    }

    return data

def interpolate_all_drivers(telemetry_data, drivers, common_distance):
    interpolated = {}

    for driver in drivers:
        interpolated[driver] = interpolate_driver_data(
            telemetry_data[driver],
            common_distance
        )

    return interpolated