class CityStateMap:
    DEFAULT_NAME = "city_state_map"
    CITY_STATE_MAP = None

    def __init__(self, storage_client):
        self._storage_client = storage_client
        # current list 3000 cities. It's safe to keep it in memory.
        # we'll load it in here, but you can implement your own query if needed.
        if not self.CITY_STATE_MAP:
            self.CITY_STATE_MAP = self._load_all_city_states()

    def _load_all_city_states(self):
        city_state_map = {}
        df = self._storage_client.get_from_table(self.DEFAULT_NAME)
        for row in df.itertuples():
            city_state_map[row.city] = row.state
        return city_state_map

    def get_state(self, city):
        return self.CITY_STATE_MAP.get(city)
