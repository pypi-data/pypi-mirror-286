import paramiko
import os
import stat
from sstc_core.sites.spectral.utils import extract_two_dirs_and_filename


def open_sftp_connection(hostname, port, username, password):
    """
    Opens an SFTP connection to the specified server.

    This function establishes an SFTP connection using the provided server details and returns the
    SFTP client and transport objects. It ensures that the connection is properly established
    before returning the objects.

    Parameters:
        hostname (str): The hostname or IP address of the SFTP server.
        port (int): The port number of the SFTP server.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        tuple: A tuple containing the SFTP client and transport objects.

    Raises:
        Exception: If an error occurs while establishing the SFTP connection.

    Example:
        ```python
        hostname = 'sftp.example.com'
        port = 22
        username = 'your_username'
        password = 'your_password'
        sftp, transport = open_sftp_connection(hostname, port, username, password)
        # Use the sftp client for file operations
        sftp.close()
        transport.close()
        ```
    """
    try:
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp, transport
    except Exception as e:
        raise Exception(f"An error occurred while establishing SFTP connection: {e}")


def list_files_sftp(hostname, port, username, password, sftp_directory, extensions=['.jpg', '.jpeg']):
    """
    Lists files from an SFTP server recursively with specified extensions.

    This function connects to an SFTP server using the provided connection details,
    recursively lists all files starting from the specified directory, and filters the files
    based on the provided extensions.

    Parameters:
        hostname (str): The hostname or IP address of the SFTP server.
        port (int): The port number of the SFTP server.
        username (str): The username for authentication.
        password (str): The password for authentication.
        sftp_directory (str): The directory on the SFTP server to start listing files from.
        extensions (list): A list of file extensions to filter by. Defaults to ['.jpg', '.jpeg'].

    Returns:
        list: A list of file paths from the SFTP server that match the specified extensions.

    Raises:
        Exception: If an error occurs while connecting to the SFTP server or retrieving files.

    Example:
        ```python
        hostname = 'sftp.example.com'
        port = 22
        username = 'your_username'
        password = 'your_password'
        sftp_directory = '/path/to/sftp/directory'
        list_files_sftp(hostname, port, username, password, sftp_directory)
        ['/path/to/sftp/directory/image1.jpg', '/path/to/sftp/directory/subdir/image2.jpeg']
        ```
    """
    try:
        # Open SFTP connection
        sftp, transport = open_sftp_connection(hostname, port, username, password)

        # Function to recursively list files in a directory
        def recursive_list(sftp, directory):
            file_list = []
            for entry in sftp.listdir_attr(directory):
                mode = entry.st_mode
                filename = entry.filename
                filepath = os.path.join(directory, filename)

                if stat.S_ISDIR(mode):  # Directory
                    file_list.extend(recursive_list(sftp, filepath))
                else:  # File
                    if any(filename.lower().endswith(ext) for ext in extensions):
                        file_list.append(filepath)
            return file_list

        # Get all files recursively starting from the specified directory
        all_files = recursive_list(sftp, sftp_directory)

        # Close the SFTP connection
        sftp.close()
        transport.close()
        
        return all_files

    except Exception as e:
        raise Exception(f"An error occurred while listing files from the SFTP server: {e}")


def download_file(sftp, remote_filepath, local_dirpath, split_subdir='data'):
    """
    Downloads a file from the SFTP server and ensures that the download is complete by verifying the file size.

    This function downloads a file from the specified remote path on the SFTP server to the specified local directory path.
    The filename is extracted from the remote path and used to construct the local file path. After downloading, it verifies
    that the file size matches the size on the SFTP server. If the sizes do not match, it raises a ValueError indicating a file size mismatch.

    Parameters:
        sftp (paramiko.SFTPClient): An active SFTP client connection.
        remote_filepath (str): The path to the remote file on the SFTP server.
        local_dirpath (str): The path to the local directory where the download will be saved.
        split_subdir (str): The subdirectory name to split the file path on. Defaults to 'data'.

    Returns:
        str: The path to the local file if the download was successful.

    Raises:
        ValueError: If the file size of the downloaded file does not match the file size on the SFTP server.
        Exception: If any other error occurs during the file download process.

    Example:
        ```python    
        hostname = 'sftp.example.com'
        port = 22
        username = 'your_username'
        password = 'your_password'
        remote_filepath = '/remote/path/to/data/subdir1/file1.jpg'
        local_dirpath = '/local/path/to/directory'
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        download_file(sftp, remote_filepath, local_dirpath, 'data')
        sftp.close()
        transport.close()
        ```
    """
    
    try:
        # Split the remote file path into components
        parts = remote_filepath.split('/')
        filename = parts[-1]

        # Find the index of the split_subdir in the parts
        if split_subdir in parts:
            split_index = parts.index(split_subdir)
            remote_subdir = os.path.join(*parts[split_index:])
        else:
            remote_subdir = ""

        # Construct the local file path using the structure from the split_subdir to the filename
        local_filepath = os.path.join(local_dirpath, remote_subdir)

        # Ensure the local directory exists
        os.makedirs(os.path.dirname(local_filepath), exist_ok=True)

        # Download the file from the SFTP server
        sftp.get(remote_filepath, local_filepath)

        # Verify the file size
        remote_file_size = sftp.stat(remote_filepath).st_size
        local_file_size = os.path.getsize(local_filepath)

        if remote_file_size != local_file_size:
            raise ValueError(f"Download failed for {remote_filepath}: file size mismatch. "
                             f"Remote size: {remote_file_size}, Local size: {local_file_size}")

        # Return the local file path if the download was successful
        return local_filepath

    except Exception as e:
        raise Exception(f"An error occurred while downloading {remote_filepath}: {e}")
