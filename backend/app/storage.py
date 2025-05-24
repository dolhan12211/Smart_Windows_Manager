from azure.storage.blob.aio import BlobServiceClient
import os
import json

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "smart-data"

async def save_to_blob(blob_name, data):
    container_client = blob_service_client.get_container_client(container_name)
    try:
        await container_client.create_container()
    except:
        pass
    blob_client = container_client.get_blob_client(blob_name)
    await blob_client.upload_blob(json.dumps(data), overwrite=True)