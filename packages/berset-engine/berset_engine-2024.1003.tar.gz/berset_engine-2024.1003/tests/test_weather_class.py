import unittest
from berset_engine.better.weather import Weather
from geopy import Nominatim
from berset_engine.better.weather import process_downloaded_weather_noaa
import pandas as pd


geolocator = Nominatim(user_agent="berset")
geo_coder = geolocator.geocode(
    "Brussels,Belgium"
)
geo_coord = [geo_coder.latitude,geo_coder.longitude]
weatherInstance = Weather(geo_coord)

class Test_weather_class(unittest.TestCase):
    def test_find_closest_weather_station(self):

        self.assertEqual(
            weatherInstance.closest_weather_station_ID,
            '064470-99999',
            "not equals"
        )

    def test_download_weather_NOAA(self):
        df = process_downloaded_weather_noaa('064470-99999', 2021, 2022)
        self.assertFalse(df.empty)        

if __name__=='__main__':
    unittest.main()

