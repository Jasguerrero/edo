import time
import pandas as pd
import redis
import pickle

from typing import Union
from storage.storage_client import StorageClient

class CacheClient(StorageClient):
    def save(self, data: Union[str, pd.DataFrame], table: str, if_exists: str = None):
        ttl = 3600 * 5 # persist cache for 5 hours 
        connection = self._connection()
        if type(data) is not str: # Handle dataframe store
            data = pickle.dumps(data)
        connection.set(table, data, ex=ttl)
        connection.close()

    def get_from_table(self, table: str):
        connection = self._connection()
        val = connection.get(table)
        connection.close()
        return val
    
    def get_dataframe(self, key: str) -> pd.DataFrame:
        connection = self._connection()
        val = connection.get(key)
        if not val:
            self._logging.info(f"DataFrame not found key={key}")
            val = pd.DataFrame()
        else:
            val = pickle.loads(val)
        connection.close()
        return val

    def _connection(self, host='cache', port=6379, max_retries=5, retry_delay=10):
        attempt = 0
        while attempt < max_retries:
            try:
                r = redis.Redis(host=host, port=port, db=0)
                r.ping()  # Check if the connection is successful
                self._logging.info(f"Connected to Redis at {host}:{port}")
                return r
            except ConnectionError as e:
                attempt += 1
                self._logging.info(f"Attempt {attempt}: Connection to Redis failed - {e}")
                time.sleep(retry_delay)
        raise ConnectionError(f"Failed to connect to Redis after {max_retries} attempts")
