import requests
import json
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient

STORAGE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME', 'ukjobmarketlake')
STORAGE_ACCOUNT_KEY = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY', '')
ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID', '')
ADZUNA_API_KEY = os.environ.get('ADZUNA_API_KEY', '')

# Fallback to config file if env vars not set
if not STORAGE_ACCOUNT_KEY or not ADZUNA_APP_ID:
    try:
        import sys
        sys.path.append(r'C:\Users\ASUS\Documents\uk-job-market-pipeline')
        from config.config import AZURE_STORAGE_ACCOUNT_KEY, ADZUNA_APP_ID as AZ_ID, ADZUNA_API_KEY as AZ_KEY
        STORAGE_ACCOUNT_KEY = AZURE_STORAGE_ACCOUNT_KEY
        ADZUNA_APP_ID = AZ_ID
        ADZUNA_API_KEY = AZ_KEY
    except:
        pass

def fetch_adzuna_jobs(keywords, page=1, results_per_page=50):
    url = f'https://api.adzuna.com/v1/api/jobs/gb/search/{page}'
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_API_KEY,
        'what': keywords,
        'results_per_page': results_per_page
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error {response.status_code}: {response.text}')
        return None

def upload_to_azure(data, blob_name):
    connection_string = f'DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client('raw')
    json_data = json.dumps(data, indent=2)
    container_client.upload_blob(name=f'adzuna/{blob_name}', data=json_data, overwrite=True)
    print(f'Uploaded {blob_name} to Azure raw/adzuna/')

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    keywords_list = ['data engineer', 'data analyst', 'machine learning', 'python developer', 'software engineer']
    all_jobs = []
    for keyword in keywords_list:
        print(f'Fetching Adzuna jobs for: {keyword}...')
        result = fetch_adzuna_jobs(keywords=keyword, page=1, results_per_page=50)
        if result and 'results' in result:
            jobs = result['results']
            for job in jobs:
                job['search_keyword'] = keyword
                job['ingestion_date'] = today
                job['source'] = 'adzuna'
            all_jobs.extend(jobs)
            print(f'  Got {len(jobs)} jobs')
    print(f'Total Adzuna jobs fetched: {len(all_jobs)}')
    upload_to_azure(all_jobs, f'adzuna_jobs_{today}.json')
    print('Adzuna ingestion complete!')

if __name__ == '__main__':
    main()