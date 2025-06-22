import requests
from apideck_unify import Apideck


def fetch_file_list(api_key, app_id, consumer_id, service_id="box"):
    """Fetches a list of files from the specified service."""
    try:
        with Apideck(
            api_key=api_key, app_id=app_id, consumer_id=consumer_id
        ) as apideck:
            response = apideck.file_storage.files.list(service_id=service_id)
            if response.get_files_response and response.get_files_response.data:
                return response.get_files_response.data
            else:
                print("No files found or an issue occurred.")
                return []
    except Exception as e:
        print(f"An error occurred while fetching file list: {e}")
        return []


def download_file(file_id, file_name, api_key, app_id, consumer_id, service_id="box"):
    """Downloads a specific file and saves it locally."""
    try:
        download_url = (
            f"https://unify.apideck.com/file-storage/files/{file_id}/download"
        )
        headers = {
            "Authorization": f"Bearer {api_key}",
            "x-apideck-app-id": app_id,
            "x-apideck-consumer-id": consumer_id,
            "x-apideck-service-id": service_id,
        }

        response = requests.get(download_url, headers=headers, allow_redirects=True)
        response.raise_for_status()

        with open(file_name, "wb") as f:
            f.write(response.content)

        print(f"Successfully downloaded '{file_name}'")
        return file_name

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during download: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
