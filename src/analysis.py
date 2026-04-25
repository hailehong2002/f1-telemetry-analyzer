import numpy as np


def compute_speed_delta(interpolated, driver_a, driver_b):
    return interpolated[driver_a]["speed"] - interpolated[driver_b]["speed"]


def compute_time_delta(interpolated, driver_a, driver_b):
    return interpolated[driver_a]["time"] - interpolated[driver_b]["time"]


def detect_corners(common_distance, speed_a, speed_b):
    avg_speed = (speed_a + speed_b) / 2

    threshold = np.percentile(avg_speed, 30)
    
    is_corner = avg_speed < threshold

    corners = []
    in_corner = False
    start_idx = 0

    for i in range(len(is_corner)):
        if is_corner[i] and not in_corner:
            start_idx = i
            in_corner = True

        if not is_corner[i] and in_corner:
            end_idx = i
            in_corner = False

            start_dist = common_distance[start_idx]
            end_dist = common_distance[end_idx]

            if end_dist - start_dist > 50:
                corners.append((start_idx, end_idx, start_dist, end_dist))

    return corners


def analyze_driver_decisions(
    corners,
    common_distance,
    interpolated,
    time_delta,
    driver_a,
    driver_b
):
    results = []

    for idx, (start_i, end_i, start_d, end_d) in enumerate(corners, start=1):
        delta_start = time_delta[start_i]
        delta_end = time_delta[end_i - 1]
        time_gain = delta_end - delta_start

        if time_gain < 0:
            winner = driver_a
            loser = driver_b
        elif time_gain > 0:
            winner = driver_b
            loser = driver_a
        else:
            winner = "Equal"
            loser = "Equal"

        reasons = []

        if winner != "Equal":
            w = interpolated[winner]
            l = interpolated[loser]

            winner_exit_speed = w["speed"][end_i - 1]
            loser_exit_speed = l["speed"][end_i - 1]

            winner_min_speed = np.min(w["speed"][start_i:end_i])
            loser_min_speed = np.min(l["speed"][start_i:end_i])

            winner_throttle = np.mean(w["throttle"][start_i:end_i])
            loser_throttle = np.mean(l["throttle"][start_i:end_i])

            winner_brake = np.sum(w["brake"][start_i:end_i])
            loser_brake = np.sum(l["brake"][start_i:end_i])

            if winner_exit_speed > loser_exit_speed:
                reasons.append("higher exit speed")

            if winner_min_speed > loser_min_speed:
                reasons.append("higher minimum corner speed")

            if winner_throttle > loser_throttle:
                reasons.append("more throttle through corner")

            if winner_brake < loser_brake:
                reasons.append("less braking")

        if not reasons:
            reasons.append("mixed inputs or small difference")

        results.append({
            "corner": idx,
            "start_distance": start_d,
            "end_distance": end_d,
            "winner": winner,
            "time_gain": time_gain,
            "reason": ", ".join(reasons)
        })

    return results


def print_decision_analysis(results):
    print("\n===== DRIVER DECISION ANALYSIS =====")

    for r in results:
        print(
            f"Corner {r['corner']} "
            f"({r['start_distance']:.0f}m - {r['end_distance']:.0f}m):\n"
            f"  Winner: {r['winner']}\n"
            f"  Time gain: {r['time_gain']:+.3f}s\n"
            f"  Reason: {r['reason']}\n"
        )