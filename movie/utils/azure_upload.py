import os
from azure.storage.blob import BlobServiceClient

def upload_to_azure_hls_files(folder_path, container_name="hls-videos"):
    # Initialize BlobServiceClient from the connection string
    blob_service_client = BlobServiceClient.from_connection_string(AzureMediaStorage.connection_string)
    file_urls = {}

    # Upload all files in the folder (playlist and segments)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Create the blob client
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

        # Upload the file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        # Store the URL of the uploaded file
        file_urls[filename] = f"{AZURE_BLOB_URL}{filename}"

    return file_urls