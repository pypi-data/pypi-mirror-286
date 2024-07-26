import requests, logging, os, base64, urllib3
from datetime import datetime

logging.basicConfig(filename='log.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def aitAUTH(client_id, client_secret, tenant_id, AIT_Development=False):

    print('------------------------------------')

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "tenant_id": tenant_id
    }
    headers = {
        "client-id": client_id,
        "client-secret": client_secret,
        "tenant-id": tenant_id
    }

    authentication_dev = "https://aitdev.ari.only.sap/api/token"
    authentication = "https://ait.ari.only.sap/api/token"

    if AIT_Development:
        authentication = authentication_dev
        print('AIT Development Environment')

    # Check if the authentication URL is active
    try:
        response = requests.head(authentication, verify=False)
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

    logging.debug(f'Auth URL: {authentication} / json: {data}')
    access_token_response = requests.post(authentication, json=data, headers=headers)
    logging.debug(f'Response: {access_token_response}')
    if access_token_response.status_code == 200:
        access_token = access_token_response.json()['access_token']
        logging.debug(f'Access Token: {access_token}')
        logging.info('Authentication Successful')
        print('Authentication Successful')
        return access_token_response
    else:
        logging.error(f'{access_token_response.json()}')
        print(f'Error: {access_token_response.json()}')
        exit()
