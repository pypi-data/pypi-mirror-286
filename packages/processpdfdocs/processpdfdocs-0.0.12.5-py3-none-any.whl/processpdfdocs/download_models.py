import os
import requests

def download_file_from_google_drive(file_id, dest_path):
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, dest_path)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, dest_path):
    CHUNK_SIZE = 32768

    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

def download_models(model_dir='models'):
    os.makedirs(model_dir, exist_ok=True)
    model_urls = {
        'rotation_model': '1oQJzzD7FSvYG1rBvzOftLSbOoScazBAk',
        'table_detect_model': '1MvMgipndrK50ahtyLARp9Nt3-b2qfjhS',
        'cell_detect_model': '1-7rV13nkNicKNmUmelnKbTRSCRPIo-kQ'
    }

    for model_name, file_id in model_urls.items():
        dest_path = os.path.join(model_dir, f'{model_name}.onnx' if model_name == 'rotation_model' else f'{model_name}.pt')
        print(f"Downloading {model_name}...")
        download_file_from_google_drive(file_id, dest_path)
        print(f"{model_name} downloaded.")