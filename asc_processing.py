## SCRIPT TO DOWNLOAD AND PROCESS ALL CMS ASC FILES AND COMBINE THEM INTO ONE FILE ##

import pandas as pd
import requests
import zipfile
import os
import glob
import re

from homogenized_functions import split_rates
from Dicts.asc_dicts import asc_file_dict
from custom_exceptions import InvalidDateRange

# Get current working directory from parentfolder of folder containing scripts
directory = os.getcwd()

# List ASC schedules to include. Files are annual starting in 2001 (format is YYYY)
# and quarterly starting at 2018Q1 (format is YYYYQ).

# Regular expression to match the year
year_pattern = re.compile(r'(20\d{2}|\d{2})')
eff_date_pattern = re.compile(r'(\b[a-zA-Z][a-zA-Z][a-zA-Z]+\s\d{4})|(\b\w+\s\d{1,2},\s\d{4})|(\b\w+\sCY\s\d{4}\b)|(\bCY\s\d{4}\b)')

#
# # Create function to download and unzip ASC files from CMS website
def download_and_unzip_asc(file_list):

    for file in file_list:
        file_name = asc_file_dict[file]
        folder_name = file_name[:-4]

        # Create year object
        match = year_pattern.search(file_name)
        if match:
            year = match.group(0)
            if len(year) == 2:
                # Assuming the years are in the 2000s, so '05' -> '2005'
                year = '20' + year
            year = int(year)
        print(year)

        save_path = directory + fr'\Inputs\ASC\{year}\{folder_name}'
        os.makedirs(save_path, exist_ok=True)

        try:
            # Send a HTTP request to the specified URL
            if year > 2019:
                response = requests.get('https://www.cms.gov/files/zip/' + file_name + '?agree=yes&next=Accept')
            else:
                response = requests.get('https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/ascpayment/downloads/' + file_name + '?agree=yes&next=Accept')

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
                    zip_ref.extractall(extract_path)
                    print(f"File successfully unzipped to {extract_path}")
            else:
                print(f"{complete_save_path} is not a zip file")

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

# Function to standardize dates
def standardize_date(date_str):

    # Define the possible formats
    formats = ['%b %Y', '%B %Y', '%B %d, %Y', '%Y', '%B CY %Y', 'CY %Y', 'FINAL CY %Y']
    
    for fmt in formats:
        try:
            parsed_date = pd.to_datetime(date_str, format=fmt)
            # return parsed_date.strftime('%Y/%m/%d')
            return parsed_date
        except ValueError:
            continue
    return None

def process_data(df, year, file_name, rate_col_pattern):
    
    # Get effective date from rate column
    rate_col = df.filter(regex=rate_col_pattern).columns.tolist()[-1]
    if year >= 2008:
        eff_date = re.search(eff_date_pattern, rate_col).group()
        eff_date = standardize_date(eff_date)
    else:
        eff_date = pd.to_datetime(year, format='%Y')
        
    # Rename columns
    df.columns = df.columns.str.lower()
    df.rename(columns={df.filter(like='hcpcs', axis=1).columns[0]: 'HCPCS', 'short descriptor': 'SHORTDESC', rate_col.lower(): 'RATE'}, inplace=True)

    # Remove extra columns
    df = df[['HCPCS', 'SHORTDESC', 'RATE']]
    
    # Ensure HCPCS is a string
    df.loc[:, 'HCPCS'] = df['HCPCS'].astype(str)

    # Drop unnecessary rows
    df = df[~df['HCPCS'].str.contains('note|Asterisked', case=False, regex=True)]
    df.dropna(subset=['SHORTDESC'], inplace=True)

    # Create YEAR column
    df.insert(0, 'YEAR', year)

    # Create EFF_DATE column
    df.insert(1, 'EFF_DATE', eff_date)
    
    # Create FILE_NAME column
    df['FILE_NAME'] = os.path.basename(file_name)
    
    return df

