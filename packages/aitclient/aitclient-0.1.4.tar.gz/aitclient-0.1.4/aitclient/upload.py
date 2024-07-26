import requests, logging, os, base64, shutil
from datetime import datetime

logging.basicConfig(filename='log.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)

def aitPOST(access_token_response, directory_path, file_type, project):

    """
    Upload files to the AIT service.

    Parameters:
    access_token_response (Response): The response object containing the access token and upload URL.
    directory_path (str): The path to the directory containing the files to upload.
    file_type (str): The type of files to upload (e.g., 'json', 'xls').
    project (str): The project name associated with the files.

    Returns:
    None
    """


    print('------------------------------------')

    #Extract the access token and upload URL from the response
    access_token = access_token_response.json()['access_token']
    api_url = access_token_response.json()['upload_url']

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    logging.debug(f'API: {api_url} / Headers: {headers}')

    # Create an archive directory if it doesn't exist
    archive_dir = os.path.join(directory_path, 'archive')
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    files_list = []
    count = 0
    status = ''

    # Iterate over the files in the directory
    for file_name in os.listdir(directory_path):
        # Process JSON Files
        if file_type == 'json' and file_name.endswith('.json'):
            with open(os.path.join(directory_path, file_name), 'rb') as file:
                count += 1
                binary_data = file.read()
                content_bytes = base64.b64encode(binary_data).decode('utf-8')
                file_metadata = {
                    'file_name': file_name,
                    'file': content_bytes,
                    'project': project
                }
                logging.debug(f'File Name: {file_name} | Directory: {directory_path}')
                response = requests.post(api_url, headers=headers, json=file_metadata)
                logging.debug(response.json())
                if response.status_code == 200:
                    logging.info(f'{count}: {file_name} Processed')
                    files_list.append(file_name)
                    status = 'Success'
                else:
                    status = f'Failed: {response.json()}'
                    print(f'Error: {response.json()}')
                    logging.error(f'Error: {response.json()}')
            if status == 'Success':
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                new_file_name = f"{os.path.splitext(file_name)[0]}_{timestamp}{os.path.splitext(file_name)[1]}"
                shutil.move(os.path.join(directory_path, file_name), os.path.join(archive_dir, new_file_name))
        # Process XLS Files
        elif file_type == 'xls' and file_name.endswith('.xls'):
            with open(os.path.join(directory_path, file_name), 'rb') as file:
                
                count = count + 1

                binary_data = file.read()

                content_bytes = base64.b64encode(binary_data).decode('utf-8')

                file_metadata = {
                    'file_name': file_name,
                    'file': content_bytes,
                    'project': project
                }
                try:
                    logging.debug(f'File Name: {file_name} | Directory: {directory_path}')
                    response = requests.post(api_url, headers=headers, json=file_metadata)
                    logging.debug(response.json())
                    if response.status_code == 200:
                        logging.info(f'{count}: {file_name} Processed')
                        print(f'{count}: {file_name} Processed')
                        files_list.append(file_name)
                        status = 'Success'
                    else:
                        status = f'Failed: {response.json()}'
                        print(f'Error: {response.json()}')
                        logging.error(f'Error: {response.json()}')
                except Exception as e:
                    logging.debug(f'Error: {e}')
            if status == 'Success':
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Format the timestamp as you need
                new_file_name = f"{os.path.splitext(file_name)[0]}_{timestamp}{os.path.splitext(file_name)[1]}"
                shutil.move(os.path.join(directory_path, file_name), os.path.join(archive_dir, new_file_name))
        # Process XLSX Files
        elif file_type.lower() == 'xlsx' and file_name.endswith('.xlsx'):
            with open(os.path.join(directory_path, file_name), 'rb') as file:
                
                count = count + 1

                binary_data = file.read()

                content_bytes = base64.b64encode(binary_data).decode('utf-8') 

                file_metadata = {
                    'file_name': file_name,
                    'file': content_bytes,
                    'project': project
                }
                try:
                    logging.debug(f'File Name: {file_name} | Directory: {directory_path}')
                    response = requests.post(api_url, headers=headers, json=file_metadata)
                    logging.debug(response.json())
                    if response.status_code == 200:
                        logging.info(f'{count}: {file_name} Processed')
                        print(f'{count}: {file_name} Processed')
                        files_list.append(file_name)
                        status = 'Success'
                    else:
                        status = f'Failed: {response.json()}'
                        print(f'Error: {response.json()}')
                        logging.error(f'Error: {response.json()}')
                except Exception as e:
                    logging.debug(f'Error: {e}')
            if status == 'Success':
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Format the timestamp as you need
                new_file_name = f"{os.path.splitext(file_name)[0]}_{timestamp}{os.path.splitext(file_name)[1]}"
                shutil.move(os.path.join(directory_path, file_name), os.path.join(archive_dir, new_file_name))
        # Process CSV Files
        elif file_type == 'csv' and file_name.endswith('.csv'):
            with open(os.path.join(directory_path, file_name), 'rb') as file:

                count = count + 1

                binary_data = file.read()

                content_bytes = base64.b64encode(binary_data).decode('utf-8')

                file_metadata = {
                    'file_name': file_name,
                    'file': content_bytes,
                    'project': project
                }
                try:
                    logging.debug(f'File Name: {file_name} | Directory: {directory_path}')
                    response = requests.post(api_url, headers=headers, json=file_metadata)
                    logging.debug(response.json())
                    if response.status_code == 200:
                        logging.info(f'{count}: {file_name} Processed')
                        print(f'{count}: {file_name} Processed')
                        files_list.append(file_name)
                    else:
                        status = f'Failed: {response.json()}'
                        print(f'Error: {response.json()['error']}')
                        logging.error(f'Error: {response.json()}')
                except Exception as e:
                    logging.debug(f'Error: {e}')
            if status == 'Success':
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Format the timestamp as you need
                new_file_name = f"{os.path.splitext(file_name)[0]}_{timestamp}{os.path.splitext(file_name)[1]}"
                shutil.move(os.path.join(directory_path, file_name), os.path.join(archive_dir, new_file_name))

    # Log the summary of processed files
    print('------------------------------------')
    logging.info(f'Total files processed: {count}')
    logging.info(f'Files successfully uploaded: {files_list}')
    print(f'Total files processed: {count}')
    print(f'Files successfully uploaded: {files_list}')