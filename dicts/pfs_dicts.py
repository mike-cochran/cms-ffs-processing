# File name dictionary
pfs_file_dict = {'2003Q1': 'rvu03_a.zip',
                 '2003Q4': 'rvu03_d.zip',
                 '2004Q1': 'rvu04_a.zip',
                 '2004Q2': 'rvu04_b.zip',
                 '2004Q3': 'rvu04_c.zip',
                 '2004Q4': 'rvu04_d.zip',
                 '2005Q1_p1': 'rvu05_a.zip',  # 2005Q1 prior to revision
                 '2005Q1': 'rvu05a_r.zip',  # 2005Q1 revised
                 '2005Q2': 'rvu05_b.zip',
                 '2005Q3': 'rvu05_c.zip',
                 '2005Q4_p1': 'prrev05d.zip',  # 2005Q4 prior to revision
                 '2005Q4': 'rvu05_e.zip',  # 2005Q4 revised
                 '2006Q1_p2': 'rvu06a.zip',  # 2006Q1 prior to revision
                 '2006Q1_p1': 'rvu06ar.zip',  # 2006Q1 previous revision
                 '2006Q1': 'rvu06ar2.zip',  # 2006Q1 final revision
                 '2006Q2': 'rvu06b.zip',
                 '2006Q3': 'rvu06c.zip',
                 '2006Q4': 'rvu06d.zip',
                 '2007Q1_p2': 'rvu07a2.zip',  # 2007Q1 prior to revision
                 '2007Q1_p1': 'rvu07a3.zip',  # 2007Q1 previous revision
                 '2007Q1': 'rvu07a4.zip',  # 2007Q1 final revision
                 '2007Q2': 'rvu07b.zip',
                 '2007Q3': 'rvu07c.zip',
                 '2007Q4': 'rvu07d.zip',
                 '2008Q1': 'rvu08ar.zip',
                 '2008Q2': 'rvu08ab.zip',  # Physician Fee Schedule has been revised for the April 2008, despite confusing name
                 '2008Q3': 'rvu08c.zip',
                 '2008Q4': 'rvu08d.zip',
                 '2009Q1_p1': 'rvu09a.zip',  # 2009Q1 prior to revision
                 '2009Q1': 'rvu09ar.zip',  # 2009Q1 revised
                 '2009Q2': 'rvu09b.zip',
                 '2009Q3': 'rvu09c.zip',
                 '2010Q1': 'rvu10ar1.zip',
                 '2010Q3_p1': 'rvu10c_pct0.zip',  # Prior to 2.2% revision from 2010 legislation
                 '2010Q3': 'rvu10c_pct22.zip',  # After 2.2% rate adjustment from 2010 legislation
                 '2010Q4_p1': 'rvu10d_pct0.zip',  # Prior to 2.2% revision from 2010 legislation
                 '2010Q4': 'rvu10d_pct22.zip',  # After 2.2% rate adjustment from 2010 legislation
                 '2011Q1_p1': 'rvu11a.zip',  # 2011Q1 prior to revision
                 '2011Q1': 'rvu11ar.zip',  # 2011Q1 prior to revision
                 '2011Q2': 'rvu11b_2.zip',
                 '2011Q3': 'rvu11c.zip',
                 '2011Q4': 'rvu11d.zip',
                 '2012Q1_p1': 'rvu12a.zip',  # 2012Q1 prior to revision
                 '2012Q1': 'rvu12ar.zip',  # 2012Q1 revised for Jan. - Feb.
                 '2012Q1_march': 'rvu12m.zip',  # 2012Q1 revised for March
                 '2012Q2': 'rvu12b-.zip',
                 '2012Q3': 'rvu12c.zip',
                 '2012Q4': 'rvu12d.zip',
                 '2013Q1_p1': 'rvu13a.zip',
                 '2013Q1': 'rvu13ar.zip',
                 '2013Q2': 'rvu13b.zip',
                 '2013Q3': 'rvu13c.zip',
                 '2013Q4': 'rvu13d.zip',
                 '2014Q1': 'rvu14a.zip',
                 '2014Q2': 'rvu14b.zip',
                 '2014Q3': 'rvu14c.zip',
                 '2014Q4': 'rvu14d.zip',
                 '2015Q1': 'rvu15a.zip',
                 '2015Q2': 'rvu15b.zip',
                 '2015Q3': 'rvu15c.zip',
                 '2015Q4': 'rvu15d.zip',
                 '2016Q1': 'rvu16a.zip',
                 '2016Q2': 'rvu16b.zip',
                 '2016Q3': 'rvu16c.zip',
                 '2016Q4': 'rvu16d.zip',
                 '2017Q1': 'rvu17a.zip',
                 '2017Q2': 'rvu17b.zip',
                 '2017Q3': 'rvu17c.zip',
                 '2017Q4': 'rvu17d.zip',
                 '2018Q1_p2': 'rvu18a.zip',  # 2018Q1 prior to revisions
                 '2018Q1_p1': 'rvu18ar.zip',  # 2018Q1 revision incorporates changes from SUSTAIN Care Act
                 '2018Q1': 'rvu18ar1.zip',  # 2018Q1 final revision, includes revised Anesthesia Conversion Factors for 2018
                 '2018Q2': 'rvu18b.zip',
                 '2018Q3': 'rvu18c1.zip',
                 '2018Q4': 'rvu18d.zip',
                 '2019Q1': 'rvu19a.zip',
                 '2019Q2': 'rvu19b.zip',
                 '2019Q3': 'rvu19c.zip',
                 '2019Q4': 'rvu19d.zip',
                 '2020Q1': 'rvu20a-updated-01312020.zip',
                 '2020Q2': 'rvu20b.zip',
                 '2020Q3': 'rvu20c.zip',
                 '2020Q4': 'rvu20d.zip',
                 '2021Q1': 'rvu21a-updated-01052021.zip',
                 '2021Q2': 'rvu21b.zip',
                 '2021Q3': 'rvu21c.zip',
                 '2021Q4': 'rvu21d.zip',
                 '2022Q1': 'rvu22a.zip',
                 '2022Q2': 'rvu22b.zip',
                 '2022Q3': 'rvu22c.zip',
                 '2022Q4': 'rvu22d.zip',
                 '2023Q1': 'rvu23a.zip',
                 '2023Q2': 'rvu23b.zip',
                 '2023Q3': 'rvu23c.zip',
                 '2023Q4': 'rvu23d.zip',
                 '2024Q1_p1': 'rvu24a.zip',  # 2024Q1 rates for 1/1/24, through 3/8/24, the PFS CF is $32.7442
                 '2024Q1': 'rvu24ar.zip',  # 2024Q1 updated CF to $33.2875
                 '2024Q2': 'rvu24b-updated-03/18/2024.zip',
                 '2024Q3': 'rvu24c.zip',
                 '2024Q4': 'rvu24d.zip',
                 '2025Q1': 'rvu25a-updated-01/10/2025.zip'
                 }

