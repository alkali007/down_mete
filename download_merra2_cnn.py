import os
import requests
from datetime import datetime, timedelta
import calendar

def download_merra2_cnn(start_year, end_year, start_month, end_month, save_path):
    # Define the new base URL pattern
    base_url = "https://acdisc.gesdisc.eosdis.nasa.gov/opendap/HAQAST/MERRA2_CNN_HAQAST_PM25.1/{year}/MERRA2_HAQAST_CNN_L4_V1.{date}.nc4.nc4?MERRA2_CNN_Surface_PM25[0:23][158:192][440:514],QFLAG[158:192][440:514],time,lat[158:192],lon[440:514]"

    # Initialize the array to store generated URLs
    generated_urls = []

    # Loop through the specified year and month
    for year in range(start_year, end_year + 1):
        for month in range(start_month, end_month + 1):
            # Get the last day of the month using calendar.monthrange
            _, last_day_of_month = calendar.monthrange(year, month)
            for day in range(1, last_day_of_month + 1):
                user_date = f"{year}{str(month).zfill(2)}{str(day).zfill(2)}"
                url = base_url.format(year=year, date=user_date)
                generated_urls.append(url)

    # Specify the path where you want to save the downloaded files based on the URL year
    for url in generated_urls:
        year_from_url = url.split('/')[-2]  # Extract the year from the URL

        # Adjust the path to save files in the specified save_path
        save_path_year = os.path.join(save_path, year_from_url)

        # Enter your Earthdata access token
        access_token = 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6InJpZGhhZmF0b255MDAiLCJleHAiOjE3NDY3MzgxNDMsImlhdCI6MTc0MTU1NDE0MywiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292IiwiaWRlbnRpdHlfcHJvdmlkZXIiOiJlZGxfb3BzIiwiYWNyIjoiZWRsIiwiYXNzdXJhbmNlX2xldmVsIjozfQ.njFeiKYsfYL9ZKe_ztNFgUSaVTdnSL729QQR6IqACDlD2vD_bBulLAqEdKZ4eC6aDJbuN03drqk3DyA2CfFrdu1chHOETJHK3pDzh_b2ugW9Ctt0lcllM55aGtFZl2xdDptp1ipFsIE9IHWgrBvY9Fw88AJ7CbhUBYVDPpa3Sc9ylwFDrPNeNJkF2YZFGBjy4puIKjnl6ZMgt0QV20Oy4lxlL0-y-SgxuclF3aTxf69ZNgGhWia4WT9LiP0ZBNK2zSKCb4cpAk6yXbzSktkc3QsxjsSlgucDhe192alXiR98pGzMNnzzR8dMg4DhdfUP7qqpx3pbfCQjM9FPhVLnVw'
        # Extract file name from the URL
        filename = url.split('/')[-1].split('?')[0]  # More robust file name extraction
        file_path = os.path.join(save_path_year, filename)  # Specify the full path to save the file

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"File already exists: {filename}")
        else:
            # Ensure the directory exists or create it
            os.makedirs(save_path_year, exist_ok=True)

            # Download the file
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                try:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f'Successfully downloaded: {filename}')
                except IOError as e:
                    print(f'Error saving {filename}: {e}')
            else:
                print(f'Failed to download {filename}: Status code {response.status_code}')

# Example usage:
# download_merra2_cnn(2023, 2024, 11, 12, '/content/')
