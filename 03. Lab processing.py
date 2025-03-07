## SCRIPT TO DOWNLOAD AND PROCESS ALL CMS LAB FILES AND COMBINE THEM INTO ONE FILE ##

import pandas as pd
import numpy as np
import requests
import zipfile
import os
import glob
import re
import time

from Runall import split_rates

# Get current working directory from parentfolder of folder containing scripts
directory = os.path.dirname(os.getcwd())

# List of files to download
# lab_files = ['08CLAB-b.zip','09CLAB.zip','10CLAB.zip','11CLAB.zip','Clab2011C.zip','12CLAB.zip','13CLAB.zip','14CLAB.zip','15CLAB.zip','16CLAB.zip','17CLAB.zip','18CLAB.zip','18CLABQ2.zip','18CLABQ3.zip','19CLABQ1.zip','19CLABQ3.zip','19CLABQ4.zip','20CLABQ1.zip','20CLABQ2.zip','20CLABQ3.zip','20CLABQ4.zip','21CLABQ1.zip','21CLABQ2.zip','21CLABQ3.zip','21CLABQ4.zip','22CLABQ1.zip','22CLABQ2.zip','22CLABQ3.zip','22CLABQ4.zip','23CLABQ1.zip','23CLABQ2.zip','23CLABQ3.zip','23CLABQ4.zip','24CLABQ1.zip', '24CLABQ2.zip','24CLABQ3.zip','24CLABQ4.zip','25CLABQ1.zip']
lab_files = ['25CLABQ1.zip']

#TODO: '10CLABAPR.zip' NEED TO FIGURE OUT HOW TO UNZIP AND PROCESS THIS DATA

# Regular expression to match the year
year_pattern = re.compile(r'(20\d{2}|\d{2})')

def download_and_unzip_file(file, save_path):
    try:
        # Send a HTTP request to the specified URL
        if year > 2019:
            response = requests.get('https://www.cms.gov/files/zip/' + file + '?agree=yes&next=Accept')
        else:
            response = requests.get('https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/ClinicalLabFeeSched/Downloads/' + file + '?agree=yes&next=Accept')

        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()

        # Define the complete path including the file name
        complete_save_path = os.path.join(save_path, file)

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
for file_name in lab_files:
    folder_name = file_name[:-4]
    if file_name[:1] == 'C':
        year = 2000
    else:
        year = 2000 + int(file_name[:2])
    year = int(year)
    save_path = directory + fr'\Inputs\Lab\{folder_name}'
    os.makedirs(save_path, exist_ok=True)
    download_and_unzip_file(file_name, save_path)

# Create empty dataframe for appending
combined_lab = pd.DataFrame()

# Process each file and combine
for file_name in lab_files:
    print(file_name)
    folder_name = file_name[:-4]
    
    # Create year object
    match = year_pattern.search(file_name)
    if match:
        year = match.group(0)
        if len(year) == 2:
            # Assuming the years are in the 2000s, so '05' -> '2005'
            year = '20' + year
        year = int(year)
    
    if year <= 2017 and year > 2014:
        file = glob.glob(directory + fr'\Inputs\Lab\{folder_name}\*.xls')
    elif year == 2014: # Need to also add in the 2014 April codes
        file = [directory + fr'\Inputs\Lab\{folder_name}\CLAB2014.EffJan1.Full.xls']
    else:
        file = glob.glob(directory + fr'\Inputs\Lab\{folder_name}\*.csv')

    # Read in CSV file particular to the format of that year
    if year < 2014:
        lab_file = pd.read_csv(file[0], skiprows=4, encoding='cp1252')
    if year < 2018 and year >= 2014:
        lab_file = pd.read_excel(file[0], skiprows=3, engine='xlrd')
    if (year < 2023 and year >= 2018) or folder_name == '23CLABQ1':
        lab_file = pd.read_csv(file[0], skiprows=3, encoding='cp1252')
        
    if year >= 2023 and folder_name != '23CLABQ1':
        lab_file = pd.read_csv(file[0], skiprows=4, encoding='cp1252')
    len(lab_file)
    # Standardize file format
    if year <= 2017:
        
        if year < 2014:
            # Apply names to unnamed columns
            col_names = ['HCPCS', 'Modifier', 'National Limit', 'Mid Point', 'Floor']
            column_mapping = {lab_file.columns[i]: col_names[i] for i in range(5)}
            lab_file.rename(columns=column_mapping, inplace=True)
            lab_file.rename(columns={lab_file.columns[-1]: 'SHORTDESC'}, inplace=True)

        # Remove first two rows
        lab_file = lab_file.iloc[2:]

        # Remove extra columns
        lab_file = lab_file.drop(columns=['Mid Point','Floor'])

        # Reorder columns
        col = lab_file.pop('SHORTDESC')
        lab_file.insert(2,'SHORTDESC',col)

        # Create rate column for each geography
        cols = lab_file.columns.to_list()
        lab_file = pd.melt(lab_file, id_vars=['HCPCS','Modifier','SHORTDESC'], value_vars=cols[4:], var_name = 'GEOGRAPHY', value_name = 'RATE')

        # Create YEAR column
        lab_file.insert(0,'YEAR',year)
        
        # Rename modifier column
        lab_file.rename(columns={'Modifier': 'MOD'}, inplace=True)
        
        #Create EFF_DATE column, 2011C is the revised rates effective 4/1/2011 according to CMS website
        if file_name == 'Clab2011C.zip':
            lab_file.insert(1,'EFF_DATE',pd.to_datetime('2011-04-01'))
        else:
            lab_file.insert(1,'EFF_DATE',pd.to_datetime(str(year), format='%Y'))
        
    if year > 2017:
        # Limit to desired columns
        rate_col = lab_file.filter(regex='^RATE').columns.tolist()[0]
        cols = ['YEAR','HCPCS','MOD','EFF_DATE','SHORTDESC',rate_col]
        lab_file = lab_file[cols]

        # Create geography column
        lab_file.insert(2,'GEOGRAPHY','NATIONAL')

        # Rename columns
        lab_file = lab_file.rename(columns={rate_col: 'RATE'})
        
        # Format EFF_DATE column
        lab_file['EFF_DATE'] = pd.to_datetime(lab_file['EFF_DATE'], format='%Y%m%d')

    # Create column for file name
    lab_file['FILE_NAME'] = os.path.basename(file[0])
    
    # Create combined Lab df
    combined_lab = pd.concat([combined_lab, lab_file], ignore_index=True)
    
# Convert to NP datetime format
combined_lab['EFF_DATE'] = combined_lab['EFF_DATE']
combined_lab.insert(0, 'CMS SCHEDULE', '3. LAB')

split_rates(combined_lab)

# Save combined reults
combined_lab.to_csv(directory + r'\Outputs\Combined Lab.csv', index=False)

# EOF