# Process each ASC file and combine
def clean_and_combine_asc(file_list):

    # Create empty dataframe for appending
    combined_asc = pd.DataFrame()

    for file in file_list:
        file_name = asc_file_dict[file]
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
        print(year)

        # Get Excel file name
        files = glob.glob(directory + fr'\Inputs\ASC\{year}\{folder_name}\*.xls*')
        path = directory + fr'\Inputs\ASC\{year}\{folder_name}'
        if year == 2010:
            files = ['Rev_ASC_Apr10_AddAA_BB_DD1_ACA_zero_web_01Jun10', 'Rev_ASC_Jan10_AddAA_BB_DD1_ACA_zero_web_01Jun10', 'Jun10_ASC_AddAA_BB_DD1_ACA', 'Jul10_ASC_AddAA_BB_DD1_ACA', 'ASC_AddAA_BB_DD1_ACA_final']
            files = [os.path.join(path, file) + '.xlsx' for file in files]

        for file in files:
            print(file)

            if year >= 2008:

                # Set rate column regex pattern
                rate_col_pattern = '(.*\s\d{4}\s.*Payment)'

                # Get sheet names for AA and BB addenda
                xlsx = pd.ExcelFile(file)
                sheets = xlsx.sheet_names
                aa_sheet = next((name for name in sheets if 'AA' in name), None)
                bb_sheet = next((name for name in sheets if 'BB' in name), None)
                sheet_names = [aa_sheet, bb_sheet]

                # Loop through addenda AA and BB
                for addenda in sheet_names:
                    print(addenda)
                    if addenda == None:
                        continue
                    # Read in ASC file
                    if year >= 2018:
                        if addenda == bb_sheet and file_name in ['april-2020-asc-approved-hcpcs-code-and-payment-rates-updated-04092020.zip','july-2020-asc-approved-hcpcs-code-and-payment-rates.zip','october-2020-asc-approved-hcpcs-code-and-payment-rates.zip']:
                            row_skip = 2
                        elif file_name == 'march-9-2024-asc-approved-hcpcs-code-and-payment-rates.zip':
                            row_skip = 4
                        else:
                            row_skip = 3
                        asc_file = pd.read_excel(file, sheet_name=addenda, skiprows=row_skip)
                    elif year >= 2008:
                        if year >= 2010:
                            row_skip = 1
                            if year >= 2012: row_skip = 2
                            if year >= 2015: row_skip = 3
                            asc_file = pd.read_excel(file, sheet_name=addenda, skiprows=row_skip)
                        else:
                            row_skip = 1
                            if file[-9:] == 'Jul08.xls': row_skip = 2
                            asc_file = pd.read_excel(file, sheet_name=addenda, skiprows=row_skip, engine='xlrd')
                    processed_df = process_data(asc_file, year, file, rate_col_pattern)

                    # Create combined ASC df
                    combined_asc = pd.concat([combined_asc, processed_df], ignore_index=True)

            elif year >= 2003:

                # Set rate column regex pattern
                rate_col_pattern = '(.*Payment.*)'

                if year == 2006:
                    asc_file = pd.read_excel(file, sheet_name='asclist_ALL_2006 CPT codes', skiprows=1, engine='xlrd')
                else:
                    asc_file = pd.read_excel(file, engine='xlrd')
                processed_df = process_data(asc_file, year, file, rate_col_pattern)

                # Create combined ASC df
                combined_asc = pd.concat([combined_asc, processed_df], ignore_index=True)

            else:
                raise InvalidDateRange(f"Date range of file unclassified '{file_name}', year: '{year}'!")

    # Convert to NP datetime format
    combined_asc['EFF_DATE'] = combined_asc['EFF_DATE']

    # Fill in blank rate values with zeros
    combined_asc['RATE'] = combined_asc['RATE'].fillna(0)

    # Remove * from HCPCS
    combined_asc['HCPCS'] = combined_asc['HCPCS'].str.replace("*","", regex=False)

    # Sort by EFF_DATE and HCPCS
    combined_asc.sort_values(['EFF_DATE','HCPCS'], inplace=True)

    # Create geography column
    combined_asc.insert(2,'GEOGRAPHY','NATIONAL')
    combined_asc.insert(0, 'CMS SCHEDULE', '5. ASC')

    split_rates(combined_asc)

    # Save combined reults
    combined_asc.to_csv(directory + r'\Outputs\Combined ASC.csv', index=False)
    print(combined_asc)

    return combined_asc


################TESTING################
# asc_file = pd.read_excel(directory + r'\Inputs\ASC\2006\ascpuf2006\CY2006ASCPUF.11092005.xls', sheet_name='asclist_ALL_2006 CPT codes', skiprows=1, engine='xlrd')

# # Extract the rate column
# rate_col = asc_file.filter(regex='(.*Payment.*)').columns.tolist()[-1]
# print (rate_col)
# year = 2007
# eff_date = pd.to_datetime(str(year), format='%Y')

# # Rename columns
# asc_file.columns = asc_file.columns.str.lower()
# asc_file.rename(columns={asc_file.filter(like='HCPCS', axis=1).columns[0]: 'HCPCS', 'short descriptor': 'SHORTDESC', rate_col.lower(): 'RATE'}, inplace=True)

# # Remove extra columns
# asc_file = asc_file[['HCPCS', 'SHORTDESC', 'RATE']]

# # Ensure HCPCS is a string
# asc_file.loc[:, 'HCPCS'] = asc_file['HCPCS'].astype(str)

# # Drop unnecessary rows
# asc_file = asc_file[~asc_file['HCPCS'].str.contains('note|Asterisked', case=False, regex=True)]
# asc_file.dropna(subset=['SHORTDESC'], inplace=True)

# # Create YEAR column
# asc_file.insert(0, 'YEAR', year)

# # Create EFF_DATE column
# asc_file.insert(1, 'EFF_DATE', eff_date)

# # Create FILE_NAME column
# asc_file.loc[:, 'FILE_NAME'] = os.path.basename(file_name)
# print(asc_file)
# asc_file.to_csv(directory + r'\Outputs\ASC test.csv', index=False)
