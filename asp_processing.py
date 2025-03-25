## SCRIPT TO DOWNLOAD AND PROCESS ALL CMS ASP FILES AND COMBINE THEM INTO ONE FILE ##

import pandas as pd
import requests
import zipfile
import os
import glob
import re

from _process_all_cms import split_rates
from Dicts.asp_dicts import asp_file_dict
from custom_exceptions import InvalidMonthError, InvalidDateRange

# Get current working directory from parentfolder of folder containing scripts
directory = os.getcwd()

# List ASP schedules to include. Files are quarterly starting at 2005Q1. Format is YYYYQ.
asp_files = ['2018Q1', '2019Q1', '2020Q1', '2021Q1', '2022Q1', '2023Q1', '2024Q1', '2025Q1']

# Regular expression to match the year
year_pattern = re.compile(r'(20\d{2}|\d{2})')

# Create function to download and unzip ASP files from CMS website
def download_and_unzip_file(file, save_path):
    try:
        # Send a HTTP request to the specified URL
        if year == 2020:
            response = requests.get('https://www.cms.gov/files/zip/' + file + '?agree=yes&next=Accept')
        elif year > 2020:
            response = requests.get('https://www.cms.gov/files/zip/' + file)
        else:
            response = requests.get('https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Part-B-Drugs/McrPartBDrugAvgSalesPrice/downloads/' + file + '?agree=yes&next=Accept')

        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()

        # Define the complete path including the file name
        complete_save_path = os.path.join(save_path, file.replace("/","_"))

        # Open the specified file path in binary write mode and save the content
        if os.path.exists(complete_save_path):
            print(f"File already exists at {complete_save_path}")
        else:
            with open(complete_save_path, 'wb') as file:
                file.write(response.content)
            print(f"File successfully downloaded and saved to {complete_save_path}")

        # Define the extraction path
        extract_path = save_path

        # Check if the zip file has already been unzipped
        if os.path.exists(extract_path):
            non_zip_files_exist = any(
                entry for entry in os.scandir(extract_path)
                if entry.is_file() and not entry.name.endswith('.zip')
            )
            if non_zip_files_exist:
                print(f"Files already extracted to {extract_path}")
                return

        # Check if the file is a zip file
        if zipfile.is_zipfile(complete_save_path):
            with zipfile.ZipFile(complete_save_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                print(f"File successfully unzipped to {extract_path}")
        else:
            print(f"{complete_save_path} is not a zip file")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Loop through the list of files and download and unzip each one
for file in asp_files:
    file_name = asp_file_dict[file]
    folder_name = file_name[:-4].replace("/","_")

    # Create year object
    match = year_pattern.search(file_name)
    if match:
        year = match.group(0)
        if len(year) == 2:
            # Assuming the years are in the 2000s, so '05' -> '2005'
            year = '20' + year
        year = int(year)
    print(year)

    save_path = directory + fr'\Inputs\ASP\{year}\{folder_name}'
    os.makedirs(save_path, exist_ok=True)
    download_and_unzip_file(file_name, save_path)

# Create empty dataframe for appending
combined_asp = pd.DataFrame()

# Process each drug file and combine
for file in asp_files:
    file_name = asp_file_dict[file]
    print(file_name)
    folder_name = file_name[:-4].replace("/","_")

    # Create year object
    match = year_pattern.search(file_name)
    if match:
        year = match.group(0)
        if len(year) == 2:
            # Assuming the years are in the 2000s, so '05' -> '2005'
            year = '20' + year
        year = int(year)

    # Get Excel file name
    if year > 2007:
        file = glob.glob(directory + fr'\Inputs\ASP\{year}\{folder_name}\*.csv')
    else:
        file = glob.glob(directory + fr'\Inputs\ASP\{year}\{folder_name}\*HCPCS*.xls')

    # Create month object
    if "jan" in file[0].lower(): month = 1
    elif "apr" in file[0].lower(): month = 4
    elif "jul" in file[0].lower(): month = 7
    elif "oct" in file[0].lower(): month = 10
    else:
        raise InvalidMonthError(f"No valid month found in file name '{file_name}'!")
    yr_month = year*100 + month
    print(yr_month)
    
    # Avoid reading in 200701 CSV that has format issues
    if yr_month == 200701:
        file = glob.glob(directory + fr'\Inputs\ASP\{year}\{folder_name}\*HCPCS*.xls')
    
    # Read in ASP file
    if year >= 2020:
        asp_file = pd.read_csv(file[0], skiprows=8, encoding='cp1252')
    elif yr_month >= 200904 and yr_month < 202001:
        asp_file = pd.read_csv(file[0], skiprows=9, encoding='cp1252')
    elif yr_month >= 200801 and yr_month <= 200901:
        asp_file = pd.read_csv(file[0], skiprows=10, encoding='cp1252')
    elif year <= 2007 and yr_month != 200501:
        asp_file = pd.read_excel(file[0], skiprows=10, engine='xlrd')
    elif yr_month == 200501:
        asp_file = pd.read_excel(file[0], skiprows=11, engine='xlrd')
    else:
        raise InvalidDateRange(f"Date range of file unclassified '{file_name}', yr_mth: '{yr_month}'!")

    # Remove whitespace in column names
    asp_file.columns = asp_file.columns.str.replace(' ','')

    # Limit to relevant columns
    asp_file = asp_file[['HCPCSCode','ShortDescription','PaymentLimit']]
    
    # Rename columns
    asp_file = asp_file.rename(columns={'HCPCSCode': 'HCPCS', 'ShortDescription': 'SHORTDESC', 'PaymentLimit': 'RATE'})
    
    # Create YEAR column
    asp_file.insert(0,'YEAR', year)
    
    # Create EFF_DATE column
    asp_file.insert(1,'EFF_DATE', pd.to_datetime(str(yr_month), format='%Y%m'))
    
    # Create FILE_NAME column
    asp_file['FILE_NAME'] = os.path.basename(file[0])
    
    # Create combined ASP df
    combined_asp = pd.concat([combined_asp, asp_file], ignore_index=True)
    print(str(yr_month) + "ASP file processed")

# Convert to NP datetime format
combined_asp['EFF_DATE'] = combined_asp['EFF_DATE']

# Create geography column
combined_asp.insert(2,'GEOGRAPHY','NATIONAL')
combined_asp.insert(0, 'CMS SCHEDULE', '2. ASP')

split_rates(combined_asp)

# Save combined reults
combined_asp.to_csv(directory + r'\Outputs\Combined ASP.csv', index=False)
print(combined_asp)

# EOF