# State and loc dictionary for PFS locality standardization
state_loc = {'2ALASKA': {'State': 'AK', 'Std Locality Name': 'ALASKA'}
    ,'ALABAMA': {'State': 'AL', 'Std Locality Name': 'ALABAMA'}
    ,'ALASKA': {'State': 'AK', 'Std Locality Name': 'ALASKA'}
    ,'ANAHEIM/SANTA ANA, CA': {'State': 'CA', 'Std Locality Name': 'ANAHEIM/SANTA ANA, CA'}
    ,'ARIZONA': {'State': 'AZ', 'Std Locality Name': 'ARIZONA'}
    ,'ARKANSAS': {'State': 'AR', 'Std Locality Name': 'ARKANSAS'}
    ,'ATLANTA': {'State': 'GA', 'Std Locality Name': 'ATLANTA'}
    ,'ATLANTA, GA': {'State': 'GA', 'Std Locality Name': 'ATLANTA'}
    ,'AUSTIN': {'State': 'TX', 'Std Locality Name': 'AUSTIN'}
    ,'AUSTIN, TX': {'State': 'TX', 'Std Locality Name': 'AUSTIN'}
    ,'BAKERSFIELD': {'State': 'CA', 'Std Locality Name': 'BAKERSFIELD'}
    ,'BAKERSFIELD, CA': {'State': 'CA', 'Std Locality Name': 'BAKERSFIELD'}
    ,'BALTIMORE/SURR. CNTYS': {'State': 'MD', 'Std Locality Name': 'BALTIMORE/SURR. CNTYS'}
    ,'BALTIMORE/SURR. CNTYS, MD': {'State': 'MD', 'Std Locality Name': 'BALTIMORE/SURR. CNTYS'}
    ,'BEAUMONT': {'State': 'TX', 'Std Locality Name': 'BEAUMONT'}
    ,'BEAUMONT, TX': {'State': 'TX', 'Std Locality Name': 'BEAUMONT'}
    ,'BRAZORIA': {'State': 'TX', 'Std Locality Name': 'BRAZORIA'}
    ,'BRAZORIA, TX': {'State': 'TX', 'Std Locality Name': 'BRAZORIA'}
    ,'CHICAGO': {'State': 'IL', 'Std Locality Name': 'CHICAGO'}
    ,'CHICAGO, IL': {'State': 'IL', 'Std Locality Name': 'CHICAGO'}
    ,'CHICO': {'State': 'CA', 'Std Locality Name': 'CHICO'}
    ,'CHICO, CA': {'State': 'CA', 'Std Locality Name': 'CHICO'}
    ,'COLORADO': {'State': 'CO', 'Std Locality Name': 'COLORADO'}
    ,'CONNECTICUT': {'State': 'CT', 'Std Locality Name': 'CONNECTICUT'}
    ,'DALLAS': {'State': 'TX', 'Std Locality Name': 'DALLAS'}
    ,'DALLAS, TX': {'State': 'TX', 'Std Locality Name': 'DALLAS'}
    ,'DC + MD/VA SUBURBS': {'State': 'DC', 'Std Locality Name': 'DC + MD/VA SUBURBS'}
    ,'DELAWARE': {'State': 'DE', 'Std Locality Name': 'DELAWARE'}
    ,'DETROIT': {'State': 'MI', 'Std Locality Name': 'DETROIT'}
    ,'DETROIT, MI': {'State': 'MI', 'Std Locality Name': 'DETROIT'}
    ,'EAST ST. LOUIS': {'State': 'IL', 'Std Locality Name': 'EAST ST. LOUIS'}
    ,'EAST ST. LOUIS, IL': {'State': 'IL', 'Std Locality Name': 'EAST ST. LOUIS'}
    ,'EL CENTRO': {'State': 'CA', 'Std Locality Name': 'EL CENTRO'}
    ,'EL CENTRO, CA': {'State': 'CA', 'Std Locality Name': 'EL CENTRO'}
    ,'FORT LAUDERDALE': {'State': 'FL', 'Std Locality Name': 'FORT LAUDERDALE'}
    ,'FORT LAUDERDALE, FL': {'State': 'FL', 'Std Locality Name': 'FORT LAUDERDALE'}
    ,'FORT WORTH': {'State': 'TX', 'Std Locality Name': 'FORT WORTH'}
    ,'FORT WORTH, TX': {'State': 'TX', 'Std Locality Name': 'FORT WORTH'}
    ,'FRESNO': {'State': 'CA', 'Std Locality Name': 'FRESNO'}
    ,'FRESNO, CA': {'State': 'CA', 'Std Locality Name': 'FRESNO'}
    ,'GALVESTON': {'State': 'TX', 'Std Locality Name': 'GALVESTON'}
    ,'GALVESTON, TX': {'State': 'TX', 'Std Locality Name': 'GALVESTON'}
    ,'HANFORD-CORCORAN': {'State': 'CA', 'Std Locality Name': 'HANFORD-CORCORAN'}
    ,'HANFORD-CORCORAN, CA': {'State': 'CA', 'Std Locality Name': 'HANFORD-CORCORAN'}
    ,'HAWAII, GUAM': {'State': 'HI', 'Std Locality Name': 'HAWAII, GUAM'}
    ,'HAWAII/GUAM': {'State': 'HI', 'Std Locality Name': 'HAWAII, GUAM'}
    ,'HAWAII/GUAM/AMERICAN SAMOA/NORTHERN MARIANA ISLANDS': {'State': 'HI', 'Std Locality Name': 'HAWAII, GUAM'}
    ,'HOUSTON': {'State': 'TX', 'Std Locality Name': 'HOUSTON'}
    ,'HOUSTON, TX': {'State': 'TX', 'Std Locality Name': 'HOUSTON'}
    ,'IDAHO': {'State': 'ID', 'Std Locality Name': 'IDAHO'}
    ,'INDIANA': {'State': 'IN', 'Std Locality Name': 'INDIANA'}
    ,'IOWA': {'State': 'IA', 'Std Locality Name': 'IOWA'}
    ,'KANSAS': {'State': 'KS', 'Std Locality Name': 'KANSAS'}
    ,'KENTUCKY': {'State': 'KY', 'Std Locality Name': 'KENTUCKY'}
    ,'LOS ANGELES, CA': {'State': 'CA', 'Std Locality Name': 'LOS ANGELES, CA'}
    ,'LOS ANGELES-LONG BEACH-ANAHEIM (LOS ANGELES CNTY)': {'State': 'CA', 'Std Locality Name': 'LOS ANGELES-LONG BEACH-ANAHEIM (LOS ANGELES CNTY)'}
    ,'LOS ANGELES-LONG BEACH-ANAHEIM (LOS ANGELES CNTY), CA': {'State': 'CA', 'Std Locality Name': 'LOS ANGELES-LONG BEACH-ANAHEIM (LOS ANGELES CNTY)'}
    ,'LOS ANGELES-LONG BEACH-ANAHEIM (LOS ANGELES/ORANGE CNTY)': {'State': 'CA', 'Std Locality Name': 'LOS ANGELES-LONG BEACH-ANAHEIM (LOS ANGELES/ORANGE CNTY)'}
    ,'LOS ANGELES-LONG BEACH-ANAHEIM (ORANGE CNTY)': {'State': 'CA', 'Std Locality Name': 'LOS ANGELES-LONG BEACH-ANAHEIM (ORANGE CNTY)'}
    ,'LOS ANGELES-LONG BEACH-ANAHEIM (ORANGE CNTY), CA': {'State': 'CA', 'Std Locality Name': 'LOS ANGELES-LONG BEACH-ANAHEIM (ORANGE CNTY)'}
    ,'MADERA': {'State': 'CA', 'Std Locality Name': 'MADERA'}
    ,'MADERA, CA': {'State': 'CA', 'Std Locality Name': 'MADERA'}
    ,'MANHATTAN': {'State': 'NY', 'Std Locality Name': 'MANHATTAN'}
    ,'MANHATTAN, NY': {'State': 'NY', 'Std Locality Name': 'MANHATTAN'}
    ,'MARIN/NAPA/SOLANO, CA': {'State': 'CA', 'Std Locality Name': 'MARIN/NAPA/SOLANO, CA'}
    ,'MERCED': {'State': 'CA', 'Std Locality Name': 'MERCED'}
    ,'MERCED, CA': {'State': 'CA', 'Std Locality Name': 'MERCED'}
    ,'METROPOLITAN BOSTON': {'State': 'MA', 'Std Locality Name': 'METROPOLITAN BOSTON'}
    ,'METROPOLITAN BOSTON, MA': {'State': 'MA', 'Std Locality Name': 'METROPOLITAN BOSTON'}
    ,'METROPOLITAN KANSAS CITY': {'State': 'MO', 'Std Locality Name': 'METROPOLITAN KANSAS CITY'}
    ,'METROPOLITAN KANSAS CITY, MO': {'State': 'MO', 'Std Locality Name': 'METROPOLITAN KANSAS CITY'}
    ,'METROPOLITAN PHILADELPHIA': {'State': 'PA', 'Std Locality Name': 'METROPOLITAN PHILADELPHIA'}
    ,'METROPOLITAN PHILADELPHIA, PA': {'State': 'PA', 'Std Locality Name': 'METROPOLITAN PHILADELPHIA'}
    ,'METROPOLITAN ST LOUIS, MO': {'State': 'MO', 'Std Locality Name': 'METROPOLITAN ST. LOUIS'}
    ,'METROPOLITAN ST. LOUIS': {'State': 'MO', 'Std Locality Name': 'METROPOLITAN ST. LOUIS'}
    ,'METROPOLITAN ST. LOUIS, MO': {'State': 'MO', 'Std Locality Name': 'METROPOLITAN ST. LOUIS'}
    ,'MIAMI': {'State': 'FL', 'Std Locality Name': 'MIAMI'}
    ,'MIAMI, FL': {'State': 'FL', 'Std Locality Name': 'MIAMI'}
    ,'MINNESOTA': {'State': 'MN', 'Std Locality Name': 'MINNESOTA'}
    ,'MISSISSIPPI': {'State': 'MS', 'Std Locality Name': 'MISSISSIPPI'}
    ,'MODESTO': {'State': 'CA', 'Std Locality Name': 'MODESTO'}
    ,'MODESTO, CA': {'State': 'CA', 'Std Locality Name': 'MODESTO'}
    ,'MONTANA': {'State': 'MT', 'Std Locality Name': 'MONTANA'}
    ,'NAPA': {'State': 'CA', 'Std Locality Name': 'NAPA'}
    ,'NAPA, CA': {'State': 'CA', 'Std Locality Name': 'NAPA'}
    ,'NATIONAL': {'State': 'NATIONAL', 'Std Locality Name': 'NATIONAL'}
    ,'NEBRASKA': {'State': 'NE', 'Std Locality Name': 'NEBRASKA'}
    ,'NEVADA': {'State': 'NV', 'Std Locality Name': 'NEVADA'}
    ,'NEW HAMPSHIRE': {'State': 'NH', 'Std Locality Name': 'NEW HAMPSHIRE'}
    ,'NEW MEXICO': {'State': 'NM', 'Std Locality Name': 'NEW MEXICO'}
    ,'NEW ORLEANS': {'State': 'LA', 'Std Locality Name': 'NEW ORLEANS'}
    ,'NEW ORLEANS, LA': {'State': 'LA', 'Std Locality Name': 'NEW ORLEANS'}
    ,'NORTH CAROLINA': {'State': 'NC', 'Std Locality Name': 'NORTH CAROLINA'}
    ,'NORTH DAKOTA': {'State': 'ND', 'Std Locality Name': 'NORTH DAKOTA'}
    ,'NORTHERN NJ': {'State': 'NJ', 'Std Locality Name': 'NORTHERN NJ'}
    ,'NYC SUBURBS/LONG I., NY': {'State': 'NY', 'Std Locality Name': 'NYC SUBURBS/LONG ISLAND'}
    ,'NYC SUBURBS/LONG ISLAND': {'State': 'NY', 'Std Locality Name': 'NYC SUBURBS/LONG ISLAND'}
    ,'NYC SUBURBS/LONG ISLAND, NY': {'State': 'NY', 'Std Locality Name': 'NYC SUBURBS/LONG ISLAND'}
    ,'OAKLAND/BERKELEY, CA': {'State': 'CA', 'Std Locality Name': 'OAKLAND/BERKELEY'}
    ,'OAKLAND/BERKLEY, CA': {'State': 'CA', 'Std Locality Name': 'OAKLAND/BERKELEY'}
    ,'OHIO': {'State': 'OH', 'Std Locality Name': 'OHIO'}
    ,'OKLAHOMA': {'State': 'OK', 'Std Locality Name': 'OKLAHOMA'}
    ,'OXNARD-THOUSAND OAKS-VENTURA': {'State': 'CA', 'Std Locality Name': 'OXNARD-THOUSAND OAKS-VENTURA'}
    ,'OXNARD-THOUSAND OAKS-VENTURA, CA': {'State': 'CA', 'Std Locality Name': 'OXNARD-THOUSAND OAKS-VENTURA'}
    ,'PORTLAND': {'State': 'OR', 'Std Locality Name': 'PORTLAND'}
    ,'PORTLAND, OR': {'State': 'OR', 'Std Locality Name': 'PORTLAND'}
    ,'POUGHKPSIE/N NYC SUBURBS': {'State': 'NY', 'Std Locality Name': 'POUGHKPSIE/N NYC SUBURBS'}
    ,'POUGHKPSIE/N NYC SUBURBS, NY': {'State': 'NY', 'Std Locality Name': 'POUGHKPSIE/N NYC SUBURBS'}
    ,'PUERTO RICO': {'State': 'PR', 'Std Locality Name': 'PUERTO RICO'}
    ,'QUEENS': {'State': 'NY', 'Std Locality Name': 'QUEENS'}
    ,'QUEENS, NY': {'State': 'NY', 'Std Locality Name': 'QUEENS'}
    ,'REDDING': {'State': 'CA', 'Std Locality Name': 'REDDING'}
    ,'REDDING, CA': {'State': 'CA', 'Std Locality Name': 'REDDING'}
    ,'REST OF CALIFORNIA': {'State': 'CA', 'Std Locality Name': 'REST OF CALIFORNIA'}
    ,'REST OF CALIFORNIA*': {'State': 'CA', 'Std Locality Name': 'REST OF CALIFORNIA'}
    ,'REST OF CALIFORNIA, CA': {'State': 'CA', 'Std Locality Name': 'REST OF CALIFORNIA'}
    ,'REST OF FLORIDA': {'State': 'FL', 'Std Locality Name': 'REST OF FLORIDA'}
    ,'REST OF GEORGIA': {'State': 'GA', 'Std Locality Name': 'REST OF GEORGIA'}
    ,'REST OF ILLINOIS': {'State': 'IL', 'Std Locality Name': 'REST OF ILLINOIS'}
    ,'REST OF LOUISIANA': {'State': 'LA', 'Std Locality Name': 'REST OF LOUISIANA'}
    ,'REST OF MAINE': {'State': 'ME', 'Std Locality Name': 'REST OF MAINE'}
    ,'REST OF MARYLAND': {'State': 'MD', 'Std Locality Name': 'REST OF MARYLAND'}
    ,'REST OF MASSACHUSETTS': {'State': 'MA', 'Std Locality Name': 'REST OF MASSACHUSETTS'}
    ,'REST OF MICHIGAN': {'State': 'MI', 'Std Locality Name': 'REST OF MICHIGAN'}
    ,'REST OF MISSOURI': {'State': 'MO', 'Std Locality Name': 'REST OF MISSOURI'}
    ,'REST OF MISSOURI*': {'State': 'MO', 'Std Locality Name': 'REST OF MISSOURI'}
    ,'REST OF NEW JERSEY': {'State': 'NJ', 'Std Locality Name': 'REST OF NEW JERSEY'}
    ,'REST OF NEW YORK': {'State': 'NY', 'Std Locality Name': 'REST OF NEW YORK'}
    ,'REST OF OREGON': {'State': 'OR', 'Std Locality Name': 'REST OF OREGON'}
    ,'REST OF PENNSYLVANIA': {'State': 'PA', 'Std Locality Name': 'REST OF PENNSYLVANIA'}
    ,'REST OF TEXAS': {'State': 'TX', 'Std Locality Name': 'REST OF TEXAS'}
    ,'REST OF WASHINGTON': {'State': 'WA', 'Std Locality Name': 'REST OF WASHINGTON'}
    ,'RHODE ISLAND': {'State': 'RI', 'Std Locality Name': 'RHODE ISLAND'}
    ,'RIVERSIDE-SAN BERNARDINO-ONTARIO': {'State': 'CA', 'Std Locality Name': 'RIVERSIDE-SAN BERNARDINO-ONTARIO'}
    ,'RIVERSIDE-SAN BERNARDINO-ONTARIO, CA': {'State': 'CA', 'Std Locality Name': 'RIVERSIDE-SAN BERNARDINO-ONTARIO'}
    ,'SACRAMENTO--ROSEVILLE--ARDEN-ARCADE': {'State': 'CA', 'Std Locality Name': 'SACRAMENTO-ROSEVILLE-FOLSOM'}
    ,'SACRAMENTO--ROSEVILLE--ARDEN-ARCADE, CA': {'State': 'CA', 'Std Locality Name': 'SACRAMENTO-ROSEVILLE-FOLSOM'}
    ,'SACRAMENTO-ROSEVILLE-FOLSOM': {'State': 'CA', 'Std Locality Name': 'SACRAMENTO-ROSEVILLE-FOLSOM'}
    ,'SALINAS': {'State': 'CA', 'Std Locality Name': 'SALINAS'}
    ,'SALINAS, CA': {'State': 'CA', 'Std Locality Name': 'SALINAS'}
    ,'SAN DIEGO-CARLSBAD': {'State': 'CA', 'Std Locality Name': 'SAN DIEGO-CARLSBAD'}
    ,'SAN DIEGO-CARLSBAD, CA': {'State': 'CA', 'Std Locality Name': 'SAN DIEGO-CARLSBAD'}
    ,'SAN DIEGO-CHULA VISTA-CARLSBAD': {'State': 'CA', 'Std Locality Name': 'SAN DIEGO-CARLSBAD'}
    ,'SAN FRANCISCO, CA': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO'}
    ,'SAN FRANCISCO-OAKLAND-BERKELEY (ALAMEDA/CONTRA COSTA CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (ALAMEDA/CONTRA COSTA CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-BERKELEY (MARIN CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (MARIN CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-BERKELEY (SAN FRANCISCO CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (SAN FRANCISCO CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-BERKELEY (SAN FRANCISCO/SAN MATEO/ALAMEDA/CONTRA COSTA CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (SAN FRANCISCO/SAN MATEO/ALAMEDA/CONTRA COSTA CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-BERKELEY (SAN MATEO CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (SAN MATEO CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-HAYWARD (ALAMEDA/CONTRA COSTA CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (ALAMEDA/CONTRA COSTA CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-HAYWARD (ALAMEDA/CONTRA COSTA CNTY), CA': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (ALAMEDA/CONTRA COSTA CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-HAYWARD (MARIN CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (MARIN CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-HAYWARD (MARIN CNTY), CA': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (MARIN CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-HAYWARD (SAN FRANCISCO CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (SAN FRANCISCO CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-HAYWARD (SAN FRANCISCO CNTY), CA': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (SAN FRANCISCO CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-HAYWARD (SAN MATEO CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (SAN MATEO CNTY)'}
    ,'SAN FRANCISCO-OAKLAND-HAYWARD (SAN MATEO CNTY), CA': {'State': 'CA', 'Std Locality Name': 'SAN FRANCISCO-OAKLAND-BERKELEY (SAN MATEO CNTY)'}
    ,'SAN JOSE-SUNNYVALE-SANTA CLARA (SAN BENITO CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN JOSE-SUNNYVALE-SANTA CLARA (SAN BENITO CNTY)'}
    ,'SAN JOSE-SUNNYVALE-SANTA CLARA (SAN BENITO CNTY), CA': {'State': 'CA', 'Std Locality Name': 'SAN JOSE-SUNNYVALE-SANTA CLARA (SAN BENITO CNTY)'}
    ,'SAN JOSE-SUNNYVALE-SANTA CLARA (SANTA CLARA CNTY)': {'State': 'CA', 'Std Locality Name': 'SAN JOSE-SUNNYVALE-SANTA CLARA (SANTA CLARA CNTY)'}
    ,'SAN JOSE-SUNNYVALE-SANTA CLARA (SANTA CLARA CNTY), CA': {'State': 'CA', 'Std Locality Name': 'SAN JOSE-SUNNYVALE-SANTA CLARA (SANTA CLARA CNTY)'}
    ,'SAN LUIS OBISPO-PASO ROBLES': {'State': 'CA', 'Std Locality Name': 'SAN LUIS OBISPO-PASO ROBLES'}
    ,'SAN LUIS OBISPO-PASO ROBLES-ARROYO GRANDE': {'State': 'CA', 'Std Locality Name': 'SAN LUIS OBISPO-PASO ROBLES'}
    ,'SAN LUIS OBISPO-PASO ROBLES-ARROYO GRANDE, CA': {'State': 'CA', 'Std Locality Name': 'SAN LUIS OBISPO-PASO ROBLES'}
    ,'SAN MATEO, CA': {'State': 'CA', 'Std Locality Name': 'SAN MATEO'}
    ,'SANTA CLARA, CA': {'State': 'CA', 'Std Locality Name': 'SANTA CLARA'}
    ,'SANTA CRUZ-WATSONVILLE': {'State': 'CA', 'Std Locality Name': 'SANTA CRUZ-WATSONVILLE'}
    ,'SANTA CRUZ-WATSONVILLE, CA': {'State': 'CA', 'Std Locality Name': 'SANTA CRUZ-WATSONVILLE'}
    ,'SANTA MARIA-SANTA BARBARA': {'State': 'CA', 'Std Locality Name': 'SANTA MARIA-SANTA BARBARA'}
    ,'SANTA MARIA-SANTA BARBARA, CA': {'State': 'CA', 'Std Locality Name': 'SANTA MARIA-SANTA BARBARA'}
    ,'SANTA ROSA': {'State': 'CA', 'Std Locality Name': 'SANTA ROSA-PETALUMA'}
    ,'SANTA ROSA, CA': {'State': 'CA', 'Std Locality Name': 'SANTA ROSA-PETALUMA'}
    ,'SANTA ROSA-PETALUMA': {'State': 'CA', 'Std Locality Name': 'SANTA ROSA-PETALUMA'}
    ,'SEATTLE (KING CNTY)': {'State': 'WA', 'Std Locality Name': 'SEATTLE (KING CNTY)'}
    ,'SEATTLE (KING CNTY), WA': {'State': 'WA', 'Std Locality Name': 'SEATTLE (KING CNTY)'}
    ,'SOUTH CAROLINA': {'State': 'SC', 'Std Locality Name': 'SOUTH CAROLINA'}
    ,'SOUTH DAKOTA': {'State': 'SD', 'Std Locality Name': 'SOUTH DAKOTA'}
    ,'SOUTHERN MAINE': {'State': 'ME', 'Std Locality Name': 'SOUTHERN MAINE'}
    ,'STOCKTON': {'State': 'CA', 'Std Locality Name': 'STOCKTON'}
    ,'STOCKTON-LODI': {'State': 'CA', 'Std Locality Name': 'STOCKTON'}
    ,'STOCKTON-LODI, CA': {'State': 'CA', 'Std Locality Name': 'STOCKTON'}
    ,'SUBURBAN CHICAGO': {'State': 'IL', 'Std Locality Name': 'SUBURBAN CHICAGO'}
    ,'SUBURBAN CHICAGO, IL': {'State': 'IL', 'Std Locality Name': 'SUBURBAN CHICAGO'}
    ,'TENNESSEE': {'State': 'TN', 'Std Locality Name': 'TENNESSEE'}
    ,'UTAH': {'State': 'UT', 'Std Locality Name': 'UTAH'}
    ,'VALLEJO': {'State': 'CA', 'Std Locality Name': 'VALLEJO'}
    ,'VALLEJO-FAIRFIELD': {'State': 'CA', 'Std Locality Name': 'VALLEJO'}
    ,'VALLEJO-FAIRFIELD, CA': {'State': 'CA', 'Std Locality Name': 'VALLEJO'}
    ,'VENTURA, CA': {'State': 'CA', 'Std Locality Name': 'VENTURA'}
    ,'VERMONT': {'State': 'VT', 'Std Locality Name': 'VERMONT'}
    ,'VIRGIN ISLANDS': {'State': 'VI', 'Std Locality Name': 'VIRGIN ISLANDS'}
    ,'VIRGINIA': {'State': 'VA', 'Std Locality Name': 'VIRGINIA'}
    ,'VISALIA': {'State': 'CA', 'Std Locality Name': 'VISALIA'}
    ,'VISALIA-PORTERVILLE': {'State': 'CA', 'Std Locality Name': 'VISALIA'}
    ,'VISALIA-PORTERVILLE, CA': {'State': 'CA', 'Std Locality Name': 'VISALIA'}
    ,'WEST VIRGINIA': {'State': 'WV', 'Std Locality Name': 'WEST VIRGINIA'}
    ,'WISCONSIN': {'State': 'WI', 'Std Locality Name': 'WISCONSIN'}
    ,'WYOMING': {'State': 'WY', 'Std Locality Name': 'WYOMING'}
    ,'YUBA CITY': {'State': 'CA', 'Std Locality Name': 'YUBA CITY'}
    ,'YUBA CITY, CA': {'State': 'CA', 'Std Locality Name': 'YUBA CITY'}
    }