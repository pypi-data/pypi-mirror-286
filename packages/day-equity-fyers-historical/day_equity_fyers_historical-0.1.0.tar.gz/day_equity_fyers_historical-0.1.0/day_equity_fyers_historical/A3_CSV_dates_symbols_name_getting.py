import os
from dotenv import dotenv_values, load_dotenv
from A2_loguru_and_telegram_combine import log_and_send_msg,measure_time
from time import perf_counter
import csv
from datetime import datetime
import polars as pl
import sys

def load_env_config():
    """
    Load environment variables from the fyers.env file located in the same directory.
    
    :return: Dictionary containing environment variables
    """ 
    env_path = os.path.join(os.path.dirname(__file__), "fyers.env")
    load_dotenv(dotenv_path=env_path)


def count_csv_files():
    """
    Count the total number of CSV files in the folder specified by the environment variable.
    :return: Total number of CSV files in the folder.
    """
    # Load environment variables from fyers.env file
    load_env_config()
   
    # Retrieve the folder path from the environment variable
    folder_path = os.getenv('OLD_DAY_HISTORICAL_CSV_FOLDER_PATH')
   
    if not folder_path:
        raise ValueError("Environment variable 'OLD_DAY_HISTORICAL_CSV_FOLDER_PATH' is not set in fyers.env.")
   
    # List all files in the directory
    try:
        files = os.listdir(folder_path)
    except Exception as e:
        raise Exception(f"Failed to list files in directory: {folder_path}. Error: {e}")
   
    # Filter out the CSV files
    csv_files = [file for file in files if file.endswith('.csv')]
    
    
    # Log all information in a single call
    log_and_send_msg(
        f"CSV file count completed. "
        f"Folder path: {folder_path}. "
        f"Found {len(csv_files)} CSV files. "
    )
   
    # Return the total number of CSV files
    return len(csv_files)

#### Run the function
# count_csv_files()



def extract_and_save_symbols():
    """
    Extract symbols from CSV file names in the specified folder,
    and return them as a list.
    """
    # Load environment variables
    load_env_config()
    
    # Retrieve the folder path from the environment variable
    folder_path = os.getenv('OLD_DAY_HISTORICAL_CSV_FOLDER_PATH')
    
    if not folder_path:
        raise ValueError("Environment variable 'OLD_DAY_HISTORICAL_CSV_FOLDER_PATH' is not set in fyers.env.")
    
    try:
        # List all files in the directory
        files = os.listdir(folder_path)
        
        # Filter CSV files and extract symbols
        symbols = [os.path.splitext(file)[0] for file in files if file.endswith('.csv')]
        
        # Sort symbols alphabetically
        symbols.sort()
        
        log_and_send_msg(
            f"Symbols extraction completed. "
            f"Total symbols extracted: {len(symbols)}. "
            f"First 5 symbols: {', '.join(symbols[:5])}..."
        )
        
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, "symbols_list.txt")
        
        # Save symbols to a text file in the specified directory
        with open(file_path, "w") as txtfile:
            for symbol in symbols:
                txtfile.write(f"{symbol}\n")  # Write each symbol on a new line without quotes or comma
        
        print(f"Symbols saved to {file_path}")
        
        return symbols
    
    except Exception as e:
        error_msg = f"Error processing symbols: {str(e)}"
        log_and_send_msg(error_msg)
        raise

# ### Run the function
# symbols = extract_and_save_symbols()
# print(symbols)


def check_and_save_last_dates_for_symbols():
    sys.stdout.reconfigure(encoding='utf-8')
   
    load_env_config()
    folder_path = os.getenv('OLD_DAY_HISTORICAL_CSV_FOLDER_PATH')
   
    if not folder_path:
        raise ValueError("Environment variable 'OLD_DAY_HISTORICAL_CSV_FOLDER_PATH' is not set in fyers.env.")
   
    print(f"\nReading files from folder: {folder_path}")
   
    try:
        all_files = os.listdir(folder_path)
        csv_files = [f for f in all_files if f.endswith('.csv')]
        print(f"Total files in folder: {len(all_files)}")
        print(f"Total CSV files in folder: {len(csv_files)}")
    except Exception as e:
        raise Exception(f"Failed to list files in directory: {folder_path}. Error: {e}")
   
    last_dates = {}
    processed_files = 0
    skipped_files = 0
   
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        symbol = os.path.splitext(csv_file)[0]  # Get symbol name from file name
        try:
            df = pl.read_csv(file_path, encoding='utf-8')
            print(f"\nProcessing {csv_file}:")
            print(f"Shape: {df.shape}")
            print(f"Columns: {df.columns}")
           
            if 'date' not in df.columns:
                print(f"Warning: 'date' column not found in {csv_file}. Skipping this file.")
                skipped_files += 1
                continue
           
            date_formats = ['%Y-%m-%d %H:%M:%S', '%d-%m-%Y %H:%M', '%d-%m-%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S']
            for date_format in date_formats:
                try:
                    df = df.with_columns(pl.col('date').str.strptime(pl.Datetime, date_format))
                    break
                except:
                    continue
            else:
                print(f"Error: Unable to parse date in {csv_file}. Skipping this file.")
                skipped_files += 1
                continue
           
            last_date = df['date'].to_list()[-1]
            last_dates[symbol] = last_date.strftime('%Y-%m-%d')
           
            print(f"Last date for {symbol}: {last_dates[symbol]}")
            processed_files += 1
           
        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")
            skipped_files += 1
            continue
   
    print(f"\nProcessed files: {processed_files}")
    print(f"Skipped files: {skipped_files}")
   
     # Use os.path.dirname(__file__) to get the current script's directory
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "last_date.txt")
   
    with open(file_path, "w") as txtfile:
        for symbol, date in last_dates.items():
            txtfile.write(f"{symbol} = {date}\n")
   
    print(f"\nLast dates for all symbols saved to {file_path}")
   
 
   
    log_and_send_msg(
        f"CSV file processing completed. "
        f"Folder path: {folder_path}. "
        f"Total files: {len(all_files)}. "
        f"CSV files: {len(csv_files)}. "
        f"Processed: {processed_files}. "
        f"Skipped: {skipped_files}. "
    )

# Run this function
# check_and_save_last_dates_for_symbols()