import pandas as pd

from city_state.city_state_handler import CityStateMap
from storage.storage_client import StorageClient
from storage.csv_storage_client import CSVStorageClient

class EDODirectory:
    CSV_FIELDS = ["EIN", "NAME", "ICO", "STREET", "CITY", "STATE", "ZIP", "NTEE_CD"]
    NTEE_CODES = [
        'S30',  # Economic Development
        'S31',  # Urban & Community Economic Development
        'S32'  # Rural Economic Development
        # Add other relevant codes as necessary
    ]

    def __init__(self, logging, storage_client: StorageClient):
        self._storage_client = storage_client
        self._city_map = CityStateMap(CSVStorageClient(logging))
        self._logging = logging

    def _download_csv_from_irs(self, state, filename):
        url = f"https://www.irs.gov/pub/irs-soi/eo_{state}.csv"
        self._logging.info(url)
        df = pd.read_csv(url)
        df = df[self.CSV_FIELDS]
        df = df[df["NTEE_CD"].isin(self.NTEE_CODES)]
        self._storage_client.save(df, filename)

    def _read_df(self, filename, city):
        df = self._storage_client.get_dataframe(filename)
        df = df[df["CITY"] == city.upper()]
        return df

    def get_city_edos(self, city):
        state = self._city_map.get_state(city)
        filename = f"{state}_edo"

        df = self._storage_client.get_dataframe(filename)
        if df.empty:
            self._download_csv_from_irs(state, filename)
        return self._read_df(filename, city)
