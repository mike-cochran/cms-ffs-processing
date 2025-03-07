## SCRIPT TO DOWNLOAD AND PROCESS ALL CMS DME FILES AND COMBINE THEM INTO ONE FILE ##

import pandas as pd
import numpy as np
import requests
import zipfile
import os
import contextlib
import io
import glob
import re
import time

from Runall import split_rates

# TODO: ADD DME PEN PROCESSING. SCRIPT ONLY COVERS DME POS

# SELECT GEOGRAPHIES TO INCLUDE IN OUTPUT FILE; pre-2016 geographies do not have separate rates for NR and R
geos = ['WA (NR)']

# Get current working directory from parentfolder of folder containing scripts
directory = os.path.dirname(os.getcwd())

# List of files to download
# dme_files = ['dme98_d.zip','dme99_c.zip','dme00_b.zip','dme00_c.zip','dme01_a.zip','d01jan_c.zip','d01july_c.zip','d02jan_a.zip','d02jan_c.zip','d02jan_d.zip','d03_jan_r.zip','d03_jan_b.zip','d03_jan_c.zip','d03_jan_d.zip','d04_jan.zip','d04_janb.zip','d04_janc.zip','d04_jand.zip','d05_jan_r.zip','d05_janr2.zip','d05_jand.zip','d05_jan_b.zip','d05_jan_b3.zip','d05_jan_c.zip','d05_jan_d.zip','d06_jan.zip','d06_jan_r.zip','d06_jan_b.zip','d06_jan_c2.zip','d06_jan_d.zip','d06_jan_g.zip','d06_jan_h.zip','d06_jan_i.zip','d07_jan.zip','d07_jan_r.zip','d07_jan_c.zip','d08_janr2.zip','d08_jan_c.zip','d09_janr.zip', 'd09_jan_c.zip','d10_janr.zip','dme10_c.zip','2010dmev2.zip','dme10_oct.zip','dme11_a.zip','dmepos2011_-l3660_l3670_l3675_pricing.zip','dme11_c.zip','dme12_a.zip','dme12_c.zip','dme13-a.zip','dme13_b.zip','dme13-c-file.zip','dme14-a.zip','dme14-b.zip','dme14-c.zip','dme15-a.zip','dme15-c.zip','dme15-d.zip','dme16-a.zip','dme16-b.zip','dme16-c.zip','dme16-d.zip','dme17-a.zip','dme17-b.z8ip','dme17-c.zip','dme17-d.zip','dme18-a.zip','dme18-b.zip','dme18-c.zip','dme18-d.zip','dme18-ifc.zip','dme19-a.zip','dme19-b.zip','dme19-c.zip','dme19-d.zip','dme20.zip','dme20-b.zip','dme20-c.zip','dme20-d.zip','dme20-cares.zip','dme21.zip','dme-21ar.zip','dme21-b.zip','dme21-d.zip','dme22.zip','dme22-b-posted-031522.zip','dme22c-posted-061722.zip','dme22-d.zip','dme22-r.zip','dme23-updated-12192022.zip','dme23-b.zip','dme23c.zip','dme23d.zip','dme24.zip','dme24-b.zip','dme24-c.zip','dme24-d.zip','dme25.zip']
dme_files = ['dme25.zip']

# Need special processing for 'dme-l-code-update-file.zip' effective 1/1/2013

# Regex to match year
year_pattern = re.compile(r'(20\d{2}|\d{2})')

def download_and_unzip_file(file, save_path):
    try:
        # Send a HTTP request to the specified URL
        if year > 2019:
            response = requests.get('https://www.cms.gov/files/zip/' + file)
        else:
            response = requests.get('https://www.cms.gov/medicare/medicare-fee-for-service-payment/dmeposfeesched/downloads/' + file)

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
                try:
                    zip_ref.extractall(extract_path)
                    print(f"File successfully unzipped to {extract_path}")
                except Exception as e:
                    print(f"Error: {e} encountered while trying to unzip all files. Attempting to unzip individual files...")
                    for file in zip_ref.namelist():
                        try:
                            zip_ref.extract(file, extract_path)
                            print(f"{file} successfully unzipped to {extract_path}")
                        except zipfile.BadZipFile:
                            print(f"Error: BadZipFile encountered for {file}. Skipping this file.")
                        except Exception as e:
                            print(f"Error: {e} encountered for {file}. Skipping this file.")
        else:
            print(f"{complete_save_path} is not a zip file")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Loop through the list of files and download and unzip each one
for file_name in dme_files:
    folder_name = file_name[:-4]
    
    # Create year object
    match = year_pattern.search(file_name)
    if match:
        year = match.group(0)
        if len(year) == 2 and int(year) < 98:
            year = '20' + year
        elif len(year) == 2 and int(year) >= 98:
            year = '19' + year
        year = int(year)
    print(year)
    
    save_path = directory + fr'\Inputs\DME\{year}\{folder_name}'
    os.makedirs(save_path, exist_ok=True)
    download_and_unzip_file(file_name, save_path)

