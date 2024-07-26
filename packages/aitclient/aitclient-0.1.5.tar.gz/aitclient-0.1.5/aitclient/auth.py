import requests, logging, os, base64, urllib3
from datetime import datetime

# Configure logging to log to a file with a specific format and level
logging.basicConfig(filename='log.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)

# Disable warnings about insecure requests (e.g., unverified HTTPS requests)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def aitAUTH(client_id, client_secret, tenant_id, AIT_Development=False):
    """
    Authenticate with the AIT service and obtain an access token.

    Parameters:
    client_id (str): The client ID for authentication.
    client_secret (str): The client secret for authentication.
    tenant_id (str): The tenant ID for authentication.
    AIT_Development (bool): Flag to indicate if the development environment should be used.

    Returns:
    Response: The response object containing the access token if authentication is successful.
    """

    print('------------------------------------')

    # ANSI escape code for underlining text
    underline_start = "\033[4m"
    underline_end = "\033[0m"

    # Prepare the data payload for the authentication request
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "tenant_id": tenant_id
    }

    # Prepare the headers for the authentication request
    headers = {
        "client-id": client_id,
        "client-secret": client_secret,
        "tenant-id": tenant_id
    }

    # Define the authentication URLs for production and development environments
    authentication_dev = "https://aitdev.ari.only.sap/api/token"
    authentication = "https://ait.ari.only.sap/api/token"

    # Use the development URL if the AIT_Development flag is set
    if AIT_Development:
        authentication = authentication_dev
        print(f'{underline_start}AIT Development Environment{underline_end}')

    # Check if the authentication URL is active
    try:
        response = requests.head(authentication, verify=False)  # Using HEAD for a lightweight check
        if response.status_code in [200, 204]:
            logging.debug(f'URL {authentication} is active.')
        else:
            print(f'URL {authentication} is not active. Status code: {response.status_code}')
            logging.error(f'URL {authentication} is not active. Status code: {response.status_code}')
            exit()
    except requests.ConnectionError:
        print(f'Failed to connect to {authentication}')
        logging.error(f'Failed to connect to {authentication}')
        exit()

    # Log the authentication URL and data payload
    logging.debug(f'Auth URL: {authentication} / json: {data}')

    # Send the POST request to obtain the access token
    access_token_response = requests.post(authentication, json=data, headers=headers)
    logging.debug(f'Response: {access_token_response}')

    # Check if the authentication was successful
    if access_token_response.status_code == 200:
        # Extract the access token from the response
        access_token = access_token_response.json()['access_token']
        logging.debug(f'Access Token: {access_token}')
        logging.info('Authentication Successful')
        print('Authentication Successful')
        return access_token_response
    else:
        # Log an error if authentication failed
        logging.error(f'{access_token_response.json()}')