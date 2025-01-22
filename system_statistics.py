import psutil # type: ignore
import os

def battery_percentage() -> int | None:
    battery = psutil.sensors_battery()
    
    if battery is None:
        return None
    
    return battery.percent

def cpu_usage() -> float | None:
    return psutil.cpu_percent()