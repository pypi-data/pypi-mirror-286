import requests
import json
from urllib.parse import quote_plus, parse_qs
from .constants import BASE_URL

def upload_data(filename, data, api_key):
    encoded_filename = quote_plus(filename)
    signed_url_response = requests.get(BASE_URL + "/signed_upload_url?filename=" + encoded_filename, headers={'Authorization': f'Bearer {api_key}'})
    if signed_url_response.status_code != 200:
        raise ValueError("Failed to create signed url.")
    
    signed_url_body = json.loads(signed_url_response.text)
    signed_url = signed_url_body["signedUrl"]

    if type(data) is str:
        upload_response = requests.put(signed_url, data=data.encode('utf-8'))
    elif type(data) is dict:
        encoded_data = json.dumps(data).encode('utf-8')
        upload_response = requests.put(signed_url, data=encoded_data)
    else:
        raise ValueError("unsupported data type in upload_data")

    if upload_response.status_code != 200:
        raise ValueError("Failed to upload data")
    
    return filename

def get_data_size(data):
    if type(data) is str:
        return len(data.encode('utf-8'))
    elif type(data) is dict:
        json_data = json.dumps(data)
        return len(json_data.encode('utf-8'))
    else:
        raise ValueError("unsupported data type. Supported types: str, dict")

def download_data(filename, api_key):
    encoded_filename = quote_plus(filename)
    download_response = requests.get(BASE_URL + "/signed_download_url?filename=" + encoded_filename, headers={'Authorization': f'Bearer {api_key}'})
    if download_response.status_code != 200:
        raise ValueError("Failed to download " + filename)
    
    download_response_body = json.loads(download_response.text)
    signed_url = download_response_body["signedUrl"]

    content_response = requests.get(signed_url)
    return content_response.text


def read_source_code_as_func(source_code, func_name):
    local_env = {}
    exec(source_code, {}, local_env)

    # Return the function object from the local_env dictionary
    # The name for "scoring_rubric" should be dynamic
    return local_env[func_name]