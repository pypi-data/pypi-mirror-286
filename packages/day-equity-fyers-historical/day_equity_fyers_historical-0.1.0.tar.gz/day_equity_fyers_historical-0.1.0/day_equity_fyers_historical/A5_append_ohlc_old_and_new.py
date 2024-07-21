import os
import polars as pl
import shutil
from datetime import datetime, timedelta
from A2_loguru_and_telegram_combine import log_and_send_msg

def append_ohlc_data(old_folder_path, new_folder_path):
    results = {}
    old_files = os.listdir(old_folder_path)
    new_files = os.listdir(new_folder_path)
    
    total_files = len(old_files)
    processed_files = 0
    success_count = 0
    failure_count = 0
    failure_files = []
   
    for file in old_files:
        processed_files += 1
        print(f"Processing file {processed_files}/{total_files}: {file}")
        
        if file in new_files:
            old_data_path = os.path.join(old_folder_path, file)
            new_data_path = os.path.join(new_folder_path, file)
           
            # Create a backup of the old file
            backup_path = old_data_path + '.bak'
            try:
                shutil.copy2(old_data_path, backup_path)
            except OSError as e:
                results[file] = {'status': 'failure', 'reason': f'Backup creation failed: {str(e)}'}
                failure_count += 1
                failure_files.append(file)
                print(f"Failed to create backup for {file}: {str(e)}")
                continue
           
            try:
                # Process the stock data
                result = process_stock_data(old_data_path, new_data_path)
                results[file] = result
                
                if result['status'] == 'success':
                    success_count += 1
                    os.remove(backup_path)  # Remove backup
                    os.remove(new_data_path)  # Remove new file after successful append
                    print(f"Successfully appended data for {file}")
                else:  # failure
                    failure_count += 1
                    failure_files.append(file)
                    print(f"Failed to append data for {file}: {result['reason']}")
                    # Restore from backup if processing failed
                    shutil.copy2(backup_path, old_data_path)
                    os.remove(backup_path)
                    # Note: We keep the new file in case of failure
                
            except Exception as e:
                results[file] = {'status': 'failure', 'reason': f'Processing failed: {str(e)}'}
                failure_count += 1
                failure_files.append(file)
                print(f"Exception occurred while processing {file}: {str(e)}")
                
                # Restore from backup if processing failed
                shutil.copy2(backup_path, old_data_path)
                os.remove(backup_path)
                # Note: We keep the new file in case of exception
        else:
            results[file] = {'status': 'no_new_data'}
            print(f"No new data for {file}")
   
    # Generate summary log
    with open('append_summary.log', 'w') as f:
        for file, result in results.items():
            f.write(f"{file}: {result}\n")
   
    # Print final summary
    print("\nProcessing complete!")
    log_and_send_msg("\nAppend Processing complete!")
    print(f"Total files processed: {total_files}")
    log_and_send_msg(f"Total files processed: {total_files}")
    print(f"Successful appends: {success_count}")
    log_and_send_msg(f"Successful appends: {success_count}")
    print(f"Failures: {failure_count}")
    log_and_send_msg(f"Failures: {failure_count}")
    
    if failure_count > 0:
        print("\nFiles that failed:")
        log_and_send_msg("\nFiles that failed:")
        for file in failure_files:
            print(f"- {file}: {results[file]['reason']}")
            log_and_send_msg(f"- {file}: {results[file]['reason']}")

    return results


def process_stock_data(old_data_path, new_data_path):
    try:
        old_data = pl.read_csv(old_data_path, separator=',', ignore_errors=True)
        new_data = pl.read_csv(new_data_path, separator=',', ignore_errors=True)
    except Exception as e:
        return {'status': 'failure', 'reason': f'Error reading CSV: {str(e)}'}
    
    # Check if columns match
    if old_data.columns != new_data.columns:
        return {'status': 'failure', 'reason': 'columns_mismatch'}
    
    # Check if 'date' column exists
    if 'date' not in old_data.columns or 'date' not in new_data.columns:
        return {'status': 'failure', 'reason': 'date_column_missing'}
    
    # Convert 'date' column to datetime
    try:
        old_data = old_data.with_columns(pl.col('date').str.strptime(pl.Datetime, '%d-%m-%Y %H:%M:%S'))
        new_data = new_data.with_columns(pl.col('date').str.strptime(pl.Datetime, '%d-%m-%Y %H:%M:%S'))
    except Exception as e:
        return {'status': 'failure', 'reason': f'Error converting date: {str(e)}'}
    
    # Verify chronological order
    if not (old_data['date'].is_sorted() and new_data['date'].is_sorted()):
        return {'status': 'failure', 'reason': 'data_not_chronological'}
    
    # Check for data continuity
    old_last_date = old_data['date'].max()
    new_first_date = new_data['date'].min()
    date_gap = new_first_date - old_last_date
    
    # Allow for up to 3 days gap to account for weekends and possibly holidays
    if date_gap > timedelta(days=3):
        return {'status': 'warning', 'reason': 'data_gap', 'gap': str(date_gap)}
    
    # Verify data types
    expected_dtypes = {'open': pl.Float64, 'high': pl.Float64, 'low': pl.Float64, 'close': pl.Float64, 'volume': pl.Int64}
    for col, dtype in expected_dtypes.items():
        if old_data[col].dtype != dtype or new_data[col].dtype != dtype:
            return {'status': 'failure', 'reason': f'incorrect_dtype_{col}'}
    
    # Check for extreme values
    for col in ['open', 'high', 'low', 'close']:
        old_mean, old_std = old_data[col].mean(), old_data[col].std()
        new_mean, new_std = new_data[col].mean(), new_data[col].std()
        if abs(new_mean - old_mean) > 10 * old_std:
            print(f"Extreme values found in {col}, but continuing with append")
    
    old_data_rows = old_data.shape[0]
    new_data_rows = new_data.shape[0]
    
    appended_data = pl.concat([old_data, new_data]).sort('date').unique(subset=['date'])
    
    appended_data_rows = appended_data.shape[0]
    
    # Calculate expected rows after append
    expected_rows = old_data_rows + new_data_rows
    
    if appended_data_rows >= old_data_rows:
        # Convert 'date' back to string before saving
        appended_data = appended_data.with_columns(pl.col('date').dt.strftime('%d-%m-%Y %H:%M:%S'))
        appended_data.write_csv(old_data_path, separator=',')
        return {
            'status': 'success',
            'old_rows': old_data_rows,
            'new_rows': new_data_rows,
            'appended_rows': appended_data_rows,
            'expected_rows': expected_rows,
            'duplicate_rows': expected_rows - appended_data_rows
        }
    else:
        return {
            'status': 'failure',
            'reason': 'unexpected_row_count',
            'old_rows': old_data_rows,
            'new_rows': new_data_rows,
            'appended_rows': appended_data_rows,
            'expected_rows': expected_rows
        }