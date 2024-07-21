import datetime
import os
import time
import polars as pl
from dotenv import dotenv_values
from fyers_apiv3 import fyersModel
from A2_loguru_and_telegram_combine import log_and_send_msg
import shutil


def get_start_date(symbol):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "last_date.txt")
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith(f"{symbol} = "):
                    last_date_str = line.split(" = ")[1]
                    last_date = datetime.datetime.strptime(last_date_str, "%Y-%m-%d").date()
                    start_date = last_date + datetime.timedelta(days=1)
                    return start_date.strftime("%Y-%m-%d")
            
            # If the symbol is not found in the file
            print(f"No last date found for symbol: {symbol}")
            return None
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except ValueError as e:
        print(f"Error reading start date for {symbol}: {e}")
        return None
    

def get_end_date():
    now = datetime.datetime.now()
    today = now.date()
    current_time = now.time()
    six_pm = datetime.time(18, 0)

    end_date = today if current_time >= six_pm else today - datetime.timedelta(days=1)
    return end_date.strftime("%Y-%m-%d")


def read_symbols():
    script_dir = os.path.dirname(__file__)
    symbols_file_path = os.path.join(script_dir, "symbols_list.txt")
    
    try:
        with open(symbols_file_path, 'r') as file:
            symbols = file.read().splitlines()
        return symbols
    except FileNotFoundError:
        raise FileNotFoundError(f"The symbols file {symbols_file_path} was not found.")


def fetch_data(fyers, symbol_eq, resolution, start_date, end_date):
    print(f"Fetching data for symbol: {symbol_eq}, resolution: {resolution}, from: {start_date}, to: {end_date}")
    
    data_eq = {
        "symbol": symbol_eq,
        "resolution": resolution,
        "date_format": "1",
        "range_from": start_date.strftime("%Y-%m-%d"),
        "range_to": end_date.strftime("%Y-%m-%d"),
        "cont_flag": "1"
    }
    try:
        historical_data = fyers.history(data_eq)
        if historical_data and 'candles' in historical_data:
            print(f"Successfully fetched {len(historical_data['candles'])} records for {symbol_eq}")
            return historical_data
        else:
            print(f"No data fetched for {symbol_eq}. API response: {historical_data}")
            return None
    except Exception as e:
        print(f"Error fetching data for {symbol_eq}: {str(e)}")
        return None

def process_data_chunk(historical_data):
    if not historical_data or 'candles' not in historical_data:
        print("No 'candles' key in the input data")
        return None

    print(f"Processing {len(historical_data['candles'])} records")
    try:
        candles_data = [
            {
                'date': datetime.datetime.fromtimestamp(row[0]),
                'open': float(row[1]),
                'high': float(row[2]),
                'low': float(row[3]),
                'close': float(row[4]),
                'volume': int(row[5])
            }
            for row in historical_data['candles']
        ]
        
        historical_df = pl.DataFrame(candles_data)
        
        if not historical_df.is_empty():
            historical_df = historical_df.sort('date')
            print("Processing completed")
            return historical_df
        else:
            print("DataFrame is empty after conversion")
            return None
    except Exception as e:
        print(f"Error processing data chunk: {str(e)}")
        return None


def save_data_to_csv(dataframe, folder_path, stock_symbol):
    if not dataframe.is_empty():
        file_path_eq = os.path.join(folder_path, f"{stock_symbol}.csv")
        try:
            # Add a 'symbol' column with the stock_symbol value
            dataframe_with_symbol = dataframe.with_columns(
                pl.lit(stock_symbol).alias('symbol')
            )
            
            # Reorder columns to put 'symbol' after 'date'
            column_order = ['date', 'symbol'] + [col for col in dataframe_with_symbol.columns if col not in ['date', 'symbol']]
            dataframe_with_symbol = dataframe_with_symbol.select(column_order)
            
            dataframe_with_symbol.write_csv(file_path_eq)
            print(f"Saved historical data for {stock_symbol} to {file_path_eq}")
        except Exception as e:
            print(f"Error saving data for {stock_symbol}: {str(e)}")
    else:
        print(f"No data to save for {stock_symbol}")


def setup_data_folder(folder_path):
    if os.path.exists(folder_path):
        import shutil
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)


def get_historical_data():
    log_and_send_msg("Started downloading Histroical Day Equity Data")
    try:
        symbols = read_symbols()
        end_date_str = get_end_date()
        resolution = "D"

        # Get the desktop path dynamically
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        folder_path = os.path.join(desktop_path, f"hist-data-{resolution}")

        # Set up the data folder
        setup_data_folder(folder_path)

        total_symbols = len(symbols)
       
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
       
        config = dotenv_values(os.path.join(os.path.dirname(__file__), "fyers.env"))
        client_id = config.get("CLIENT_ID")
        access_token = config.get("ACCESS_TOKEN")
       
        if not client_id or not access_token:
            raise ValueError("CLIENT_ID or ACCESS_TOKEN not set in fyers.env")
       
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")
       
        failed_symbols = []

        for symbol in symbols:
            try:
                start_date_str = get_start_date(symbol)
                print(start_date_str)
                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            except ValueError as e:
                print(f"Error getting start date for {symbol}: {str(e)}")
                failed_symbols.append(symbol)
                continue

            suffixes = ["-EQ", "-BE"]
            historical_data_df = pl.DataFrame()
    
            for suffix in suffixes:
                symbol_with_suffix = f"NSE:{symbol}{suffix}"
                current_start_date = start_date
        
                try:
                    while current_start_date <= end_date:
                        current_end_date = min(current_start_date + datetime.timedelta(days=99), end_date)
                        time.sleep(0.1)  # Rate limiting
                
                        historical_data = fetch_data(fyers, symbol_with_suffix, resolution, current_start_date, current_end_date)
                        processed_data = process_data_chunk(historical_data)
                
                        if processed_data is not None and not processed_data.is_empty():
                            historical_data_df = pl.concat([historical_data_df, processed_data])
                
                        if current_end_date >= end_date:
                            break
                
                        current_start_date = current_end_date + datetime.timedelta(days=1)
            
                    if not historical_data_df.is_empty():
                        # log_and_send_msg(f"Successfully downloaded data for {symbol_with_suffix} from {start_date_str} to {end_date_str}", symbol=symbol)
                        break
                    else:
                        if suffix == "-BE":  # If this was the last attempt
                            failed_symbols.append(symbol)
        
                except Exception as e:
                    if suffix == "-BE":  # If this was the last attempt
                        failed_symbols.append(symbol)
    
            if not historical_data_df.is_empty():
                historical_data_df = historical_data_df.sort('date')
                today = datetime.datetime.now().date()
                historical_data_df = historical_data_df.filter(pl.col('date').dt.date() <= today)
        
                historical_data_df = historical_data_df.with_columns(
                    pl.col('date').dt.strftime('%d-%m-%Y %H:%M:%S').alias('date')
                )
        
                save_data_to_csv(historical_data_df, folder_path, symbol)
        
        if failed_symbols:
            print(f"Failed to download data for the following symbols: {', '.join(failed_symbols)}")

        # Final log message
        print(f"Total symbols requested: {total_symbols}, Failed symbols: {len(failed_symbols)}, Failed symbol names: {', '.join(failed_symbols)}")
        
    except Exception as e:
        print(f"An error occurred in get_historical_data: {str(e)}")


# get_historical_data()
