# Set up libraries
import os

# Import functions for processing
from pfs_processing import download_and_unzip_pfs, clean_and_combine_pfs
from asp_processing import download_and_unzip_asp, clean_and_combine_asp
from lab_processing import download_and_unzip_lab, clean_and_combine_lab
from dme_processing import download_and_unzip_dme, clean_and_combine_dmepos, clean_and_combine_dmepen
from asc_processing import download_and_unzip_asc, clean_and_combine_asc
from combine_data import combine


# --------- Config --------- #
# Set fee schedule downloading and processing you wish to run
schedules = {
                'pfs': True,
                'asp': True,
                'clab': True,
                'dme': True,
                'asc': True,
            }

######################################
# GEOGRAPHY INCLUSION SPECIFICATION #
######################################

# SELECT STATES AUTOMATICALLY INCLUDES NATIONAL GEO FOR PFS
pfs_states = ['AZ', 'CA', 'CO', 'NM', 'NV', 'OR', 'UT', 'WA']

# SELECT SPECIFIC GEOS WITHIN STATES
pfs_localities = [
                    'ARIZONA',
                    'LOS ANGELES-LONG BEACH-ANAHEIM (LOS ANGELES CNTY)',
                    'LOS ANGELES-LONG BEACH-ANAHEIM (ORANGE CNTY)',
                    'LOS ANGELES-LONG BEACH-ANAHEIM (LOS ANGELES/ORANGE CNTY)',
                    'RIVERSIDE-SAN BERNARDINO-ONTARIO',
                    'SAN DIEGO-CHULA VISTA-CARLSBAD',
                    'SAN JOSE-SUNNYVALE-SANTA CLARA (SAN BENITO CNTY)',
                    'SAN JOSE-SUNNYVALE-SANTA CLARA (SANTA CLARA CNTY)',
                    'COLORADO',
                    'NEW MEXICO',
                    'NEVADA',
                    'REST OF OREGON',
                    'PORTLAND',
                    'UTAH',
                    'SEATTLE (KING CNTY)',
                    'REST OF WASHINGTON'
                ]


# SELECT CLAB GEOGRAPHIES only applies to pre-2018 data
clab_geos = ['AZ', 'CA', 'CO', 'NM', 'NV', 'OR', 'UT', 'WA']

# SELECT DME GEOGRAPHIES TO INCLUDE IN OUTPUT FILE; pre-2016 geographies do not have separate rates for NR and R
dme_geos = ['AZ (NR)', 'CA (NR)', 'CO (NR)', 'NM (NR)', 'NV (NR)', 'OR (NR)', 'UT (NR)', 'WA (NR)']

######################################
# FILE INCLUSION SPECIFICATION #
######################################

# List ASP schedules to include. Files are quarterly starting at 2005Q1. Format is YYYYQ.
# There are a number of revision files. Mostly recently revised file is the default value for that year quarter in dict
# If a previous rate schedule to a revision is desired, use the format YYYYQ_p[1-9]
pfs_files = ['2026Q1', '2026Q2']

# List ASP schedules to include. Files are quarterly starting at 2005Q1. Format is YYYYQ.
asp_files = ['2026Q1', '2026Q2']

# List CLab schedules to include. Files are annual starting in 2008 (format is YYYY)
# and quarterly starting at 2018Q1 (format is YYYYQ).
lab_files = ['2026Q1', '2026Q2']

# List DME schedules to include. Files are quarterly starting at 1998Q1. Format is YYYYQ.
# There are a number of revision files. Mostly recently revised file is the default value for that year quarter in dict
# If a previous rate schedule to a revision is desired, use the format YYYYQ_[1-9]
dme_files = ['2026Q1', '2026Q2']

# List ASC schedules to include. Files are annual starting in 2001 (format is YYYY)
# and quarterly starting at 2018Q1 (format is YYYYQ).
asc_files = ['2026Q1', '2026Q2']


# Set current working directory to the directory containing the scripts being executed
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get current working directory from parentfolder of folder containing scripts
directory = os.getcwd()
print(directory)

# Create "Outputs" folder
os.makedirs(os.path.join(directory,'Outputs'), exist_ok=True)

############################################################################
# DOWNLOAD DATA FROM CMS WEBSITE AND PROCESS UNZIPPED DATA #
############################################################################

# PFS
if schedules['pfs']:
        download_and_unzip_pfs(pfs_files)
        combined_pfs = clean_and_combine_pfs(pfs_files, pfs_states, pfs_localities)
else:
    combined_pfs = None

# ASP
if schedules['asp']:
    download_and_unzip_asp(asp_files)
    combined_asp = clean_and_combine_asp(asp_files)
else:
    combined_asp = None

# CLAB
if schedules['clab']:
    download_and_unzip_lab(lab_files)
    combined_lab = clean_and_combine_lab(lab_files, clab_geos)
else:
    combined_lab = None

# DME
if schedules['dme']:
    download_and_unzip_dme(dme_files)
    combined_dmepos = clean_and_combine_dmepos(dme_files, dme_geos)
    combined_dmepen = clean_and_combine_dmepen(dme_files, dme_geos)
else:
    combined_dmepos = None
    combined_dmepen = None

# ASC
if schedules['asc']:
    download_and_unzip_asc(asc_files)
    combined_asc = clean_and_combine_asc(asc_files)
else:
    combined_asc = None

combine(directory, combined_pfs=combined_pfs, combined_asp=combined_asp, combined_lab=combined_lab,
        combined_dmepos=combined_dmepos, combined_dmepen=combined_dmepen, combined_asc=combined_asc)

print('\n----------------Processing complete. File is ready!')
