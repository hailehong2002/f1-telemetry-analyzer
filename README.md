# F1 Telemetry Analyzer

A Python tool for comparing two Formula 1 drivers head-to-head using real telemetry data fetched via the FastF1 library. Given any session (race, qualifying, practice), it detects corners, measures time deltas, animates a ghost replay, and explains where each driver gained or lost time.

---

## Features

| Feature | Description |
|---|---|
| Session loading | Fetches real F1 telemetry via FastF1 with local disk caching |
| Racing line map | Overlays both drivers' GPS traces on a 2-D track map |
| Telemetry dashboard | Side-by-side speed, throttle, and brake traces across the full lap |
| Speed delta | Frame-by-frame speed difference plotted over distance |
| Lap time delta | Cumulative time gap between drivers filled by who is leading |
| Corner detection | Automatically identifies corner zones using a speed-percentile threshold |
| Driver decision analysis | Per-corner breakdown of who gained time and why (exit speed, min speed, throttle, braking) |
| Ghost replay | Animated side-by-side replay with live trails, time delta readout, and corner highlights |

---

## Project Structure

```
f1-telemetry-analyzer/
├── main.py                  # Orchestrates the full pipeline
└── src/
    ├── config.py            # Year, GP, session type, drivers, N_POINTS
    ├── data_loader.py       # FastF1 session loading and telemetry extraction
    ├── preprocessing_data.py# Distance normalisation and interpolation to common grid
    ├── analysis.py          # Speed/time delta, corner detection, decision analysis
    ├── plotting.py          # Static matplotlib visualisations
    └── replay.py            # Animated ghost replay with corner highlights
```

---

## Tech Stack

- **Python 3.10+**
- **FastF1** — official F1 telemetry API wrapper
- **Pandas** — lap/telemetry data frames
- **NumPy** — interpolation and numerical analysis
- **Matplotlib** — all visualisations and animation

---

## Setup

```bash
# Clone the repo
git clone <repo-url>
cd f1-telemetry-analyzer

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install fastf1 matplotlib numpy pandas
```

---

## Configuration

Edit [src/config.py](src/config.py) to change the session or drivers:

```python
YEAR         = 2023
GRAND_PRIX   = "Hungary"
SESSION_TYPE = "Q"          # Q = Qualifying, R = Race, FP1/FP2/FP3
DRIVERS      = ["VER", "HAM"]
N_POINTS     = 1000         # Interpolation resolution along the lap
CACHE_DIR    = "cache"      # FastF1 local cache directory
```

---

## Usage

```bash
python main.py
```

The pipeline runs in order:

1. Cache is initialised and the session is loaded from FastF1.
2. Fastest laps are fetched and resampled onto a common 1000-point distance grid.
3. All static plots open sequentially (close each to advance).
4. A decision analysis is printed to the terminal.
5. The ghost replay animation launches last.

---

## Pipeline Overview

```
load_session()
    └─ get_fastest_lap_telemetry()          # raw telemetry per driver
        └─ create_common_distance()         # shared distance axis
            └─ interpolate_all_drivers()    # resample to common grid
                ├─ compute_speed_delta()
                ├─ compute_time_delta()
                ├─ detect_corners()
                │   └─ analyze_driver_decisions()
                ├─ plot_racing_map()
                ├─ plot_telemetry_dashboard()
                ├─ plot_time_delta()
                ├─ plot_detected_corners()
                └─ show_ghost_replay()
```

---

## Analysis

### Corner Detection

Corners are detected purely from telemetry — no circuit map required. The average speed of both drivers is computed at each point along the lap. Any sample below the **30th percentile** of that average speed is flagged as a corner candidate. Consecutive flagged samples are merged into a single zone, and zones shorter than 50 m are discarded as noise (chicane bumps, slow-speed wiggles, etc.).

Each corner is stored as `(start_index, end_index, start_distance, end_distance)` and numbered from 1 in lap order.

**Strength:** works on any circuit without hard-coded corner lists.  
**Limitation:** the 30th-percentile threshold is circuit-agnostic, so very slow or very fast tracks may produce too many or too few zones. `N_POINTS` also affects corner resolution — lower values merge nearby zones.

---

### Time Delta

The time delta is the difference in cumulative lap time between the two drivers at every point along the lap, computed after resampling both onto the same distance grid:

```
time_delta[i] = time_A[i] - time_B[i]
```

A negative value means Driver A is ahead at that distance; positive means Driver B is ahead. The `plot_time_delta` chart fills the area under the curve so you can instantly read who is gaining and where.

---

### Driver Decision Analysis

For each detected corner the analysis compares four metrics between the two drivers over the corner index range:

| Metric | Interpretation |
|---|---|
| Exit speed | Higher = better corner exit, more straight-line time gained |
| Minimum corner speed | Higher = carrying more speed through the apex |
| Mean throttle | Higher = earlier or more aggressive power application |
| Total brake events | Lower = less braking required, smoother entry |

The winner of each corner is the driver whose cumulative time delta improved (decreased) from entry to exit. The reasons list describes which metrics drove that advantage.

---

### Ghost Replay

The replay animates both cars simultaneously at 30 ms per frame on a 2-D track map. Corner zones detected earlier are drawn as **yellow highlighted bands** on the track background with their corner number. When either car enters a corner zone a bold **CORNER N** banner appears at the bottom of the plot and clears on exit. A 25-frame trail follows each car to show relative speed visually. The live info panel shows current distance, each driver's speed, time delta, and who is leading at that instant.

---

## Possible Extensions

- Add DRS detection zones from brake/throttle patterns
- Support more than two drivers
- Export per-corner data to CSV for further analysis
- Interactive Plotly/Streamlit dashboard
- Sector-level breakdown aligned to official F1 sector markers

## Future works
- Create a model to mimic the driver decision and compare it with a driver.