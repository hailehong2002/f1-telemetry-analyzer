
import os
import fastf1
from requests import session

def setup_fastf1_cache(cache_dir: str):
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)
    
def load_session(year: int, grand_prix: str, session_type: str):
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()
    return session

def get_fastest_lap_telemetry(session, drivers):
    telemetry_data = {}
    lapdata = {}
    for driver in drivers:
        lap = session.laps.pick_driver(driver).pick_fastest()
        tel = lap.get_telemetry().add_distance()
        telemetry_data[driver] = tel
        lapdata[driver] = lap
        print(f"{driver} fastest lap: {lap['LapTime']}")
    return telemetry_data, lapdata

