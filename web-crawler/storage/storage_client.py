from abc import ABC, abstractmethod
import pandas as pd

class StorageClient(ABC):

    def __init__(self, logging, dry_run=False):
        self._dry_run = dry_run
        self._logging = logging

    @abstractmethod
    def save(self, data, table: str, if_exists: str = None):
        pass

    @abstractmethod
    def get_from_table(self, table: str) -> pd.DataFrame:
        pass

    def is_dry_run(self) -> bool:
        return self._dry_run
    
    def get_dataframe(self, name: str) -> pd.DataFrame:
        pass
