import os
import requests

def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

def main():
    models_dir = os.path.join(os.path.expanduser('~'), '.processpdfdocs', 'models')
    os.makedirs(models_dir, exist_ok=True)

    files_to_download = {
        'rotation_model.onnx': '1oQJzzD7FSvYG1rBvzOftLSbOoScazBAk',
        'table_detect_model.pt': '1MvMgipndrK50ahtyLARp9Nt3-b2qfjhS',
        'cell_detect_model.pt': '1-7rV13nkNicKNmUmelnKbTRSCRPIo-kQ',
    }

    for filename, file_id in files_to_download.items():
        destination = os.path.join(models_dir, filename)
        if not os.path.exists(destination):
            print(f"Downloading {filename}...")
            download_file_from_google_drive(file_id, destination)
        else:
            print(f"{filename} already exists, skipping download.")

if __name__ == "__main__":
    main()
