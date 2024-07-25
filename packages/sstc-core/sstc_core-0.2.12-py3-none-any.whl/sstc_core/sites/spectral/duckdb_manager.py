import hashlib
import duckdb
import keyring
from datetime import datetime
from typing import List, Dict, Any
from sstc_core.sites.spectral import utils, sftp_tools
from sstc_core.sites.spectral.stations import PlatformData
from collections import defaultdict

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
        
    Example:
        ```python
        db_manager = DuckDBManager('example.db')

        # Define table schema
        schema = phenocam_table_schema()

        # Create table
        db_manager.create_table('phenocam', schema)

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
            db_manager.insert_record('phenocam', record)
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
            db_manager.insert_multiple_records('phenocam', records)
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
            print(f"Executing query: {query} with params: {params}")  # Debug statement
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

    def record_exists(self, table_name: str, record_id: str) -> bool:
        """
        Checks if a record exists in the specified table based on a unique record_id.

        Parameters:
            table_name (str): The name of the table to check.
            record_id (str): The unique record ID.

        Returns:
            bool: True if the record exists, False otherwise.
        """
        query = f"SELECT 1 FROM {table_name} WHERE record_id = ? LIMIT 1"
        result = self._execute_query(query, (record_id,))
        return len(result) > 0

    def insert_record(self, table_name: str, record_dict: Dict[str, Any]):
        """
        Inserts a single record into the specified table if it does not already exist.

        Parameters:
            table_name (str): The name of the table to insert the record into.
            record_dict (Dict[str, Any]): The dictionary containing the record data.

        Raises:
            RecordExistsError: If the record already exists in the table.
        """
        record_id = generate_unique_id(
            record_dict['creation_date'],
            record_dict['station_acronym'],
            record_dict['location_id'],
            record_dict['platform_id']
        )
        record_dict['record_id'] = record_id

        if self.record_exists(table_name, record_id):
            raise RecordExistsError("Record already exists, skipping insertion.")
        
        columns = ', '.join(record_dict.keys())
        placeholders = ', '.join(['?'] * len(record_dict))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self._execute_query(query, tuple(record_dict.values()))

    def insert_multiple_records(self, table_name: str, records: List[Dict[str, Any]]):
        """
        Inserts multiple records into the specified table if they do not already exist.

        Parameters:
            table_name (str): The name of the table to insert the records into.
            records (List[Dict[str, Any]]): The list of dictionaries containing the record data.

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
                record_id = generate_unique_id(
                    record['creation_date'],
                    record['station_acronym'],
                    record['location_id'],
                    record['platform_id']
                )
                record['record_id'] = record_id

                if not self.record_exists(table_name, record_id):
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
    
    def list_tables(self) -> List[str]:
        """
        Returns a list of all tables in the database.

        Returns:
            List[str]: A list of table names in the database.

        Raises:
            DatabaseError: If an error occurs during query execution.
        """
        query = "SHOW TABLES"
        result = self._execute_query(query)
        return [row[0] for row in result]

    def get_catalog_filepaths(self, table_name: str, year: int = None) -> Dict[str, str]:
        """
        Retrieves all catalog filepaths organized by creation_date.

        The returned dictionary uses the creation_date as the key and the catalog_filepath as the value.

        If a specific year is provided, only the data for that year will be returned.

        Parameters:
            table_name (str): The name of the table to fetch data from.
            year (int, optional): The specific year to filter the results. If None, data for all years is returned.

        Returns:
            Dict[str, str]: A dictionary mapping creation_date to catalog_filepath.
        """
        if year:
            query = f"SELECT creation_date, catalog_filepath FROM {table_name} WHERE year(creation_date) = ?"
            result = self._execute_query(query, (year,))
        else:
            query = f"SELECT creation_date, catalog_filepath FROM {table_name}"
            result = self._execute_query(query)

        catalog_filepaths = {row['creation_date']: row['catalog_filepath'] for row in result}
        return catalog_filepaths

    def get_source_filepaths(self, table_name: str, year: int = None) -> Dict[str, str]:
        """
        Retrieves all source filepaths organized by creation_date.

        The returned dictionary uses the creation_date as the key and the source_filepath as the value.

        If a specific year is provided, only the data for that year will be returned.

        Parameters:
            table_name (str): The name of the table to fetch data from.
            year (int, optional): The specific year to filter the results. If None, data for all years is returned.

        Returns:
            Dict[str, str]: A dictionary mapping creation_date to source_filepath.
        """
        if year:
            query = f"SELECT creation_date, source_filepath FROM {table_name} WHERE year(creation_date) = ?"
            result = self._execute_query(query, (year,))
        else:
            query = f"SELECT creation_date, source_filepath FROM {table_name}"
            result = self._execute_query(query)

        source_filepaths = {row['creation_date']: row['source_filepath'] for row in result}
        return source_filepaths
    
    def add_day_of_year_column(self, table_name: str):
        """
        Adds a new column named 'day_of_year' to the specified table and populates it.

        The 'day_of_year' column holds the integer value of the day of the year based on the 'creation_date' field.

        Parameters:
            table_name (str): The name of the table to modify.
        """
        try:
            # Add the new column 'day_of_year'
            self._execute_query(f"ALTER TABLE {table_name} ADD COLUMN day_of_year INTEGER;")
            
            # Fetch required fields to compute 'day_of_year'
            query = f"SELECT rowid, creation_date FROM {table_name}"
            records = self._execute_query(query)

            for row in records:
                rowid = row[0]
                creation_date = row[1]

                # Parse the creation_date to get the day of the year
                date_obj = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
                day_of_year = date_obj.timetuple().tm_yday

                # Update the row with the day_of_year value
                update_query = f"UPDATE {table_name} SET day_of_year = ? WHERE rowid = ?"
                self._execute_query(update_query, (day_of_year, rowid))
        except Exception as e:
            raise DatabaseError(f"An error occurred while adding or populating 'day_of_year': {e}")

    def filter_by_time_window(self, table_name: str, start_time: str = "10:00:00", end_time: str = "14:00:00") -> List[int]:
        """
        Filters records based on creation_date time being within the specified time window.

        Parameters:
            table_name (str): The name of the table to filter data from.
            start_time (str): The start of the time window in 'HH:MM:SS' format.
            end_time (str): The end of the time window in 'HH:MM:SS' format.

        Returns:
            List[int]: A list of rowids where the creation_date is within the time window.
        """
        query = f"SELECT rowid, creation_date FROM {table_name}"
        records = self._execute_query(query)

        start_time_obj = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time_obj = datetime.strptime(end_time, '%H:%M:%S').time()

        rowids_in_time_window = []
        for row in records:
            rowid = row[0]
            creation_date = row[1]
            creation_time = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S').time()

            if start_time_obj <= creation_time <= end_time_obj:
                rowids_in_time_window.append(rowid)

        return rowids_in_time_window
    
    def populate_L0_name(self, table_name: str):
        """
        Adds or updates a column named 'L0_name' in the specified table.

        The 'L0_name' is generated by concatenating the station_acronym, location_id,
        platform_id, day of the year, and creation date in the format 
        'station_acronym-location_id-platform_id_dayofyear_creationdate'.

        Parameters:
            table_name (str): The name of the table to modify.
        """
        try:
            # Check if 'L0_name' column exists, and add it if not
            existing_columns_query = f"PRAGMA table_info({table_name})"
            columns = self._execute_query(existing_columns_query)
            if 'L0_name' not in [col[1] for col in columns]:  # Checking if 'L0_name' is in the column names
                self._execute_query(f"ALTER TABLE {table_name} ADD COLUMN L0_name TEXT;")

            # Fetch required fields to compute 'L0_name'
            query = f"SELECT rowid, creation_date, station_acronym, location_id, platform_id, day_of_year FROM {table_name}"
            records = self._execute_query(query)

            for row in records:
                rowid = row[0]
                creation_date = row[1]
                station_acronym = row[2]
                location_id = row[3]
                platform_id = row[4]
                day_of_year = row[5]

                # Format the day_of_year with leading zeros
                day_of_year_str = f"{day_of_year:03d}"
                formatted_date = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d_%H%M%S')

                # Generate L0_name
                L0_name = f"{station_acronym}-{location_id}-{platform_id}_{day_of_year_str}_{formatted_date}"

                # Update the row with the L0_name
                update_query = f"UPDATE {table_name} SET L0_name = ? WHERE rowid = ?"
                self._execute_query(update_query, (L0_name, rowid))
        except Exception as e:
            raise DatabaseError(f"An error occurred while adding or populating 'L0_name': {e}")


    def check_is_L1(self, table_name: str):
        """
        Adds a new column named 'is_L1' to the specified table and sets it based on whether the creation_date
        falls within the 10:00 to 14:00 time window.

        Parameters:
            table_name (str): The name of the table to modify.
        """
        try:
            # Check if 'is_L1' column exists, and add it if not
            existing_columns_query = f"PRAGMA table_info({table_name})"
            columns = self._execute_query(existing_columns_query)
            if 'is_L1' not in [col[1] for col in columns]:  # Checking if 'is_L1' is in the column names
                self._execute_query(f"ALTER TABLE {table_name} ADD COLUMN is_L1 BOOLEAN;")

            # Get rowids within the time window
            rowids_in_time_window = self.filter_by_time_window(table_name)

            # Update 'is_L1' column based on the time window
            for rowid in rowids_in_time_window:
                self._execute_query(f"UPDATE {table_name} SET is_L1 = TRUE WHERE rowid = ?", (rowid,))

            # Set 'is_L1' to False for all other rows
            self._execute_query(f"UPDATE {table_name} SET is_L1 = FALSE WHERE is_L1 IS NULL")
        except Exception as e:
            raise DatabaseError(f"An error occurred while adding or populating 'is_L1': {e}")


    def get_catalog_filepaths_by_year_and_day(self, table_name: str, year: int = None, is_L1: bool = None) -> Dict[int, Dict[int, Dict[str, Dict[str, Any]]]]:
        """
        Retrieves all catalog filepaths organized by year, day_of_year, and L0_name.

        The returned dictionary uses the year as the first key, which maps to another dictionary.
        This nested dictionary uses the day_of_year as the second-level key, which then maps to another
        dictionary with L0_name as the third-level key, mapping to a dictionary containing the details.

        If a specific year or is_L1 filter is provided, only the data matching these filters will be returned.

        Parameters:
            table_name (str): The name of the table to fetch data from.
            year (int, optional): The specific year to filter the results. If None, data for all years is returned.
            is_L1 (bool, optional): The specific is_L1 value to filter the results. If None, data for all values is returned.

        Returns:
            Dict[int, Dict[int, Dict[str, Dict[str, Any]]]]: A nested dictionary with year as the top-level key,
                                                              day_of_year as the second-level key, L0_name as the third-level key,
                                                              and a dictionary containing day_of_year, L0_name, is_L1,
                                                              location_id, platform_id, station_acronym, and catalog_filepath as the values.
        """
        # Construct the base query
        query = f"""
        SELECT creation_date, day_of_year, L0_name, is_L1, location_id, platform_id, station_acronym, catalog_filepath
        FROM {table_name}
        """
        
        # Build conditions for filtering
        conditions = []
        params = []
        if year is not None:
            conditions.append("STRFTIME('%Y', CAST(creation_date AS TIMESTAMP)) = ?")
            params.append(str(year))  # Year should be a string for comparison
        if is_L1 is not None:
            conditions.append("is_L1 = ?")
            params.append(is_L1)

        # Combine conditions with 'AND'
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        result = self._execute_query(query, tuple(params))

        # Organize the results
        filepaths_by_year_and_day = defaultdict(lambda: defaultdict(dict))
        for row in result:
            creation_date = row[0]  # Accessing the creation_date
            day_of_year = row[1]  # Accessing the day_of_year
            L0_name = row[2]  # Accessing the L0_name
            is_L1_status = row[3]  # Accessing the is_L1 status
            location_id = row[4]  # Accessing the location_id
            platform_id = row[5]  # Accessing the platform_id
            station_acronym = row[6]  # Accessing the station_acronym
            catalog_filepath = row[7]  # Accessing the catalog_filepath
            
            date_obj = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
            year_key = date_obj.year

            # Assign values to the dictionary
            filepaths_by_year_and_day[year_key][day_of_year][L0_name] = {
                "day_of_year": day_of_year,
                "L0_name": L0_name,
                "is_L1": is_L1_status,
                "location_id": location_id,
                "platform_id": platform_id,
                "station_acronym": station_acronym,
                "catalog_filepath": catalog_filepath
            }

        return dict(filepaths_by_year_and_day)            

def generate_unique_id(creation_date: str, station_acronym: str, location_id: str, platform_id: str) -> str:
    """
    Generates a unique global identifier based on creation_date, station_acronym, location_id, and platform_id.

    Parameters:
        creation_date (str): The creation date of the record.
        station_acronym (str): The station acronym.
        location_id (str): The location ID.
        platform_id (str): The platform ID.

    Returns:
        str: A unique global identifier as a SHA-256 hash string.
    """
    # Concatenate the input values to form a unique string
    unique_string = f"{creation_date}_{station_acronym}_{location_id}_{platform_id}"
    
    # Generate the SHA-256 hash of the unique string
    unique_id = hashlib.sha256(unique_string.encode()).hexdigest()
    
    return unique_id


def get_phenocam_table_schema() -> str:
    """
    Returns the SQL schema definition for the Phenocam table.

    This function generates and returns the SQL schema definition as a string for the Phenocam table.
    The schema includes the following columns:
        ```markdown
        - record_id: TEXT (unique identifier)
        - year: INTEGER
        - creation_date: TEXT
        - station_acronym: TEXT
        - location_id: TEXT
        - platform_id: TEXT
        - platform_type: TEXT
        - catalog_filepath: TEXT
        - source_filepath: TEXT
        - is_selected: BOOL
        ```

    Returns:
        str: The SQL schema definition for the Phenocam table.
    """
    return """
    record_id TEXT PRIMARY KEY,
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



def _download_files_and_create_records_generator(acronym, location_id, platform_id, platform_type, local_dirpath: str, sftp, sftp_filepaths, split_subdir:str = 'data'):
    """
    Downloads files from an SFTP server and creates record dictionaries for insertion into the database.

    Parameters:
        acronym (str): The station acronym.
        location_id (str): The location ID.
        platform_id (str): The platform ID.
        platform_type (str): The platform type.
        local_dirpath (str): The local directory path to save downloaded files.
        sftp: The SFTP connection object.
        sftp_filepaths (list): List of file paths on the SFTP server to download.
        split_subdir (str): The subdirectory name to split the file path on. Defaults to 'data'.
        
    Yields:
        dict: A dictionary containing record information.
        
    Example:
       ```python
        # Defining variables
        system_name='abisko'
        acronym= 'ANS'
        platform_id= 'P_BTH_1'
        location_id= 'BTH_FOR'
        platform_type: 'PhenoCam'
        
        table_name= 'ANS__BTH_FOR__P_BTH_1'
        db_path = f'/home/aurora02/data/SITES/Spectral/data/catalog/{system_name}_catalog.db'
        local_dirpath = f'/home/aurora02/data/SITES/Spectral/data/catalog/{system_name}/locations/{location_id}/platforms/{platform_type}/{platform_id}'
       
        # Step 1: List files on the SFTP server
        sftp_filepaths = sftp_tools.list_files_sftp(
            hostname=hostname,
            port=port,
            username=username,
            password = password,
            sftp_directory=sftp_directory
        )
        
        # Step 2: Open sftp connection
        sftp, transport = sftp_tools.open_sftp_connection(
            hostname=hostname,
            port=port,
            username=username,
            password = password,
        )
        
        # Step 3: Connect to database
        db = DuckDBManager(db_path=db_path)
        schema = dbm.phenocam_table_schema()
        db.create_table(table_name, schema=schema)
        
        # Step 4: Download files and create records
        
        for record in download_files_and_create_records(
            acronym, 
            location_id, 
            platform_id, 
            platform_type, 
            local_dirpath, 
            sftp, 
            sftp_filepaths, 
            split_subdir='data'):
            
            try:
                db.insert_record(table_name, record)
            except RecordExistsError as e:
                print(e)
            except DatabaseError as e:
                print(e)
                
        sftp.close()
        transport.close()
       
        
       ```
    """
    for remote_filepath in sftp_filepaths:
        # Download the file from the SFTP server
        downloaded_filepath = sftp_tools.download_file(
            sftp,
            remote_filepath=remote_filepath,
            local_dirpath=local_dirpath,
            split_subdir=split_subdir)
        
        # Get creation date and formatted date
        creation_date = utils.get_image_dates(downloaded_filepath)
        formatted_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
        year = creation_date.year

        try:
            # Create the record dictionary
            record_dict = {
                'record_id': generate_unique_id(formatted_date, acronym, location_id, platform_id),
                'year': year,
                'creation_date': formatted_date,
                'catalog_filepath': downloaded_filepath,
                'source_filepath': remote_filepath,
                'station_acronym': acronym,
                'location_id': location_id,
                'platform_id': platform_id,
                'platform_type': platform_type
            }
            yield record_dict
        except Exception as e:
            print(f"Failed to move file: {e}")


def download_files_and_create_records(platform_dict: dict, db_filepath: str):
    """
    Downloads files from an SFTP server and creates records in the database.

    Parameters:
        platform_dict (dict): A dictionary containing platform information.
        catalog_dict (dict): A dictionary containing catalog information.
        db_filepath (str): The file path to the DuckDB database.
        
    Example:
        ```python
        platform_dict = {
            'system_name': 'abisko',
            'acronym': 'ANS',
            'location_id': 'BTH_FOR',
            'platform_id': 'P_BTH_1',
            'platform_type': 'PhenoCam'
        }
        
        catalog_dict = {
            'sftp_directory': '/abisko/data/PhenoCam/ANS/'
        }
        
        db_filepath = '/home/aurora02/data/SITES/Spectral/data/catalog/abisko_catalog.db'
        
        download_files_and_create_records(platform_dict, catalog_dict, db_filepath)
        ```
    Notes:
        Recommended to be use for first population of the database or
    """
    # SFTP variables
    hostname = keyring.get_password('sftp', 'hostname')
    port = int(keyring.get_password('sftp', 'port'))
    username = keyring.get_password('sftp', 'username')
    password = keyring.get_password('sftp', 'password')
    sftp_directory = f'/{platform_dict["system_name"]}/data/PhenoCam/{platform_dict["legacy_acronym"]}/'
    
    system_name = platform_dict.get('system_name')
    acronym = platform_dict.get('acronym')
    location_id = platform_dict.get('location_id')
    platform_id = platform_dict.get('platform_id')
    platform_type = platform_dict.get('platform_type')
        
    table_name = f'{acronym}__{location_id}__{platform_id}'
    local_dirpath = f'/home/aurora02/data/SITES/Spectral/data/catalog/{system_name}/locations/{location_id}/platforms/{platform_type}/{platform_id}'
    
    # Step 1: List files on the SFTP server
    sftp_filepaths = sftp_tools.list_files_sftp(
        hostname=hostname,
        port=port,
        username=username,
        password=password,
        sftp_directory=sftp_directory
    )
        
    # Step 2: Open SFTP connection
    sftp, transport = sftp_tools.open_sftp_connection(
        hostname=hostname,
        port=port,
        username=username,
        password=password,
    )
        
    # Step 3: Connect to the database
    db = DuckDBManager(db_path=db_filepath)
    schema = get_phenocam_table_schema()
    db.create_table(table_name, schema=schema)
        
    # Step 4: Download files and create records
    for record in _download_files_and_create_records_generator(
        acronym, 
        location_id, 
        platform_id, 
        platform_type, 
        local_dirpath, 
        sftp, 
        sftp_filepaths, 
        split_subdir='data'):
        
        try:
            db.insert_record(table_name, record)
        except RecordExistsError as e:
            print(e)
        except DatabaseError as e:
            print(e)
            
    sftp.close()
    transport.close()
    
    
def get_all_tables(db_path):
    """
    Retrieves all table names from the DuckDB database.

    Parameters:
        db_path (str): The path to the DuckDB database file.

    Returns:
        list: A list of table names present in the database.

    Raises:
        ValueError: If any error occurs during the process.
    """
    try:
        # Connect to DuckDB
        conn = duckdb.connect(database=db_path, read_only=True)

        # Retrieve all table names
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='main';"
        result = conn.execute(query).fetchall()

        # Extract table names from the result
        table_names = [row[0] for row in result]

        return table_names

    except Exception as e:
        raise ValueError(f"An error occurred while retrieving tables from DuckDB: {e}")
    finally:
        # Close the connection
        conn.close()