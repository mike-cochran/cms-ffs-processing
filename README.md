# CMS FFS pricing

The code this set up to download and process the five different FFS rate schedules from CMS. There are five different
schedules considered:
  1. Physician fee schedule (PFS)
  2. Drug Average Sale Price (ASP) schedule
  3. Clinical Laboratory (CLAB) schedule
  4. Durable Medical Equipment (DME) schedule
  5. Ambulatory Surgical Center (ASC) schedule

# Instructions for running code

"_process_all_cms.py" is the only script that needs to be run. This script contains a dictionary to determine what 
schedules to download/process, lists to determine what geographies to include in the output and the years/quarters that 
wish to be included. Once the values for the lists are set, you can go ahead and run the script and it will produce the 
combined CMS data in the "Outputs" folder.

CMS adds new schedules every quarter. The dictionaries that contain the specific file names need to be updated with the 
new file names as published by CMS. This is a manual update that is required. You simply need to add another key/value 
pair for the file that was published by CMS.

## Outstanding work
  1. Homogenize more functions across schedules
  2. Process ASC files pre-2006
