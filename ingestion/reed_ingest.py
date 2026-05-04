import requests
import json
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient

STORAGE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME', 'ukjobmarketlake')
STORAGE_ACCOUNT_KEY = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY', '')
REED_API_KEY = os.environ.get('REED_API_KEY', '')

# Fallback to config file if env vars not set
if not STORAGE_ACCOUNT_KEY or not REED_API_KEY:
    try:
        import sys
        sys.path.append(r'C:\Users\ASUS\Documents\uk-job-market-pipeline')
        from config.config import AZURE_STORAGE_ACCOUNT_KEY, REED_API_KEY as REED_KEY
        STORAGE_ACCOUNT_KEY = AZURE_STORAGE_ACCOUNT_KEY
        REED_API_KEY = REED_KEY
    except:
        pass

def fetch_reed_jobs(keywords, location='UK', results_to_take=100):
    url = 'https://www.reed.co.uk/api/1.0/search'
    params = {'keywords': keywords, 'locationName': location, 'resultsToTake': results_to_take}
    response = requests.get(url, params=params, auth=(REED_API_KEY, ''))
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
    container_client.upload_blob(name=f'reed/{blob_name}', data=json_data, overwrite=True)
    print(f'Uploaded {blob_name} to Azure raw/reed/')

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    keywords_list = ['data engineer', 'data analyst', 'machine learning engineer', 'python developer', 'software engineer']
    all_jobs = []
    for keyword in keywords_list:
        print(f'Fetching Reed jobs for: {keyword}...')
        result = fetch_reed_jobs(keywords=keyword)
        if result and 'results' in result:
            jobs = result['results']
            for job in jobs:
                job['search_keyword'] = keyword
                job['ingestion_date'] = today
                job['source'] = 'reed'
            all_jobs.extend(jobs)
            print(f'  Got {len(jobs)} jobs')
    print(f'Total Reed jobs fetched: {len(all_jobs)}')
    upload_to_azure(all_jobs, f'reed_jobs_{today}.json')
    print('Reed ingestion complete!')

if __name__ == '__main__':
    main()