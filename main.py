from src.config import (
    YEAR,
    GRAND_PRIX,
    SESSION_TYPE,
    DRIVERS,
    CACHE_DIR,
    N_POINTS
)

from src.data_loader import (
    setup_fastf1_cache,
    load_session,
    get_fastest_lap_telemetry
)

from src.preprocessing_data import (
    create_common_distance,
    interpolate_all_drivers
)

from src.analysis import (
    compute_speed_delta,
    compute_time_delta,
    detect_corners,
    analyze_driver_decisions,
    print_decision_analysis
)

from src.plotting import (
    plot_racing_map,
    plot_telemetry_dashboard,
    plot_time_delta,
    plot_detected_corners
)

from src.replay import show_ghost_replay


def main():
    driver_a = DRIVERS[0]
    driver_b = DRIVERS[1]

    setup_fastf1_cache(CACHE_DIR)

    session = load_session(
        YEAR,
        GRAND_PRIX,
        SESSION_TYPE
    )

    telemetry_data, lap_data = get_fastest_lap_telemetry(
        session,
        DRIVERS
    )

    common_distance = create_common_distance(
        telemetry_data,
        DRIVERS,
        N_POINTS
    )

    interpolated = interpolate_all_drivers(
        telemetry_data,
        DRIVERS,
        common_distance
    )

    speed_delta = compute_speed_delta(
        interpolated,
        driver_a,
        driver_b
    )

    time_delta = compute_time_delta(
        interpolated,
        driver_a,
        driver_b
    )

    corners = detect_corners(
        common_distance,
        interpolated[driver_a]["speed"],
        interpolated[driver_b]["speed"]
    )

    decision_results = analyze_driver_decisions(
        corners,
        common_distance,
        interpolated,
        time_delta,
        driver_a,
        driver_b
    )

    plot_racing_map(
        telemetry_data,
        DRIVERS
    )

    plot_telemetry_dashboard(
        common_distance,
        interpolated,
        driver_a,
        driver_b,
        speed_delta,
        time_delta
    )

    plot_time_delta(
        common_distance,
        time_delta,
        driver_a,
        driver_b
    )

    plot_detected_corners(
        common_distance,
        interpolated[driver_a]["speed"],
        interpolated[driver_b]["speed"],
        corners,
        driver_a,
        driver_b
    )

    print_decision_analysis(decision_results)

    show_ghost_replay(
        telemetry_data,
        common_distance,
        interpolated,
        time_delta,
        driver_a,
        driver_b,
        corners=corners
    )


if __name__ == "__main__":
    main()