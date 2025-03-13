# Set up libraries
import pandas as pd
import numpy as np
import requests
import zipfile
import os
import glob
import re
import time

# Set current working directory to the directory containing the scripts being executed
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get current working directory from parentfolder of folder containing scripts
directory = os.getcwd()
print(directory)

# Create "Outputs" folder
os.makedirs(os.path.join(directory,'Outputs'), exist_ok=True)

# Import functions
from combine_data import combine

# Select date range (inclusive range)
start_yr = 2023
end_yr = 2024

# SETUP FUNCTIONS

# Function to create standard add on columns
def add_std_columns(df):
    df.insert(0, 'YEAR', year)
    df.insert(1, 'EFF_DATE', eff_date)
    df['FILE_NAME'] = os.path.basename(file_name)
    return df

def split_rates(df):
    df['NF RATE'] = df['RATE']
    df['F RATE'] = df['RATE']
    df.drop(columns=['RATE'], inplace=True)
    return df

# TODO: complete function below
# Function to download and unzip a file
# def download_and_unzip_file(file, save_path, year, new_url_year, base_url, new_accept, old_accept):
#     """
#     Downloads and unzips a file from the specified URL.
    
#     Parameters:
#     - file: The name of the file to download.
#     - save_path: The directory to save the file.
#     - year: The year to determine the URL structure.
#     - base_url: The base URL for the download.
#     - new_url_year: Year after which the URL changes.
#     - new_accept: Whether the new URL requires the '?agree=yes&next=Accept' suffix.
#     - old_accept: Whether the old URL requires the '?agree=yes&next=Accept' suffix.
#     """
#     try:
#         # Construct the URL based on the year and conditional logic
#         if year >= new_url_year:
#             if new_accept:
#                 url = 'https://www.cms.gov/files/zip/' + file + '?agree=yes&next=Accept'
#             else:
#                 url = 'https://www.cms.gov/files/zip/' + file
#         else:
#             if old_accept and file != 'rvu12b-.zip':  # file != 'rvu12b-.zip' meant to deal with one-off PFS file
#                 url = base_url + file + '?agree=yes&next=Accept'
#             else:
#                 url = base_url + file
                
#         # Send the HTTP request to download the file
#         print(url)
#         response = requests.get(url)
#         response.raise_for_status()
#         # Define the complete path including the file name
#         complete_save_path = os.path.join(save_path, file.replace("/","_"))
        
#         # Open the specified file path in binary write mode and save the content
#         if os.path.exists(complete_save_path):
#             print(f"File already exists at {complete_save_path}")
#         else:
#             with open(complete_save_path, 'wb') as file:
#                 file.write(response.content)
#             print(f"File successfully downloaded and saved to {complete_save_path}")
            
#         # Define the extraction path
#         extract_path = save_path
#         # Check if the zip file has already been unzipped
#         if os.path.exists(extract_path):
#             non_zip_files_exist = any(
#                 entry for entry in os.scandir(extract_path)
#                 if entry.is_file() and not entry.name.endswith('.zip')
#             )
#             if non_zip_files_exist:
#                 print(f"Files already extracted to {extract_path}")
#                 return
            
#         # Check if the file is a zip file
#         if zipfile.is_zipfile(complete_save_path):
#             with zipfile.ZipFile(complete_save_path, 'r') as zip_ref:
#                 zip_ref.extractall(extract_path)
#                 print(f"File successfully unzipped to {extract_path}")
#         else:
#             print(f"{complete_save_path} is not a zip file")
            
#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error occurred: {http_err}")
#     except Exception as err:
#         print(f"An error occurred: {err}")

with open(os.path.join(directory, r'01. PFS processing.py')) as file:
    exec(file.read())
with open(os.path.join(directory, r'02. Drug processing.py')) as file:
    exec(file.read())
with open(os.path.join(directory, r'03. Lab processing.py')) as file:
    exec(file.read())
with open(os.path.join(directory, r'04. DME processing.py')) as file:
    exec(file.read())
with open(os.path.join(directory, r'05. ASC processing.py')) as file:
    exec(file.read())

combine(directory, combined_pfs=combined_pfs, combined_asp=combined_asp, combined_lab=combined_lab, combined_dme=combined_dme, combined_asc=combined_asc)
    
# EOF