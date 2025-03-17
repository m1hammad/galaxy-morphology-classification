import kaggle 
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


def clean_up():
    if os.path.isdir(path):
        shutil.rmtree(path)


def import_target_values():
    clean_up()
    api.competition_download_file(
        competition=dataset,
        file_name=output_file,
        path=path,
        force=True,
    )

    with ZipFile(f"{path}/{output_file}", 'r') as target_val:
        target_val.extractall(f"{path}")
    os.remove(f"{path}/{output_file}")

    return os.path.join( path, output_file.split(".")[0]+'.csv')
    


def import_training_data():
    clean_up()
    api.competition_download_file(
        competition=dataset,
        file_name=training_images,
        path=path,
        force=True,
    )

    with ZipFile(f"{path}/{training_images}") as train_data:
        train_data.extractall(f"{path}")
    os.remove(f"{path}/{training_images}")

def import_test_data():
    clean_up()
    api.competition_download_file(
        competition=dataset,
        file_name=test_images,
        path=path,
        force=True,
    )

    with ZipFile(f"{path}/{test_images}") as test_data:
        test_data.extractall(f"{path}")
    os.remove(f"{path}/{test_images}")
    


if __name__ == "__main__":
    import_target_values()
    clean_up()