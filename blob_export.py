from data_import import import_training_data, import_test_data
from dotenv import load_dotenv
import os
from azure.storage.blob import BlobServiceClient

load_dotenv()



connection_string = os.getenv("BLOB_CONNECTION_STRING")
# container_id = os.getenv("CONTAINER_ID")
training_container_id = "galaxy-zoo-training-images"
test_container_id = "galaxy-zoo-test-images"

if not connection_string:
    raise Exception("BLOB_CONNECTION_STRING is not defined in your environment variables.")

# connect to Azure blob service
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


def create_container(container_id):
    try:
        blob_service_client.create_container(container_id)
        print(f"Container {container_id} created.")
        # 
    except Exception as e:
        print(f"Container {container_id} possibly exist: {e}. ")
        if "ContainerAlreadyExists" in str(e):
            print(f"\nAccessing container. {container_id}\n")
            blob_service_client.get_container_client(container_id)

def blob_upload_image(container_id):
    if container_id == "galaxy-zoo-training-images":
        print("Importing training images from Kaggle...")
        path = import_training_data()
    elif container_id == "galaxy-zoo-test-images":
        print("Importing test images from Kaggle...")
        path = import_test_data()
    else:
        raise Exception("Container not found")
    
    for file in os.listdir(path):
        img_file_path = os.path.join(path, file)
        # print(img_file_path)
        if os.path.isfile(img_file_path):
            blob_client = blob_service_client.get_blob_client(container=container_id, blob=file)
            try:
                with open(img_file_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                print(f"File: {file} uploaded to Container: {container_id}")
            except Exception as e:
                print(f"Error uploading {file}: {e}")
    


    


if __name__ == '__main__':
    create_container(training_container_id)
    # blob_upload_image(training_container_id)
    create_container(test_container_id)
    # blob_upload_image(test_container_id)
