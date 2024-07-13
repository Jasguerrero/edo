import geonamescache
import pandas as pd
from geopy.geocoders import Nominatim

from storage.csv_storage_client import CSVStorageClient


class CityStateMapGenerator:
    geolocator = Nominatim(user_agent="city_state_map_generator")
    DEFAULT_NAME = "city_state_map"

    def __init__(self, storage_client):
        self._storage_client = storage_client

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
                us_city_state_map[city_name] = state_abv.lower()  # STATE_ABV_TO_NAME[state_abv]
        us_city_state_map["New York"] = "ny"
        return us_city_state_map

    def generate(self, name=None):
        name = self.DEFAULT_NAME if not name else name
        cities = self._get_cities()
        city_state_map = self._get_us_cities_state_map(cities)
        df_city_state_map = {"city": list(city_state_map.keys()), "state": list(city_state_map.values())}
        df = pd.DataFrame.from_dict(df_city_state_map)
        self._storage_client.save(df, name)


# Uncomment to run this as a script.

if __name__ == '__main__':
    csv_storage = CSVStorageClient()
    csm_generator = CityStateMapGenerator(csv_storage)
    csm_generator.generate()
