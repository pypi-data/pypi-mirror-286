from fyers_apiv3 import fyersModel
from dotenv import dotenv_values
import os

def generate_auth_code():
    # Load environment variables from fyers.env file in the same directory
    config = dotenv_values(os.path.join(os.path.dirname(__file__), "fyers.env"))

    # Retrieve credentials from environment variables
    client_id = config.get("CLIENT_ID")
    secret_key = config.get("SECRET_KEY")
    redirect_uri = config.get("REDIRECT_URI")
    response_type = config.get("RESPONSE_TYPE")
    state = config.get("STATE")

    # Create a session model with the provided credentials
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type
    )

    # Generate the auth code using the session model
    response = session.generate_authcode()

    # Print the auth code received in the response
    print(response)

# Call the function to open link to get auth code and copy it and paste in fyers.env
# generate_auth_code()





import os
from datetime import datetime
from loguru import logger
from fyers_apiv3 import fyersModel
from dotenv import dotenv_values

def generate_and_save_tokens():
    try:
        # Load environment variables from fyers.env file in the same directory
        env_path = os.path.join(os.path.dirname(__file__), "fyers.env")
        config = dotenv_values(env_path)

        # Retrieve credentials from environment variables
        client_id = config.get("CLIENT_ID")
        secret_key = config.get("SECRET_KEY")
        redirect_uri = config.get("REDIRECT_URI")
        response_type = config.get("RESPONSE_TYPE")
        state = config.get("STATE")
        grant_type = config.get("GRANT_TYPE")
        auth_code = config.get("FYERS_AUTH_CODE")

        # Validate required environment variables
        if not all([client_id, secret_key, redirect_uri, response_type, state, grant_type, auth_code]):
            raise ValueError("Missing required environment variables")

        # Create a session object to handle the Fyers API authentication and token generation
        session = fyersModel.SessionModel(
            client_id=client_id,
            secret_key=secret_key, 
            redirect_uri=redirect_uri, 
            response_type=response_type, 
            grant_type=grant_type
        )

        # Set the authorization code in the session object
        session.set_token(auth_code)

        # Generate the access token using the authorization code
        response = session.generate_token()

        # Extract access token and refresh token from the response
        access_token = response.get("access_token")
        refresh_token = response.get("refresh_token")

        # Get current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log the tokens and creation time for verification
        logger.info(f"Access Token: {access_token}")
        logger.info(f"Refresh Token: {refresh_token}")
        logger.info(f"Tokens created at: {current_time}")

        # Update the fyers.env file with the new tokens and creation time without quotes
        with open(env_path, 'r') as file:
            lines = file.readlines()

        with open(env_path, 'w') as file:
            for line in lines:
                if line.startswith("ACCESS_TOKEN="):
                    line = f"ACCESS_TOKEN={access_token}\n"
                elif line.startswith("REFRESH_TOKEN="):
                    line = f"REFRESH_TOKEN={refresh_token}\n"
                elif line.startswith("ACCESS_TOKEN_CREATED_AT="):
                    line = f"ACCESS_TOKEN_CREATED_AT={current_time}\n"
                elif line.startswith("REFRESH_TOKEN_CREATED_AT="):
                    line = f"REFRESH_TOKEN_CREATED_AT={current_time}\n"
                file.write(line)

        logger.info("Tokens and creation time saved to fyers.env file without quotes.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

# Call the function to get and save the access token
# generate_and_save_tokens()





import os
import sys
import requests
from datetime import datetime, timedelta
from loguru import logger
from dotenv import dotenv_values
import hashlib
import pandas as pd
from A2_loguru_and_telegram_combine import measure_time, log_and_send_msg

def load_env_config(env_path):
    """
    Load environment variables from the specified .env file.
    
    :param env_path: Path to the .env file
    :return: Dictionary containing environment variables
    """ 
    env_path = os.path.join(os.path.dirname(__file__), "fyers.env")
    return dotenv_values(env_path)

def validate_env_vars(config):
    """
    Validate that all required environment variables are present.
    
    :param config: Dictionary containing environment variables
    :return: True if all required variables are present, otherwise raises ValueError
    """
    required_vars = ["REFRESH_TOKEN", "REFRESH_TOKEN_CREATED_AT", "PIN", "CLIENT_ID", "SECRET_KEY"]
    if not all(var in config for var in required_vars):
        raise ValueError("Missing required environment variables")
    return True

def check_refresh_token_validity(refresh_token_created_at):
    """
    Check if the refresh token is still valid (within 15 days).
    
    :param refresh_token_created_at: Timestamp when the refresh token was created
    :return: True if the refresh token is valid, otherwise raises ValueError
    """
    refresh_token_created_at_dt = datetime.strptime(refresh_token_created_at, "%Y-%m-%d %H:%M:%S")
    if datetime.now() > refresh_token_created_at_dt + timedelta(days=15):
        raise ValueError("Refresh token has expired")
    return True

def calculate_remaining_validity(refresh_token_created_at):
    """
    Calculate the remaining days of validity for the refresh token.
    
    :param refresh_token_created_at: Timestamp when the refresh token was created
    :return: Number of days remaining before the refresh token expires
    """
    refresh_token_created_at_dt = datetime.strptime(refresh_token_created_at, "%Y-%m-%d %H:%M:%S")
    validity_end_date = refresh_token_created_at_dt + timedelta(days=15)
    remaining_days = (validity_end_date - datetime.now()).days
    return remaining_days

def generate_app_id_hash(client_id, secret_key):
    """
    Generate a SHA-256 hash using the client_id and secret_key.
    
    :param client_id: Client ID for the application
    :param secret_key: Secret key for the application
    :return: SHA-256 hash of the combined client_id and secret_key
    """
    combined = f"{client_id}:{secret_key}"
    app_id_hash = hashlib.sha256(combined.encode()).hexdigest()
    return app_id_hash

def make_refresh_request(refresh_token, app_id_hash, pin):
    """
    Make a POST request to refresh the access token.
    
    :param refresh_token: Current refresh token
    :param app_id_hash: SHA-256 hash of the client_id and secret_key
    :param pin: User's PIN
    :return: New access token
    """
    url = "https://api-t1.fyers.in/api/v3/validate-refresh-token"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "refresh_token",
        "appIdHash": app_id_hash,
        "refresh_token": refresh_token,
        "pin": pin
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json().get("access_token")

def update_env_file(env_path, new_access_token):
    """
    Update the .env file with the new access token and the current timestamp.
    
    :param env_path: Path to the .env file
    :param new_access_token: New access token
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(env_path, 'r') as file:
        lines = file.readlines()

    with open(env_path, 'w') as file:
        for line in lines:
            if line.startswith("ACCESS_TOKEN="):
                line = f"ACCESS_TOKEN={new_access_token}\n"
            elif line.startswith("ACCESS_TOKEN_CREATED_AT="):
                line = f"ACCESS_TOKEN_CREATED_AT={current_time}\n"
            file.write(line)
            

def refresh_access_token():
    """
    Main function to refresh the access token.
    """
    env_path = os.path.join(os.path.dirname(__file__), "fyers.env")
    config = load_env_config(env_path)
    if validate_env_vars(config):
        refresh_token = config["REFRESH_TOKEN"]
        refresh_token_created_at = config["REFRESH_TOKEN_CREATED_AT"]
        pin = config["PIN"]
        client_id = config["CLIENT_ID"]
        secret_key = config["SECRET_KEY"]

        app_id_hash = generate_app_id_hash(client_id, secret_key)
        remaining_days = calculate_remaining_validity(refresh_token_created_at)
        log_and_send_msg(f"Fyers refresh token has {remaining_days} days remaining before expiry.")

        if check_refresh_token_validity(refresh_token_created_at):
            try:
                new_access_token = make_refresh_request(refresh_token, app_id_hash, pin)
                update_env_file(env_path, new_access_token)
                log_and_send_msg("Fyers new Access Token and creation time saved to fyers.env file without quotes.")
            except requests.exceptions.HTTPError as e:
                log_and_send_msg(f"An HTTP error occurred: {e}")
            except Exception as e:
                log_and_send_msg(f"An error occurred: {e}")

# Call the function to refresh the access token
# refresh_access_token()