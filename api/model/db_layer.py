import psycopg2
from psycopg2 import Error

class DatabaseLayer:
    def get_edos(self):
        connection = self._db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM edos")
        cursor.close()
        connection.close()
        if cursor.pgresult_ptr is not None:
            rows = cursor.fetchall()
        else:
            return []
        return [
            {'id': row[0], 'title': row[1], 'author': row[2]}
            for row in rows
        ]
    
    def _db_connection(self):
        try:
            return psycopg2.connect(
                dbname='edo_db',
                user='user',
                password='password',
                host='db',
                port='5432'
            )
        except (Exception, Error) as error:
            print(f"Error connecting to db: {error.__str__}")
