## SCRIPT TO DOWNLOAD AND PROCESS ALL CMS ASC FILES AND COMBINE THEM INTO ONE FILE ##

import pandas as pd
import os

# Get current working directory from parentfolder of folder containing scripts
directory = os.path.dirname(os.getcwd())

def combine(dir, combined_pfs=None, combined_asp=None, combined_lab=None, combined_dme=None, combined_asc=None):
    
    """Combines the CMS data into a single file and outputs it
    
    Parameters:
    - dir (str): Parent directory where project code is running
    - combined_pfs (DataFrame, optional): CMS PFS data
    - combined_asp (DataFrame, optional): CMS ASP data
    - combined_lab (DataFrame, optional): CMS LAB data
    - combined_dme (DataFrame, optional): CMS DME data
    - combined_asc (DataFrame, optional): CMS ASC data

    Outputs:
    - Saves the combined DataFrame as an Excel file
    """

    # Create empty combined CMS dataframe for appending
    combined_cms = pd.DataFrame()
    
    # Create list of dataframes for combining
    dfs_to_combine = [df for df in [combined_pfs, combined_asp, combined_lab, combined_dme, combined_asc] if df is not None and not df.empty]
    
    # Check if no dfs to combine
    if not dfs_to_combine:
        print('No valid dataframes provided. Skipping combination.')
        return

    combined_cms = pd.concat(dfs_to_combine, ignore_index=True)

    # Move FILE_NAME column to end of df
    combined_cms['FILE_NAME'] = combined_cms.pop('FILE_NAME')

    # Save the combined DataFrame as an Excel file in the Outputs folder
    output_path = os.path.join(dir, 'Outputs', 'Combined CMS.xlsx')
    combined_cms.to_excel(output_path, sheet_name = 'raw', index=False)
    
    print(f'Combined CMS data saved to {output_path}')
