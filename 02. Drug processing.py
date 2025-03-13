## SCRIPT TO DOWNLOAD AND PROCESS ALL CMS ASP FILES AND COMBINE THEM INTO ONE FILE ##

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
directory = os.getcwd()

# List of files to download
# asp_files = ['jan05aspbyhcpcsv6_033106.zip','apr05aspbyhcpcsv8_033106.zip','jul05aspbyhcpcs_032906.zip','oct05aspbyhcpcs033106v2.zip','Jan06pricing.zip','apr06pricing.zip','july06asp_hcpcs.zip','oct06asp_hcpcs.zip','Jan07ASPbyHCPCS_121707.zip','April07ASPbyHCPCS_121707.zip','July07ASPbyHCPCS_121707.zip','October07ASPbyHCPCS.zip','Jan08ASPbyHCPCS.zip','April08ASPbyHCPCS.zip','July2008ASPPricingFilebyHCPCS.zip','October2008ASPPricingFilebyHCPCS.zip','JAN_2009_ASP_Pricing_File_by_HCPCS.zip','April_2009_ASP_Pricing_File_by_HCPCS.zip','July_2009_ASP_Pricing_File.zip','October_2009_ASP_Pricing_File.zip','January_2010_ASP_Pricing_File.zip','April_2010_ASP_Pricing_File.zip','July_2010_ASP_Pricing_File.zip','October_2010_ASP_Pricing_File.zip','January2011_ASP_PricingFile.zip','April_2011_ASP_Pricing_File.zip','July_2011_ASP_Pricing_File.zip','Oct_2011_ASP_Pricing_File.zip','Jan_2012_ASP_Pricing_File.zip','April-2012-ASP-Pricing-file-revised030513.zip','July-2012-ASP-Pricing-File.zip','October-2012-ASP-Pricing-File.zip','Jan-2013-ASP-Pricing-File.zip','Apr-13-ASP-Pricing-file.zip','2013-July-ASP-Pricing-File.zip','2013-October-ASP-Pricing-File.zip','Jan-14-ASP-Pricing-File.zip','Apr-14-ASP-Pricing-File.zip','Jul-2014-ASP-Pricing-File.zip','2014-October-ASP-Pricing-File.zip','2015-January-ASP-Pricing-File.zip','2015-April-ASP-Pricing-File.zip','2015-July-ASP-Pricing-File.zip','2015-October-ASP-Pricing-File.zip','2016-January-ASP-Pricing-File.zip','2016-April-ASP-Pricing-File.zip','2016-July-ASP-Pricing-File.zip','2016-October-ASP-Pricing-File.zip','2017-January-ASP-Pricing-Files.zip','2017-April-ASP-Pricing.zip','2017-July-ASP-Pricing-File.zip','2017-October-ASP-Pricing-File.zip','2018-January-ASP-Pricing-File.zip','2018-April-ASP-Pricing-File.zip','2018-July-ASP-Pricing-File.zip','2018-Oct-ASP-Pricing-File.zip','2019-January-ASP-Pricing-File.zip','April-2019-ASP-Pricing-File.zip','2019-July-ASP-Pricing-File.zip','2019-Oct-ASP-Pricing-File.zip','january-2020-asp-pricing-file.zip','april-2020-asp-pricing-file.zip','july-2020-asp-pricing-file-updated-06012020.zip','october-2020-asp-pricing-file.zip','january-2021-asp-pricing-file.zip','april-2021-asp-pricing-file.zip','july-2021-asp-pricing-file.zip','october-2021-asp-pricing-file.zip','january-2022-asp-pricing-file.zip','april-2022-asp-pricing-file.zip','july-2022-asp-pricing-file.zip','october-2022-asp-pricing-file.zip','january-2023-asp-pricing-file.zip','april-2023-asp-pricing-file.zip','july-2023-asp-pricing-file.zip','october-2023-asp-pricing-file.zip','january-2024-asp-pricing-file.zip','april-2024-asp-pricing-file.zip','july-2024-asp-pricing-file.zip','october-2024-asp-pricing-file.zip','january-2025-asp-pricing-file-12/19/24-final-file.zip']
asp_files = ['january-2025-asp-pricing-file-12/19/24-final-file.zip']

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
for file_name in asp_files:
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
for file_name in asp_files:
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
        print("No valid month found in file name!")
        time.sleep(100)
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
        print("Date range of file unclassified!")
        time.sleep(100)

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