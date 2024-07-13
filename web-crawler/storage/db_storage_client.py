import time
import pandas as pd
import psycopg2

from storage.storage_client import StorageClient

class DBStorageClient(StorageClient):
    def save(self, data: pd.DataFrame, table: str, if_exists: str = None):
        connection = self._db_connection()
        cursor = connection.cursor()
        tuples = data[[
            "edo_name", "phone", "email", "contact",
            "street", "city", "state", "zip", "Website URL"
        ]].apply(tuple, axis=1).tolist()
        sql = f"""
            INSERT INTO {table} 
            (name, mobileNumber, email, contact, physicalAddress, city, state, zipCode, website) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        cursor.executemany(sql, tuples)
        connection.commit()
        cursor.close()
        connection.close()

    def get_from_table(self, table: str):
        pass

    def _db_connection(self):
        max_attempts = 10
        attempt = 0
        while attempt < max_attempts:
            try:
                connection = psycopg2.connect(
                    dbname='edo_db',
                    user='admin',
                    password='password',
                    host='db',
                    port='5432'
                )
                self._logging.info("Connected to PostgreSQL!")
                return connection
            except (Exception, psycopg2.Error) as error:
                self._logging.info(f"Error connecting to db: {error.__str__}")
                attempt += 1
                time.sleep(10)
