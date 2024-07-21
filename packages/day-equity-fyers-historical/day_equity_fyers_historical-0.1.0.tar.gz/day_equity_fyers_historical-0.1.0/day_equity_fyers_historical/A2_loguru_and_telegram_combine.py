
import os
import requests
from dotenv import dotenv_values, set_key

def load_env_config():
    """
    Load environment variables from the .env file located in the same directory as the script.
    
    :return: Dictionary containing environment variables
    """
    env_path = os.path.join(os.path.dirname(__file__), "fyers.env")
    return dotenv_values(env_path)

def save_env_config(config):
    """
    Save environment variables to the .env file located in the same directory as the script.
    
    :param config: Dictionary containing environment variables
    """
    env_path = os.path.join(os.path.dirname(__file__), "fyers.env")
    with open(env_path, 'w') as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")

def get_chat_id():
    """
    Get the chat ID for a Telegram bot using the TELEGRAM_API token from the .env file.
    
    :return: Chat ID or None if not found
    """
    config = load_env_config()
    bot_token = config.get("TELEGRAM_API")
    if not bot_token:
        raise ValueError("TELEGRAM_API environment variable is not set")
    
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    
    updates = response.json()
    print("Updates Response:", updates)  # Debugging statement
    
    if updates['ok'] and updates['result']:
        for update in updates['result']:
            chat_id = update['message']['chat']['id']
            print(f"Found Chat ID: {chat_id}")  # Debugging statement
            
            # Update the config dictionary with the chat_id
            config['TELEGRAM_CHAT_ID'] = str(chat_id)
            save_env_config(config)  # Save the updated config to the .env file
            
            return chat_id
    
    return None

# Example usage

# chat_id = get_chat_id()
# if chat_id:
    # print(f"Chat ID: {chat_id}")
# else:
    # print("No chat ID found.")
    




import os
from time import perf_counter
import requests
from dotenv import dotenv_values

def load_env_config():
    """
    Load environment variables from the .env file located in the same directory as the script.
    
    :return: Dictionary containing environment variables
    """
    env_path = os.path.join(os.path.dirname(__file__), "fyers.env")
    return dotenv_values(env_path)

def send_telegram_message(message):
    """
    Send a message to a Telegram chat.
    
    :param chat_id: Telegram chat ID
    :param message: Message to send
    """
    config = load_env_config()
    token = config.get("TELEGRAM_API")
    chat_id = config.get("TELEGRAM_CHAT_ID")
    if not token:
        raise ValueError("TELEGRAM_API environment variable is not set")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    return response.json()

# message = "Hello, this is a test message!"
# response = send_telegram_message(message)
# print("Message sent successfully:", response)




import os
import sys
from datetime import datetime
from loguru import logger

# Get the directory of the current script
current_script_directory = os.path.dirname(__file__)

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Set the log directory to the same directory as the script
log_directory = os.path.join(current_script_directory, "Logs")
os.makedirs(log_directory, exist_ok=True)  # Ensure the directory exists

# Set the CSV log file path
csv_path = os.path.join(log_directory, f"logs_{current_date}.csv")

def custom_format(record):
    return "{time},{level},{message}\n".format(
        time=record["time"].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        level=record["level"].name,
        message=record["message"]
    )

# Configure loguru once
logger.remove()  # Remove default handler
logger.add(sink=sys.stdout, level="DEBUG", colorize=True, 
           format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{level: <8}</level> <blue>{message}</blue>")
logger.add(sink=csv_path, level="DEBUG", format=custom_format, 
           rotation="50 MB", retention="10 days", mode="a")

def log_and_send_msg(message, time_taken=None, symbol=None, order=None, ordertype=None, broker=None, **kwargs):
    detailed_message = message
    extras = []
    
    if time_taken is not None:
        extras.append(f"Time Taken: {time_taken:.3f} ms")
    if symbol is not None:
        extras.append(f"Symbol: {symbol}")
    if order is not None:
        extras.append(f"Order: {order}")
    if ordertype is not None:
        extras.append(f"Ordertype: {ordertype}")
    if broker is not None:
        extras.append(f"Broker: {broker}")
    for key, value in kwargs.items():
        extras.append(f"{key}: {value}")
    
    if extras:
        detailed_message += ", " + ", ".join(extras)
    
    logger.info(detailed_message)
    send_telegram_message(detailed_message)

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        time_taken = (end_time - start_time) * 1000  # Convert to milliseconds
        log_and_send_msg(f"Function executed: {func.__name__}", time_taken=time_taken)
        return result
    return wrapper