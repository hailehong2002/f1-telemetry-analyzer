import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def show_ghost_replay(
    telemetry_data,
    common_distance,
    interpolated,
    time_delta,
    driver_a,
    driver_b,
    corners=None
):
    a = interpolated[driver_a]
    b = interpolated[driver_b]

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.plot(
        telemetry_data[driver_a]["X"],
        telemetry_data[driver_a]["Y"],
        color="lightgray",
        linewidth=1
    )

    # Draw corner zones on the track background
    if corners:
        for corner_num, (start_i, end_i, _, _) in enumerate(corners, start=1):
            ax.plot(
                a["x"][start_i:end_i],
                a["y"][start_i:end_i],
                color="yellow",
                linewidth=6,
                alpha=0.4,
                zorder=1
            )
            mid_i = (start_i + end_i) // 2
            ax.text(
                a["x"][mid_i],
                a["y"][mid_i],
                str(corner_num),
                fontsize=7,
                color="darkorange",
                ha="center",
                va="center",
                zorder=2
            )

    # Build a lookup: frame index -> corner number (0 = not in corner)
    corner_at = [0] * len(common_distance)
    if corners:
        for corner_num, (start_i, end_i, _, _) in enumerate(corners, start=1):
            for i in range(start_i, end_i):
                corner_at[i] = corner_num

    ax.set_title(f"Ghost Replay - {driver_a} vs {driver_b}")
    ax.set_aspect("equal")
    ax.axis("off")

    car_a, = ax.plot([], [], "o", markersize=10, label=driver_a, zorder=5)
    car_b, = ax.plot([], [], "o", markersize=10, label=driver_b, zorder=5)

    trail_a, = ax.plot([], [], linewidth=2, alpha=0.7, zorder=4)
    trail_b, = ax.plot([], [], linewidth=2, alpha=0.7, zorder=4)

    info_text = ax.text(
        0.02,
        0.95,
        "",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top"
    )

    corner_label = ax.text(
        0.5,
        0.05,
        "",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        color="darkorange",
        ha="center",
        va="bottom"
    )

    ax.legend(loc="upper right")

    def update(frame):
        car_a.set_data([a["x"][frame]], [a["y"][frame]])
        car_b.set_data([b["x"][frame]], [b["y"][frame]])

        trail_start = max(0, frame - 25)

        trail_a.set_data(
            a["x"][trail_start:frame],
            a["y"][trail_start:frame]
        )

        trail_b.set_data(
            b["x"][trail_start:frame],
            b["y"][trail_start:frame]
        )

        current_time_delta = time_delta[frame]

        if current_time_delta < 0:
            leader = driver_a
        elif current_time_delta > 0:
            leader = driver_b
        else:
            leader = "Equal"

        info_text.set_text(
            f"Distance: {common_distance[frame]:.0f} m\n"
            f"{driver_a} speed: {a['speed'][frame]:.1f} km/h\n"
            f"{driver_b} speed: {b['speed'][frame]:.1f} km/h\n"
            f"Time delta: {current_time_delta:+.3f} s\n"
            f"Leader: {leader}"
        )

        cn = corner_at[frame]
        corner_label.set_text(f"CORNER {cn}" if cn else "")

        return car_a, car_b, trail_a, trail_b, info_text, corner_label

    ani = FuncAnimation(
        fig,
        update,
        frames=len(common_distance),
        interval=30,
        blit=True
    )

    plt.show()

    return ani