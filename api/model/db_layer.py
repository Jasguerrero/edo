import psycopg2
from psycopg2 import Error

from logger import Logger

class EDO:
    def __init__(
            self, name, mobile_number="", email="", address="", 
            _id="", contact="", city="", state="", zip_code="",
            website="", created_at=None
        ) -> None:
        self.name = name
        self.mobile_number = mobile_number
        self.email = email
        self.address = address
        self._id = _id
        self.contact = contact
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.website = website
        self.created_at = created_at

class Query:
    def __init__(
            self, ids=[], names=[], mobile_numbers=[], emails=[], addresses=[],
            contacts=[], cities=[], states=[], zip_codes=[], websites=[]
        ):
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
        if contacts:
            self.filter_values['contact'] = contacts
        if cities:
            self.filter_values['city'] = cities
        if states:
            self.filter_values['state'] = states
        if zip_codes:
            self.filter_values['zipCode'] = zip_codes
        if websites:
            self.filter_values['website'] = websites

        conditions = []
        params = []

        for column, values in self.filter_values.items():
            placeholders = ','.join(['%s'] * len(values))
            conditions.append(f"{column} IN ({placeholders})")
            params.extend(values)

        where_clause = " OR ".join(conditions)
        self.select = "SELECT * FROM edos"
        self.message = "empty query, returning all records"
        if where_clause:
            self.select = f"{self.select} WHERE {where_clause}"
            self.message = ""
        self.params = tuple(params)

class DatabaseLayer:
    def __init__(self, logger: Logger):
        self._logger = logger
    
    def get_edos(
            self, ids=[], names=[], mobile_numbers=[], emails=[], addresses=[],
            contacts=[], cities=[], states=[], zip_codes=[], websites=[]
        ):
        query = Query(
            ids, names, mobile_numbers, emails, addresses, contacts, cities,
            states, zip_codes, websites
        )
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
                    contact = row[4],
                    address = row[5],
                    city = row[6],
                    state = row[7],
                    zip_code = row[8],
                    website = row[9],
                    created_at = row[10]
                )
                for row in rows
            ]
        cursor.close()
        connection.close()
        return result, query.message
    
    def post_edo(self, edo: EDO):
        insert_query = """
        INSERT INTO edos 
        (name, mobileNumber, email, contact, physicalAddress, city, state, zipCode, website) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            connection = self._db_connection()
            cursor = connection.cursor()
            cursor.execute(
                insert_query, 
                (
                    edo.name, edo.mobile_number, 
                    edo.email, edo.contact, edo.address,
                    edo.city, edo.state, edo.zip_code, edo.website
                )
            )
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as error:
            return str(error)
        
    def delete_edos(
            self, ids=[], names=[], mobile_numbers=[], 
            emails=[], addresses=[], contacts=[], cities=[], states=[],
            zip_codes=[], websites=[]
        ):
        edos, _ = self.get_edos(
            ids=ids, names=names, mobile_numbers=mobile_numbers, emails=emails, 
            addresses=addresses, contacts=contacts, cities=cities, states=states,
            zip_codes=zip_codes, websites=websites
        )
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
            connection = psycopg2.connect(
                dbname='edo_db',
                user='admin',
                password='password',
                host='db',
                port='5432'
            )
            self._logger.info('Connected to db')
            return connection
        except (Exception, Error) as error:
            self._logger.info(f"Error connecting to db: {error}")
