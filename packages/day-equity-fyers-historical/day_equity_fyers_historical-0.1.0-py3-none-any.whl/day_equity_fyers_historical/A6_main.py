import sys
from loguru import logger
from dotenv import dotenv_values
import pandas as pd
import traceback

# Importing from custom modules
from A2_loguru_and_telegram_combine import log_and_send_msg, measure_time
from A3_CSV_dates_symbols_name_getting import count_csv_files, extract_and_save_symbols, check_and_save_last_dates_for_symbols
from A4_historical_downloader import get_historical_data, get_end_date, get_start_date, read_symbols, fetch_data, process_data_chunk, save_data_to_csv
from A1_auth_access_and_refresh_token import generate_auth_code, generate_and_save_tokens, refresh_access_token
from A5_append_ohlc_old_and_new import append_ohlc_data


## Call the function to generate and print the auth code
# generate_auth_code()

## Call the function to generate and save tokens
# generate_and_save_tokens()



# #### Fyers has done some changes, so we cant automate acess_token, so first we need to use auth_code, after that-
# #### click on link, copy that auth code and paste on fyers.env. Run below auth_code and access_token. Automatically-
# #### it generates both access_token (1 day validity) and refresh token (15 day validity)


# #### by using refresh token-we can generate daily token, by using below function

# # Refresh access token
# #log_and_send_msg("Refreshing access token...")
# refresh_access_token()

# #### we need to calculate number of CSV files in folder, save symbols - which is needed to be paased for downloading-
# #### data via fyers, also check last date of previous data is same in all files, if yes last date will be saved

# # # Count CSV files, extract symbols, and check last dates
# # #log_and_send_msg("Processing CSV files and symbols...")
# count_csv_files()
# extract_and_save_symbols()
# check_and_save_last_dates_for_symbols()

# # #### this is main funciton to download data, default set is resolution = 1, means 1 minute data, -
# # #### if you want to different timeframe, you should change. date,symbol,OHLC,volumer will be order -
# # #### and saves hist-data-D for day timeframe data or hist-data-1m for 1 min timeframe
        
# # # Download historical data
# # #log_and_send_msg("Downloading historical data...")
# get_historical_data()

# # #### append both old and new files historical files
        
# # # # Append old and new historical files
# # # #log_and_send_msg("Appending old and new historical data...")
# old_folder = r"C:\Users\ravin\Desktop\DAY timeframe Data NSE 850"
# new_folder = r"C:\Users\ravin\Desktop\hist-data-D"
# results = append_ohlc_data(old_folder, new_folder)

def day_equity_histroical():
    refresh_access_token()
    count_csv_files()
    extract_and_save_symbols()
    check_and_save_last_dates_for_symbols()
    get_historical_data()
    old_folder = r"C:\Users\ravin\Desktop\DAY timeframe Data NSE 850"
    new_folder = r"C:\Users\ravin\Desktop\hist-data-D"
    append_ohlc_data(old_folder, new_folder)

if __name__ == "__main__":
    day_equity_histroical()