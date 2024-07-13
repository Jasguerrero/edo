import pandas as pd

from storage.storage_client import StorageClient


class CSVStorageClient(StorageClient):
    def save(self, data: pd.DataFrame, table: str, if_exists: str = None):
        if not self.is_dry_run():
            filename = self._append_csv_to_name(table)
            data.to_csv(f"/app/data/{filename}")
            self._logging.info(f"File {filename} saved.")

    def get_from_table(self, table: str):
        filename = self._append_csv_to_name(table)
        return pd.read_csv(f"/app/data/{filename}")

    def _append_csv_to_name(self, table):
        return f"{table}.csv"
