import logging
import os
import time # Import the time module
from logging.handlers import RotatingFileHandler
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Define the log file path for local fallback
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'action_log.txt')

# Azure Blob Storage configuration
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "action-logs" # You might want to make this configurable
BLOB_NAME = "smart-windows-manager-actions.log" # Single blob for all logs

# Initialize Azure Blob Service Client
blob_service_client = None
blob_client = None # Initialize blob_client here as well

print(f"DEBUG: CONNECTION_STRING loaded: {'<present>' if CONNECTION_STRING else '<missing>'}")

if CONNECTION_STRING:
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        print("DEBUG: BlobServiceClient initialized.")
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        try:
            container_client.create_container()
            print(f"DEBUG: Container '{CONTAINER_NAME}' created.")
        except Exception as e:
            if "ContainerAlreadyExists" not in str(e):
                print(f"DEBUG: Container '{CONTAINER_NAME}' already exists or other error: {e}")
            else:
                print(f"DEBUG: Container '{CONTAINER_NAME}' already exists.")
        
        # Get the append blob client
        blob_client = container_client.get_blob_client(BLOB_NAME)
        print(f"DEBUG: BlobClient for '{BLOB_NAME}' obtained.")
        try:
            # Create the append blob if it doesn't exist
            blob_client.create_append_blob()
            print(f"DEBUG: Append blob '{BLOB_NAME}' created.")
        except Exception as e:
            if "BlobAlreadyExists" not in str(e):
                print(f"DEBUG: Append blob '{BLOB_NAME}' already exists or other error: {e}")
            else:
                print(f"DEBUG: Append blob '{BLOB_NAME}' already exists.")

    except Exception as e:
        print(f"ERROR: Could not connect to Azure Blob Storage: {e}")
        blob_service_client = None # Ensure it's None if connection fails
        blob_client = None # Ensure it's None if connection fails
else:
    print("DEBUG: AZURE_STORAGE_CONNECTION_STRING is missing. Azure Blob Storage logging will be skipped.")

# Create a custom logger
action_logger = logging.getLogger('action_logger')
action_logger.setLevel(logging.INFO)

# Create file handler which logs even debug messages (fallback to local file)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024 * 5, backupCount=5) # 5 MB per file, 5 backup files
file_handler.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
formatter.converter = time.gmtime # Use UTC time for logging

# Add the file handler to the logger
action_logger.addHandler(file_handler)

# Prevent the logger from passing messages to the root logger
action_logger.propagate = False

def log_action(message: str):
    # Create a LogRecord manually to ensure the logger name is included in the formatted message for Azure
    record = logging.LogRecord('action_logger', logging.INFO, '', 0, message, [], None)
    # Use the same formatter as the file_handler for consistency
    formatted_log_line = f"{formatter.format(record)}\n"
    
    # Log to local file
    action_logger.info(message)

    # Log to Azure Blob Storage if connected
    # Log to Azure Blob Storage if connected and blob_client is initialized
    if blob_client: # Check blob_client directly
        try:
            encoded_message = formatted_log_line.encode('utf-8')
            # print(f"Attempting to append {len(encoded_message)} bytes to Azure Blob Storage.") # Removed diagnostic print
            blob_client.append_block(encoded_message)
            # print(f"Successfully appended {len(encoded_message)} bytes to Azure Blob Storage.") # Removed diagnostic print
        except Exception as e:
            print(f"ERROR: Failed to upload log to Azure Blob Storage: {e}")
            # Fallback to local logging if Azure upload fails
            action_logger.error(f"Failed to upload log to Azure Blob Storage: {e} - Message: {message}")
