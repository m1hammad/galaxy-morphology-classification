from zipfile import ZipFile
from kaggle.api.kaggle_api_extended import KaggleApi
# from dotenv import load_dotenv, dotenv_values
import os
import shutil



api = KaggleApi()
api.authenticate()

# load_dotenv()

dataset = "galaxy-zoo-the-galaxy-challenge"
output_file = "training_solutions_rev1.zip"
training_images = "images_training_rev1.zip"
test_images = "images_test_rev1.zip"

path = "temp_data"
train_path = os.path.join(path, "training")
test_path = os.path.join(path, "test")


def clean_up():
    if os.path.isdir(path):
        shutil.rmtree(path)


def import_target_values():
    # clean_up()

    #ensure directory exists, create one if not
    os.makedirs(path, exist_ok=True)

    #define file paths
    zip_path = os.path.join(path,output_file)
    csv_path = os.path.join(path, output_file.split(".")[0]+".csv")

    if not os.path.exists(zip_path):
        api.competition_download_file(
            competition=dataset,
            file_name=output_file,
            path=path,
            force=True,
        )
    else:
        print("Zip file for target values already exists. Using existing file")
    
    # Overwrite existing extracted file
    if os.path.exists(csv_path):
        os.remove(csv_path)
        
    # Extract the zip file
    with ZipFile(zip_path, 'r') as target_val:
        target_val.extractall(path)
    os.remove(zip_path)

    return csv_path
    


def import_training_data():
    #ensure directory exists, create one if not
    os.makedirs(train_path, exist_ok=True)

    # Define the zip file path and extracted folder path for training images
    zip_path = os.path.join(train_path, training_images)
    extracted_folder = os.path.join(train_path, training_images.split(".")[0])

    if not os.path.exists(zip_path):
        api.competition_download_file(
            competition=dataset,
            file_name=training_images,
            path=train_path,
            force=True,
        )
    else:
        print("Training images zip file already exists. Using the existing file.")

    # Overwrite existing extracted folder
    if os.path.exists(extracted_folder):
        shutil.rmtree(extracted_folder)

    # Extract the zip file
    with ZipFile(zip_path) as train_data:
        train_data.extractall(train_path)

    # Remove the zip file 
    os.remove(zip_path)
    return extracted_folder

def import_test_data():
    #ensure directory exists, create one if not
    os.makedirs(test_path, exist_ok=True)

    # Define the zip file path and extracted folder path for training images
    zip_path = os.path.join(test_path, test_images)
    extracted_folder = os.path.join(test_path, test_images.split(".")[0])

    if not os.path.exists(zip_path):
        api.competition_download_file(
            competition=dataset,
            file_name=test_images,
            path=test_path,
            force=True,
        )
    else:
        print("Test images zip file already exists. Using the existing file.")
       
    # Overwrite existing extracted folder
    if os.path.exists(extracted_folder):
        shutil.rmtree(extracted_folder)

    # Extract the zip file
    with ZipFile(zip_path) as test_data:
        test_data.extractall(test_path)

    # Remove the zip file 
    os.remove(zip_path)
    return extracted_folder
    


if __name__ == "__main__":
    import_target_values()
    # import_training_data()
    clean_up()