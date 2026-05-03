import os
import sys
sys.path.append(r'C:\Users\ASUS\Documents\uk-job-market-pipeline')
from azure.storage.blob import BlobServiceClient
from config.config import AZURE_STORAGE_ACCOUNT_NAME, AZURE_STORAGE_ACCOUNT_KEY, AZURE_CONTAINER_RAW, KAGGLE_DATA_PATH

def upload_file_to_azure(file_path, blob_name):
    connection_string = f'DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT_NAME};AccountKey={AZURE_STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_RAW)
    print(f'Uploading {blob_name}...')
    with open(file_path, 'rb') as data:
        container_client.upload_blob(name=f'kaggle/{blob_name}', data=data, overwrite=True)
    print(f'Successfully uploaded {blob_name}')

def main():
    # job_summary.csv excluded - too large (5GB), not needed for pipeline
    files = [
        'linkedin_job_postings.csv',
        'job_skills.csv'
    ]
    for file_name in files:
        file_path = os.path.join(KAGGLE_DATA_PATH, file_name)
        if os.path.exists(file_path):
            upload_file_to_azure(file_path, file_name)
        else:
            print(f'WARNING: {file_name} not found at {file_path}')
    print('Kaggle ingestion complete!')

if __name__ == '__main__':
    main()