# Create empty dataframe for appending
combined_dme = pd.DataFrame()

# Process each file and combine
for file_name in dme_files:
    print(file_name)
    folder_name = file_name[:-4]
    
    # Create year object
    match = year_pattern.search(file_name)
    if match:
        year = match.group(0)
        if len(year) == 2 and int(year) < 98:
            year = '20' + year
        elif len(year) == 2 and int(year) >= 98:
            year = '19' + year
        year = int(year)
    print(year)
    
    # Get POS file name and check if it exists
    dme_csvs = glob.glob(directory + fr'\Inputs\DME\{year}\{folder_name}\*.csv')
    if year >= 2010: file = [dmeposcsv for dmeposcsv in dme_csvs if os.path.getsize(dmeposcsv) > 1000 * 1024]  # 1,000 KB = 1,000 * 1024 bytes
    else: file = [dmeposcsv for dmeposcsv in dme_csvs if os.path.getsize(dmeposcsv) > 800 * 1024]  # 1,000 KB = 1,000 * 1024 bytes
    if len(file) == 0:
        print(f"POS file not found for {folder_name}")
        continue
    
    # Get the effective date of the file
    csv_file_name = os.path.basename(file[0])
    if year < 2010:
        # Base effective date off zip file name for years before 2010
        if "_b" in file_name: eff_date = "April 1 " + str(year)
        elif "_c" in file_name: eff_date = "July 1 " + str(year)
        elif "_d" in file_name: eff_date = "October 1 " + str(year)
        else: eff_date = "January 1 " + str(year)
        
        if file_name == 'd01jan_c.zip': eff_date = "January 1 " + str(year) # Override the default date based on the zip file name, CMS website specifies rates are eff. 1/1/2001
        if file_name == 'd06_jan_g.zip': eff_date = "November 15 " + str(year) # To deal with unique file in 2006
        eff_date = pd.to_datetime(eff_date, format='%B %d %Y')
    else:
        # Base effective date off CSV file name for years 2010-2014
        if 2010 <= year <= 2014:
            if "jan" in csv_file_name.lower(): eff_date = "January " + str(year)
            elif "apr" in csv_file_name.lower(): eff_date = "April " + str(year)
            elif "jul" in csv_file_name.lower(): eff_date = "July " + str(year)
            elif "oct" in csv_file_name.lower(): eff_date = "October " + str(year)
        # Base effective date off month and year found in 1st column 4th row of csv file
        else:
            with contextlib.redirect_stdout(io.StringIO()):
                with open(file[0]) as preview:
                    for i in range(3):
                        next(preview)
                    eff_date = preview.readline().split(',')[0]
            eff_date = re.search(r'\b\w+\s\d{4}\b', eff_date).group()
        eff_date = pd.to_datetime(eff_date, format='%B %Y')
    print(eff_date)

    # Read in CSV file particular to the format of that year
    if file_name in ['dme99_c.zip', 'd07_jan.zip']:
        dme_file = pd.read_excel(file[0], engine='xlrd', skiprows=6)
        if file_name == 'd07_jan.zip':
            dme_file = dme_file.iloc[1:].reset_index(drop=True)
    else:
        dme_file = pd.read_csv(file[0], skiprows=6, encoding='cp1252')
    print(file[0])

    # Combine both mod columns into a single column
    dme_file.columns = dme_file.columns.str.upper()
    print(dme_file)
    dme_file['MOD'] = dme_file['MOD'] + dme_file['MOD2']

    # Remove extra columns
    dme_file = dme_file.drop(columns=['MOD2','JURIS','CATG','CEILING','FLOOR'])

    # Rename and reorder columns
    dme_file = dme_file.rename(columns=lambda col: 'SHORTDESC' if col[:4] == 'DESC' else col)
    col = dme_file.pop('SHORTDESC')
    dme_file.insert(2,'SHORTDESC',col)

    # Create rate column for each geography
    cols = dme_file.columns.to_list()
    dme_file = pd.melt(dme_file, id_vars=['HCPCS','MOD','SHORTDESC'], value_vars=cols[4:], var_name = 'GEOGRAPHY', value_name = 'RATE')

    # Limit to relevant geographies
    dme_file = dme_file[dme_file['GEOGRAPHY'].isin(geos)]

    # Create YEAR and EFF_DATE column
    dme_file.insert(0,'YEAR',year)
    dme_file.insert(1,'EFF_DATE',eff_date)
    
    # Create column for file name
    dme_file['FILE_NAME'] = csv_file_name
    
    # Create combined ASP df
    combined_dme = pd.concat([combined_dme, dme_file], ignore_index=True)
    
# Convert to NP datetime format
combined_dme['EFF_DATE'] = combined_dme['EFF_DATE']
combined_dme.insert(0, 'CMS SCHEDULE', '4. DME')

split_rates(combined_dme)

# Save combined reults
combined_dme.to_csv(directory + r'\Outputs\Combined DME.csv', index=False)
print(combined_dme)


# EOF