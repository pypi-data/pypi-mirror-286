import duckdb
from functools import wraps


def get_catalog_table_name(acronym, location_id, platform_id):
    """
    Get a table name based on station acronym, location, and platform abbreviations.

    Parameters:
        acronym (str): The abbreviation for the station.
        location_id (str): The abbreviation for the location.
        platform_id (str): The abbreviation for the platform.

    Returns:
        str: The generated table name.
    """
    return f"{acronym}__{location_id}__{platform_id}"


def table_name_decorator(func):
    """
    A decorator to generate a table name based on the instance's acronym, location ID,
    and platform ID attributes, and pass it as an argument to the decorated function.

    This decorator assumes that the instance passed to the decorated function has
    the attributes 'acronym', 'location_id', and 'platform_id'.

    Parameters:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function with the table name passed as an argument.

    Note: 
        use in sites.spectral.stations.StationData()
        
    Example:
    --------
    @table_name_decorator
    def get_table_name(self, table_name):
        return(table_name)
    """

    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        table_name = get_catalog_table_name(instance.acronym, instance.location_id, instance.platform_id)
        return func(instance, table_name, *args, **kwargs)
    
    return wrapper

        
def filter_by_year_from_grouped_filepaths_duckdb(db_path, table_name, year):
    """
    Filters and retrieves entries from a DuckDB database for a specified year.

    This function connects to a DuckDB database, executes a query to retrieve entries
    from the specified table that match the given year, and transforms the result into
    a dictionary where the keys are creation dates and the values are lists of file paths.

    Parameters:
        db_path (str): The path to the DuckDB database file.
        table_name (str): The name of the table to query.
        year (int): The year to filter entries by.

    Returns:
        dict: A dictionary where keys are creation dates (as strings) and values are lists
          of file paths that correspond to those dates.

    Example:
        ```python
        db_path = '/path/to/database.duckdb'
        table_name = 'image_table'
        year = 2023
        filter_by_year_from_duckdb(db_path, table_name, year)
        {
            '2023-01-01 12:00:00': ['/path/to/image1.jpg'],
            '2023-02-01 13:00:00': ['/path/to/image2.jpg']
        }
        ```
    """
    # Connect to DuckDB
    conn = duckdb.connect(database=db_path, read_only=True)
    
    # Execute the query to retrieve entries for the specified year
    query = f"""
    SELECT creation_date, filepath 
    FROM {table_name}
    WHERE year = ?
    """
    result = conn.execute(query, [year]).fetchall()
    
    # Close the connection
    conn.close()
    
    # Transform the result into a dictionary
    filtered_dict = {}
    for row in result:
        date, path = row
        if date not in filtered_dict:
            filtered_dict[date] = []
        filtered_dict[date].append(path)
    
    return filtered_dict 


def get_all_filepaths_in_duckdb(db_path, table_name):
    """
    Retrieves all stored file paths from a specified table in a DuckDB database.

    This function connects to a DuckDB database, retrieves all file paths stored in the specified
    table, and returns them as a list.

    Parameters:
        db_path (str): The path to the DuckDB database file.
        table_name (str): The name of the table to retrieve file paths from.

    Returns:
        list: A list of file paths stored in the specified table.

    Example:
        ```python    
        db_path = '/path/to/database.duckdb'
        table_name = 'backup_files'
        get_all_backup_filepaths_in_duckdb(db_path, table_name)
        ['/path/to/backup/file1.jpg', '/path/to/backup/file2.jpg']
        ```
    """
    # Connect to the DuckDB database and retrieve stored file paths
    conn = duckdb.connect(db_path)
    query = f'SELECT filepath FROM {table_name}'
    result = conn.execute(query).fetchall()
    conn.close()

    # Extract file paths from the result
    stored_filepaths = [row[0] for row in result]
    return stored_filepaths