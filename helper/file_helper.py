import os
import csv
import requests
import hashlib
from config.logger_config import Logger

def file_exists(file_path):
    """Check if a file exists at the given file path.
    
    Args:
        file_path (str): Path to the file.
        
    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)

def download_file(document_url, isin):
    """Download a file from the given URL and save it to a directory based on the ISIN.
    
    Args:
        document_url (str): URL of the document to download.
        isin (str): ISIN identifier to create directory and save the file.
        
    Returns:
        tuple: Full file path and MD5 hash of the downloaded file if successful, otherwise (None, None).
    """
    file_name = document_url.split('/')[-1]
    directory_path = os.path.join(os.getcwd(), 'Hansainvest', isin) 
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, file_name)

    # Check if file already exists
    if file_exists(file_path):
        Logger.info(f"File {file_path} already exists, skipping download.")
        return None, None
    else:
        try:
            response = requests.get(document_url)
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                file.write(response.content)

            # Calculate MD5 hash
            md5_hash = calculate_md5(file_path)
            Logger.info(f"Downloaded file saved as {file_path} with MD5 hash {md5_hash}")
            return file_path, md5_hash

        except requests.exceptions.RequestException as e:
            Logger.error(f"Failed to download {document_url}: {e}")
            return None, None

def calculate_md5(file_path, chunk_size=8192):
    """Calculate the MD5 hash of a file.
    
    Args:
        file_path (str): Path to the file.
        chunk_size (int, optional): Size of the chunk to read at a time. Defaults to 8192.
        
    Returns:
        str: MD5 hash of the file.
    """
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                md5.update(chunk)
    except Exception as e:
        Logger.error(f"Error calculating MD5 for {file_path}: {e}")
        return None
    return md5.hexdigest()

def get_existing_file_paths(filename):
    """Retrieve existing file paths from the CSV file.
    
    Args:
        filename (str): Path to the CSV file.
        
    Returns:
        set: A set of file paths that already exist in the CSV.
    """
    existing_file_paths = set()
    if os.path.exists(filename):
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_file_paths.add(row['FilePath'])
    return existing_file_paths

def filter_new_records(records, existing_file_paths):
    """Filter out records that have existing file paths.
    
    Args:
        records (list): List of records (dictionaries) to filter.
        existing_file_paths (set): Set of existing file paths.
        
    Returns:
        list: List of new records that do not have existing file paths.
    """
    new_records = []
    for record in records:
        if record['FilePath'] not in existing_file_paths:
            new_records.append(record)
            existing_file_paths.add(record['FilePath'])
    return new_records

def append_to_csv(filename, new_records, fieldnames):
    """Append new records to the CSV file.
    
    Args:
        filename (str): Path to the CSV file.
        new_records (list): List of new records to append.
        fieldnames (list): List of field names (CSV columns).
    """
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if mode == 'w':
            writer.writeheader()
        writer.writerows(new_records)
    Logger.info(f"Added {len(new_records)} new records to {filename}")

def save_to_csv(records, filename):
    """Save records to the CSV file, filtering out duplicates.
    
    Args:
        records (list): List of records to save.
        filename (str): Path to the CSV file.
    """
    fieldnames = records[0].keys()
    existing_file_paths = get_existing_file_paths(filename)
    new_records = filter_new_records(records, existing_file_paths)
    if new_records:
        append_to_csv(filename, new_records, fieldnames)
    else:
        Logger.info("No new records to add.")
