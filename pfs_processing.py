## SCRIPT TO DOWNLOAD AND PROCESS ALL CMS PFS FILES AND COMBINE THEM INTO ONE FILE

import pandas as pd
import requests
import zipfile
import os
import glob
import re

from dicts.pfs_dicts import state_loc
from dicts.pfs_dicts import pfs_file_dict
from custom_exceptions import InvalidMonthError

# Get current working directory from parentfolder of folder containing scripts
directory = os.getcwd()

# Regular expression to match the year
year_pattern = re.compile(r'(20\d{2}|\d{2})')

# Create function to download and unzip pfs files from CMS website
def download_and_unzip_pfs(file_list):

    new_url_year = 2020
    base_url = 'https://www.cms.gov/medicare/medicare-fee-for-service-payment/physicianfeesched/downloads/'
    new_accept = False
    old_accept = True

    # Loop through the list of files and download and unzip each one
    for file in file_list:
        file_name = pfs_file_dict[file]
        print(file_name)
        folder_name = file_name[:-4].replace("/", "_")

        # Create year object
        match = year_pattern.search(file_name)
        if match:
            year = match.group(0)
            if len(year) == 2:
                # Assuming the years are in the 2000s, so '05' -> '2005'
                year = '20' + year
            year = int(year)
        print(year)

        save_path = directory + fr'\Inputs\PFS\{year}\{folder_name}'
        print(save_path)
        os.makedirs(save_path, exist_ok=True)

        try:
            # Construct the URL based on the year and conditional logic
            if year >= new_url_year:
                if new_accept:
                    url = 'https://www.cms.gov/files/zip/' + file_name + '?agree=yes&next=Accept'
                else:
                    url = 'https://www.cms.gov/files/zip/' + file_name
            else:
                if old_accept and file_name != 'rvu12b-.zip':  # file != 'rvu12b-.zip' meant to deal with one-off PFS file
                    url = base_url + file_name + '?agree=yes&next=Accept'
                else:
                    url = base_url + file_name

            # Send the HTTP request to download the file
            print(url)
            response = requests.get(url)
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

