import os
from pathlib import Path


noaa_weather_station_list_file = os.path.abspath(
    os.path.join(
        Path(__file__).resolve(strict=True).parent,
        "noaa_weather_station_list.csv"
    )
)