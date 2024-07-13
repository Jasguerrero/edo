import geonamescache
import pandas as pd
from geopy.geocoders import Nominatim

from storage.csv_storage_client import CSVStorageClient


class CityStateMapGenerator:
    geolocator = Nominatim(user_agent="city_state_map_generator")

    def __init__(self, storage_client, city_state_file_name):
        self._storage_client = storage_client
        self._city_state_file_name = city_state_file_name

    def _get_cities(self):
        gc = geonamescache.GeonamesCache()
        c = gc.get_cities()
        return c

    def _get_us_cities_state_map(self, cities):
        us_city_state_map = {}
        for _, properties in cities.items():
            if properties["countrycode"] == "US":
                city_name = properties['name']
                state_abv = properties['admin1code']  # for the US, the state is the administrator 1.
                us_city_state_map[city_name] = state_abv.lower()
        us_city_state_map["New York"] = "ny" # handle "New York" the same as "New York City"
        return us_city_state_map

    def generate(self):
        cities = self._get_cities()
        city_state_map = self._get_us_cities_state_map(cities)
        df_city_state_map = {"city": list(city_state_map.keys()), "state": list(city_state_map.values())}
        df = pd.DataFrame.from_dict(df_city_state_map)
        self._storage_client.save(df, self._city_state_file_name)