def clean_and_combine_pfs(file_list, states, localities):

    # Create empty dataframe for appending
    combined_pfs = pd.DataFrame()

    # Process each PFS file and combine
    for file in file_list:
        file_name = pfs_file_dict[file]
        file_name = file_name.replace("/","_")
        folder_name = file_name[:-4]
        print(file_name)
        # Create year object
        match = year_pattern.search(file_name)
        if match:
            year = match.group(0)
            if len(year) == 2:
                # Assuming the years are in the 2000s, so '05' -> '2005'
                year = '20' + year
            year = int(year)

        # Get Excel file name
        rvu_file_name = glob.glob(directory + fr'\Inputs\PFS\{year}\{folder_name}\*RVU*.csv')
        gpci_file_name = glob.glob(directory + fr'\Inputs\PFS\{year}\{folder_name}\*GPCI*.csv')
        print(rvu_file_name)
        print(gpci_file_name)

        # Create month object
        match = re.search(r'\b\w+\d{2}_?([a-z])',rvu_file_name[0].lower())
        if match:
            # Map the matched character to the corresponding month
            month_mapping = {'a': 1, 'b': 4, 'c': 7, 'd': 10, 'e': 10, 'm': 3}
            month = month_mapping[match.group(1)]
        else:
            raise InvalidMonthError(f"No valid month found in file name '{file_name}'!")
        yr_month = year*100 + month
        print(yr_month)

        # Process RVU file
        head_start = [5,6,7,8,9]
        if yr_month <= 200801: head_start = [4,5,6,7,8]
        if year <= 2005: head_start = [4,5,6,7]
        rvu = pd.read_csv(rvu_file_name[0], header=head_start, encoding='cp1252')

        # Function to concatenate headers while omitting "Unnamed"
        def concatenate_headers(header_tuple):
            return ' '.join([h for h in header_tuple if 'Unnamed' not in h]).strip()

        # Apply the function to the column MultiIndex
        rvu.columns = [concatenate_headers(col) for col in rvu.columns.values]

        # Limit to relevant columns
        rvu.columns = rvu.columns.str.replace("FULLY IMPLEMENTED ", "", regex=False)
        rvu = rvu[['HCPCS','MOD','DESCRIPTION','WORK RVU','NON-FAC PE RVU','FACILITY PE RVU','MP RVU', 'CONV FACTOR']]

        # Drop no rvu codes
        rvu['RVU_SUM'] = rvu[['WORK RVU','NON-FAC PE RVU','FACILITY PE RVU','MP RVU']].sum(axis=1)
        rvu = rvu[rvu['RVU_SUM'] != 0]
        rvu = rvu.drop(columns=['RVU_SUM'])

        # Drop NA row
        rvu.dropna(subset=['DESCRIPTION'], inplace=True)

        # Read in GPCI data
        row_skip = 2
        if year in [2003, 2004, 2014, 2015, 2016]: row_skip = 0
        if year in [2005, 2020]: row_skip = 1
        gpci = pd.read_csv(gpci_file_name[0], skiprows=row_skip, encoding='cp1252')

        # Drop unnecessary columns
        if year == 2011 and file_name != 'rvu11a.zip': gpci.drop(gpci.columns[[3,4,5]], axis=1, inplace=True)
        else: gpci.dropna(axis=1, how='all', inplace=True)
        gpci = gpci.iloc[:,-4:]

        # Clean up column names
        column_mapping = {0: 'Locality Name', 1: 'PW GPCI', 2: 'PE GPCI', 3: 'MP GPCI'}
        gpci.rename(columns={gpci.columns[i]: new_name for i, new_name in column_mapping.items()}, inplace=True)

        # Clean up locality values before merging
        gpci['Locality Name'] = gpci['Locality Name'].str.replace('*', '').str.strip().str.upper()

        # Drop empty rows
        gpci.dropna(subset=['MP GPCI'], inplace=True)

        # Merge on locality
        loc_lookup = pd.DataFrame.from_dict(state_loc, orient="index").reset_index()
        loc_lookup.rename(columns={'index': 'Locality Name'}, inplace=True)
        gpci = pd.merge(gpci, loc_lookup, how='left', on='Locality Name')

        # Limit to selected states and localities
        gpci = gpci[gpci['State'].isin(states)]
        gpci = gpci[gpci['Std Locality Name'].isin(localities)]

        # Create combined GEOGRAPHY column
        gpci.insert(0,'GEOGRAPHY', gpci['State'] + '-' + gpci['Std Locality Name'])
        gpci.drop(columns=['State', 'Locality Name', 'Std Locality Name'], inplace=True)

        # Values to be inserted
        new_row = {'GEOGRAPHY': ['NATIONAL'], 'PW GPCI': [1], 'PE GPCI': [1], 'MP GPCI': [1]}
        new_row = pd.DataFrame(new_row)
        gpci = pd.concat([gpci, new_row], ignore_index=True)

        # Create merge keys for Cartersian product and merge
        rvu['key'] = 1
        gpci['key'] = 1
        pfs_file = pd.merge(rvu, gpci, on='key').drop('key', axis=1)

        # Rename columns
        pfs_file = pfs_file.rename(columns={'DESCRIPTION': 'SHORTDESC'})

        #Create YEAR column
        pfs_file.insert(0,'YEAR', year)

        #Create EFF_DATE column
        pfs_file.insert(1,'EFF_DATE', pd.to_datetime(str(yr_month), format='%Y%m'))

        # Create FILE_NAME column
        pfs_file['FILE_NAME'] = os.path.basename(file_name)

        # Create combined pfs df
        combined_pfs = pd.concat([combined_pfs, pfs_file], ignore_index=True)
        print(str(yr_month) + "pfs file processed")

    # Convert to NP datetime format
    combined_pfs['EFF_DATE'] = combined_pfs['EFF_DATE']

    # Clean up column ordering
    combined_pfs = combined_pfs[['YEAR','EFF_DATE','GEOGRAPHY','HCPCS','MOD','SHORTDESC','WORK RVU','NON-FAC PE RVU','FACILITY PE RVU','MP RVU','PW GPCI','PE GPCI','MP GPCI','CONV FACTOR','FILE_NAME']]
    combined_pfs.insert(0, 'CMS SCHEDULE', '1. PFS')

    # Create combined RVU columns
    combined_pfs['NF RVUS'] = combined_pfs['WORK RVU']*combined_pfs['PW GPCI'] + combined_pfs['NON-FAC PE RVU']*combined_pfs['PE GPCI'] + combined_pfs['MP RVU']*combined_pfs['MP GPCI']
    combined_pfs['F RVUS'] = combined_pfs['WORK RVU']*combined_pfs['PW GPCI'] + combined_pfs['FACILITY PE RVU']*combined_pfs['PE GPCI'] + combined_pfs['MP RVU']*combined_pfs['MP GPCI']
    combined_pfs['NF RATE'] = combined_pfs['NF RVUS']*combined_pfs['CONV FACTOR']
    combined_pfs['F RATE'] = combined_pfs['F RVUS']*combined_pfs['CONV FACTOR']

    # Save combined reults
    combined_pfs.to_csv(directory + r'\Outputs\Combined PFS.csv', index=False)
    print(combined_pfs)

    return combined_pfs
