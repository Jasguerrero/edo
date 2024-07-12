import psycopg2
from psycopg2 import Error

class EDO:
    def __init__(self, name, mobile_number="", email="", address="", _id="", created_at=None) -> None:
        self.name = name
        self.mobile_number = mobile_number
        self.email = email
        self.address = address
        self._id = _id
        self.created_at = created_at

class Query:
    def __init__(self, ids=[], names=[], mobile_numbers=[], emails=[], addresses=[]):
        self.filter_values = {}
        if ids:
            self.filter_values['id'] = ids
        if names:
            self.filter_values['name'] = names
        if mobile_numbers:
            self.filter_values['mobileNumber'] = mobile_numbers
        if emails:
            self.filter_values['email'] = emails
        if addresses:
            self.filter_values['physicalAddress'] = addresses

        conditions = []
        params = []

        for column, values in self.filter_values.items():
            placeholders = ','.join(['%s'] * len(values))
            conditions.append(f"{column} IN ({placeholders})")
            params.extend(values)

        where_clause = " AND ".join(conditions)
        self.select = "SELECT * FROM edos"
        self.message = "empty query, returning all records"
        if where_clause:
            self.select = f"{self.select} WHERE {where_clause}"
            self.message = ""
        self.params = tuple(params)

class DatabaseLayer:
    def get_edos(self, ids=[], names=[], mobile_numbers=[], emails=[], addresses=[]):
        query = Query(ids, names, mobile_numbers, emails, addresses)
        connection = self._db_connection()
        cursor = connection.cursor()
        cursor.execute(query.select, query.params)
        result = []
        if cursor.pgresult_ptr is not None:
            rows = cursor.fetchall()
            result = [
                EDO(
                    _id = row[0],
                    name = row[1],
                    mobile_number = row[2],
                    email = row[3],
                    address = row[4],
                    created_at = row[5]
                )
                for row in rows
            ]
        cursor.close()
        connection.close()
        return result, query.message
    
    def post_edo(self, edo: EDO):
        insert_query = """
        INSERT INTO edos (name, mobileNumber, email, physicalAddress) 
        VALUES (%s, %s, %s, %s);
        """
        try:
            connection = self._db_connection()
            cursor = connection.cursor()
            cursor.execute(insert_query, (edo.name, edo.mobile_number, edo.email, edo.address))
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as error:
            return str(error)
        
    def delete_edos(self, ids=[], names=[], mobile_numbers=[], emails=[], addresses=[]):
        edos, _ = self.get_edos(ids, names, mobile_numbers, emails, addresses)
        if not edos:
            return 0, None
        try:
            connection = self._db_connection()
            cursor = connection.cursor()
            postgres_delete_query = "DELETE FROM edos WHERE id IN %s"
            cursor.execute(postgres_delete_query, (tuple([edo._id for edo in edos]),))
            connection.commit()
            cursor.close()
            connection.close()
            return cursor.rowcount, None
        except (Exception, Error) as error:
            return 0, error
    
    def _db_connection(self):
        try:
            return psycopg2.connect(
                dbname='edo_db',
                user='admin',
                password='password',
                host='db',
                port='5432'
            )
        except (Exception, Error) as error:
            print(f"Error connecting to db: {error.__str__}")
