## SCRIPT TO DOWNLOAD AND PROCESS ALL CMS DME FILES AND COMBINE THEM INTO ONE FILE ##

import pandas as pd
import requests
import zipfile
import os
import contextlib
import io
import glob
import re

from homogenized_functions import split_rates
from dicts.dme_dicts import dme_file_dict

# TODO: ADD DME PEN PROCESSING. SCRIPT ONLY COVERS DME POS

# Get current working directory from parentfolder of folder containing scripts
directory = os.getcwd()

# Need special processing for 'dme-l-code-update-file.zip' effective 1/1/2013

# Regex to match year
year_pattern = re.compile(r'(20\d{2}|\d{2})')

# Create function to download and unzip DME files from CMS website
def download_and_unzip_dme(file_list):

    for file in file_list:
        file_name = dme_file_dict[file]
        folder_name = file_name[:-4].replace("/", "_")

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

        try:
            # Send a HTTP request to the specified URL
            if year > 2019:
                response = requests.get('https://www.cms.gov/files/zip/' + file_name)
            else:
                response = requests.get('https://www.cms.gov/medicare/medicare-fee-for-service-payment/dmeposfeesched/downloads/' + file_name)

            # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()

            # Define the complete path including the file name
            complete_save_path = os.path.join(save_path, file_name.replace("/","_"))

            # Open the specified file path in binary write mode and save the content
            if os.path.exists(complete_save_path):
                print(f"File already exists at {complete_save_path}")
            else:
                with open(complete_save_path, 'wb') as file_name:
                    file_name.write(response.content)
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
                    continue

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

def clean_and_combine_dmepos(file_list, geo_list):

    # Create empty dataframe for appending
    combined_dme = pd.DataFrame()

    # Process each file and combine
    for file in file_list:
        file_name = dme_file_dict[file]
        file_name = file_name.replace("/","_")
        folder_name = file_name[:-4]
        print(file_name)

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
        dme_file = dme_file[dme_file['GEOGRAPHY'].isin(geo_list)]

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
    combined_dme.to_csv(directory + r'\Outputs\Combined DMEPOS.csv', index=False)
    print(combined_dme)

    return combined_dme

def clean_and_combine_dmepen(file_list, geo_list):

    # Create empty dataframe for appending
    combined_dme = pd.DataFrame()

    dme_file_ct = {2002: 0, 2003: 0, 2004: 0, 2005: 0, 2006: 0, 2007: 0, 2008: 0,
                   2009: 0, 2010: 0, 2011: 0, 2012: 0, 2013: 0, 2014: 0, 2015: 0}

    # Process each file and combine
    for file in file_list:
        file_name = dme_file_dict[file]
        file_name = file_name.replace("/","_")
        folder_name = file_name[:-4]
        print(file_name)

        # Create year object
        match = year_pattern.search(file_name)
        if match:
            year = match.group(0)
            if len(year) == 2:
                year = '20' + year
            year = int(year)
        print(year)

        # Prior to 2016 only annual set of rates after any revisions so only pull in one file for each year
        if year <= 2015:
            if dme_file_ct[year] == 1:
                continue  # Skip file if a PEN set of rates have already been read in for that year
            dme_file_ct[year] += 1

        # Get PEN file name and check if it exists
        file = glob.glob(directory + fr'\Inputs\DME\{year}\{folder_name}\*pen*.csv')
        if len(file) == 0:
            print(f"PEN file not found for {folder_name}")
            continue

        # Get the effective date of the file
        csv_file_name = os.path.basename(file[0])
        if year <= 2015:  # Only annual (January) updates to PEN prior to 2016 despite rate files published each release
            eff_date = "January " + str(year)
        else:
            with contextlib.redirect_stdout(io.StringIO()):
                with open(file[0]) as preview:
                    for i in range(1):
                        next(preview)
                    eff_date = preview.readline().split(',')[0]
            eff_date = re.search(r'\b\w+\s\d{4}\b', eff_date).group()
        eff_date = pd.to_datetime(eff_date, format='%B %Y')
        print(eff_date)

        # Read in CSV file particular to the format of that year
        if year == 2005:
            dme_file = pd.read_csv(file[0], skiprows=6, encoding='cp1252')
        elif year <= 2014:
            dme_file = pd.read_csv(file[0], skiprows=3, encoding='cp1252')
        elif year == 2015:
            dme_file = pd.read_csv(file[0], skiprows=1, encoding='cp1252')
        else:
            dme_file = pd.read_csv(file[0], skiprows=4, encoding='cp1252')
        print(file[0])

        # Create mod column mapping and standardize mod column names
        dme_file.columns = dme_file.columns.str.upper()  # Avoid case issues with column names
        mod_col_dict = {'MODIFIER 1': 'MOD', 'MODIFIER 2': 'MOD2'}
        dme_file = dme_file.rename(columns={col: mod_col_dict[col] for col in dme_file.columns if col in mod_col_dict})

        # Combine both mod columns into a single column
        dme_file['MOD'] = dme_file['MOD'] + dme_file['MOD2']

        # Remove extra columns
        dme_file = dme_file.drop(columns=['MOD2'])

        # Rename and reorder columns
        dme_file = dme_file.rename(columns=lambda col: 'SHORTDESC' if col[:4] in ['DESC','SHOR'] else col)
        col = dme_file.pop('SHORTDESC')
        dme_file.insert(2,'SHORTDESC',col)

        if year <= 2015:
            dme_file = dme_file.rename(columns=lambda col: 'RATE' if 'FEE' in col else col)
        else:
            # Create rate column for each geography
            cols = dme_file.columns.to_list()
            dme_file = pd.melt(dme_file, id_vars=['HCPCS','MOD','SHORTDESC'], value_vars=cols[4:], var_name = 'GEOGRAPHY', value_name = 'RATE')

            # Limit to relevant geographies
            if year >= 2024:
                geo_list = [geo.replace(' ', '') for geo in geo_list]  # Geos in PEN do not have spaces so need to remove
            dme_file = dme_file[dme_file['GEOGRAPHY'].isin(geo_list)]

        # Create YEAR and EFF_DATE column
        if year != 2015: dme_file.insert(0,'YEAR',year)
        dme_file.insert(1,'EFF_DATE',eff_date)

        # Drop blank rows based on missing CPT
        dme_file = dme_file.dropna(subset=['HCPCS'])

        # Create column for file name
        dme_file['FILE_NAME'] = csv_file_name

        # Create combined ASP df
        combined_dme = pd.concat([combined_dme, dme_file], ignore_index=True)

    # Convert to NP datetime format
    combined_dme['EFF_DATE'] = combined_dme['EFF_DATE']
    combined_dme.insert(0, 'CMS SCHEDULE', '4. DME')

    split_rates(combined_dme)

    # Save combined reults
    combined_dme.to_csv(directory + r'\Outputs\Combined DMEPEN.csv', index=False)
    print(combined_dme)

    return combined_dme
