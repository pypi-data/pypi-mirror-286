import duckdb
from typing import List, Dict, Any


phenocam_table_squema = """
    year INTEGER,
    creation_date TEXT,
    station_acronym TEXT,
    location_id TEXT,
    platform_id TEXT,
    platform_type TEXT,            
    catalog_filepath TEXT,
    source_filepath TEXT, 
    is_selected BOOL    
    """




class DatabaseError(Exception):
    """Base class for other exceptions"""
    pass

class RecordExistsError(DatabaseError):
    """Raised when the record already exists in the database"""
    pass

class RecordNotFoundError(DatabaseError):
    """Raised when the record is not found in the database"""
    pass

class DuckDBManager:
    """
    A class to manage DuckDB database operations, including creating tables, inserting records,
    updating records, deleting records, and fetching records based on specific conditions.

    Attributes:
        db_path (str): The path to the DuckDB database file.
        
    Use:
    ```python
    db_manager = DuckDBManager('example.db')

    # Define table schema
    schema = '''
        year INTEGER,
        creation_date TEXT,
        station_acronym TEXT,
        location_id TEXT,
        platform_id TEXT,
        platform_type TEXT,            
        catalog_filepath TEXT,
        source_filepath TEXT, 
        is_selected BOOL
    '''

    # Create table
    db_manager.create_table('phenocam', schema)

    # Unique condition for record existence check
    unique_condition = "year = ? AND creation_date = ? AND station_acronym = ? AND location_id = ? AND platform_id = ?"

    # Insert single record
    try:
        record = {
            'year': 2024,
            'creation_date': '2024-07-23',
            'station_acronym': 'STA01',
            'location_id': 'LOC01',
            'platform_id': 'PLT01',
            'platform_type': 'type1',
            'catalog_filepath': '/path/to/catalog',
            'source_filepath': '/path/to/source',
            'is_selected': True
        }
        db_manager.insert_record('phenocam', record, unique_condition)
    except RecordExistsError as e:
        print(e)
    except DatabaseError as e:
        print(e)

    # Insert multiple records
    try:
        records = [
            {
                'year': 2024,
                'creation_date': '2024-07-23',
                'station_acronym': 'STA01',
                'location_id': 'LOC01',
                'platform_id': 'PLT01',
                'platform_type': 'type1',
                'catalog_filepath': '/path/to/catalog',
                'source_filepath': '/path/to/source',
                'is_selected': True
            },
            {
                'year': 2024,
                'creation_date': '2024-07-24',
                'station_acronym': 'STA02',
                'location_id': 'LOC02',
                'platform_id': 'PLT02',
                'platform_type': 'type2',
                'catalog_filepath': '/path/to/catalog2',
                'source_filepath': '/path/to/source2',
                'is_selected': False
            }
        ]
        db_manager.insert_multiple_records('phenocam', records, unique_condition)
    except RecordExistsError as e:
        print(e)
    except DatabaseError as e:
        print(e)

    # Update record
    try:
        update_values = {
            'is_selected': False
        }
        condition = "station_acronym = 'STA01'"
        db_manager.update_record('phenocam', update_values, condition)
    except DatabaseError as e:
        print(e)

    # Delete record
    try:
        condition = "station_acronym = 'STA02'"
        db_manager.delete_record('phenocam', condition)
    except DatabaseError as e:
        print(e)

    # Fetch records
    try:
        records = db_manager.fetch_records('phenocam')
        for record in records:
            print(record)
    except DatabaseError as e:
        print(e)

    # Fetch by year
    try:
        records = db_manager.fetch_by_year('phenocam', 2024)
        for record in records:
            print(record)
    except DatabaseError as e:
        print(e)

    # Fetch by is_selected
    try:
        records = db_manager.fetch_by_is_selected('phenocam', True)
        for record in records:
            print(record)
    except DatabaseError as e:
        print(e)

    # Fetch by year and is_selected
    try:
        records = db_manager.fetch_by_year_and_is_selected('phenocam', 2024, True)
        for record in records:
            print(record)
    except DatabaseError as e:
        print(e)
    ```
        
    """
    
    
    def __init__(self, db_path: str):
        """
        Initializes the DuckDBManager with the specified database path.

        Parameters:
            db_path (str): The path to the DuckDB database file.
        """
        self.db_path = db_path

    def _execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Executes a given SQL query with optional parameters and returns the result.

        Parameters:
            query (str): The SQL query to execute.
            params (tuple): The parameters to use with the SQL query.

        Returns:
            List[Dict[str, Any]]: The result of the query execution.
        
        Raises:
            DatabaseError: If an error occurs during query execution.
        """
        try:
            conn = duckdb.connect(database=self.db_path, read_only=False)
            result = conn.execute(query, params).fetchall()
            return result
        except Exception as e:
            raise DatabaseError(f"An error occurred: {e}")
        finally:
            conn.close()

    def create_table(self, table_name: str, schema: str):
        """
        Creates a table with the specified schema if it does not already exist.

        Parameters:
            table_name (str): The name of the table to create.
            schema (str): The schema of the table in SQL format.
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});"
        self._execute_query(query)

    def record_exists(self, table_name: str, unique_condition: str, params: tuple) -> bool:
        """
        Checks if a record exists in the specified table based on a unique condition.

        Parameters:
            table_name (str): The name of the table to check.
            unique_condition (str): The SQL condition to check for record uniqueness.
            params (tuple): The parameters to use with the SQL condition.

        Returns:
            bool: True if the record exists, False otherwise.
        """
        query = f"SELECT 1 FROM {table_name} WHERE {unique_condition} LIMIT 1"
        result = self._execute_query(query, params)
        return len(result) > 0

    def insert_record(self, table_name: str, record_dict: Dict[str, Any], unique_condition: str):
        """
        Inserts a single record into the specified table if it does not already exist.

        Parameters:
            table_name (str): The name of the table to insert the record into.
            record_dict (Dict[str, Any]): The dictionary containing the record data.
            unique_condition (str): The SQL condition to check for record uniqueness.

        Raises:
            RecordExistsError: If the record already exists in the table.
        """
        unique_params = (
            record_dict['year'],
            record_dict['creation_date'],
            record_dict['station_acronym'],
            record_dict['location_id'],
            record_dict['platform_id']
        )
        if self.record_exists(table_name, unique_condition, unique_params):
            raise RecordExistsError("Record already exists, skipping insertion.")
        
        columns = ', '.join(record_dict.keys())
        placeholders = ', '.join(['?'] * len(record_dict))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self._execute_query(query, tuple(record_dict.values()))

    def insert_multiple_records(self, table_name: str, records: List[Dict[str, Any]], unique_condition: str):
        """
        Inserts multiple records into the specified table if they do not already exist.

        Parameters:
            table_name (str): The name of the table to insert the records into.
            records (List[Dict[str, Any]]): The list of dictionaries containing the record data.
            unique_condition (str): The SQL condition to check for record uniqueness.

        Raises:
            RecordExistsError: If any of the records already exist in the table.
            DatabaseError: If an error occurs during query execution.
        """
        if not records:
            return
        
        columns = ', '.join(records[0].keys())
        placeholders = ', '.join(['?'] * len(records[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        try:
            conn = duckdb.connect(database=self.db_path, read_only=False)
            for record in records:
                unique_params = (
                    record['year'],
                    record['creation_date'],
                    record['station_acronym'],
                    record['location_id'],
                    record['platform_id']
                )
                if not self.record_exists(table_name, unique_condition, unique_params):
                    conn.execute(query, tuple(record.values()))
                else:
                    raise RecordExistsError("Record already exists, skipping insertion.")
        except Exception as e:
            raise DatabaseError(f"An error occurred: {e}")
        finally:
            conn.close()

    def update_record(self, table_name: str, update_values: Dict[str, Any], condition: str):
        """
        Updates records in the specified table based on a condition.

        Parameters:
            table_name (str): The name of the table to update.
            update_values (Dict[str, Any]): The dictionary containing the update data.
            condition (str): The SQL condition to identify which records to update.

        Raises:
            DatabaseError: If an error occurs during query execution.
        """
        set_clause = ', '.join([f"{k} = ?" for k in update_values.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self._execute_query(query, tuple(update_values.values()))

    def delete_record(self, table_name: str, condition: str):
        """
        Deletes records from the specified table based on a condition.

        Parameters:
            table_name (str): The name of the table to delete records from.
            condition (str): The SQL condition to identify which records to delete.

        Raises:
            DatabaseError: If an error occurs during query execution.
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self._execute_query(query)

    def fetch_records(self, table_name: str, condition: str = "1=1") -> List[Dict[str, Any]]:
        """
        Fetches records from the specified table based on a condition.

        Parameters:
            table_name (str): The name of the table to fetch records from.
            condition (str): The SQL condition to filter records.

        Returns:
            List[Dict[str, Any]]: The list of fetched records.

        Raises:
            DatabaseError: If an error occurs during query execution.
        """
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        return self._execute_query(query)

    def fetch_by_year(self, table_name: str, year: int) -> List[Dict[str, Any]]:
        """
        Fetches records from the specified table based on the year.

        Parameters:
            table_name (str): The name of the table to fetch records from.
            year (int): The year to filter records by.

        Returns:
            List[Dict[str, Any]]: The list of fetched records.

        Raises:
            DatabaseError: If an error occurs during query execution.
        """
        query = f"SELECT * FROM {table_name} WHERE year = ?"
        return self._execute_query(query, (year,))

    def fetch_by_is_selected(self, table_name: str, is_selected: bool) -> List[Dict[str, Any]]:
        """
        Fetches records from the specified table based on the is_selected field.

        Parameters:
            table_name (str): The name of the table to fetch records from.
            is_selected (bool): The is_selected value to filter records by.

        Returns:
            List[Dict[str, Any]]: The list of fetched records.

        Raises:
            DatabaseError: If an error occurs during query execution.
        """
        query = f"SELECT * FROM {table_name} WHERE is_selected = ?"
        return self._execute_query(query, (is_selected,))

    def fetch_by_year_and_is_selected(self, table_name: str, year: int, is_selected: bool) -> List[Dict[str, Any]]:
        """
        Fetches records from the specified table based on both the year and is_selected fields.

        Parameters:
            table_name (str): The name of the table to fetch records from.
            year (int): The year to filter records by.
            is_selected (bool): The is_selected value to filter records by.

        Returns:
            List[Dict[str, Any]]: The list of fetched records.

        Raises:
            DatabaseError: If an error occurs during query execution.
        """
        query = f"SELECT * FROM {table_name} WHERE year = ? AND is_selected = ?"
        return self._execute_query(query, (year, is_selected))

