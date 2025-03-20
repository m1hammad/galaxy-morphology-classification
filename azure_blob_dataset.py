
import torch
from torch.utils.data import Dataset
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
from io import BytesIO
from skimage import io, transform, img_as_float

load_dotenv()



class AzureBlobDataset(Dataset):
    def __init__(self, train=True, transform=None, target_dict=None , img_size=(424, 424)):
        self.img_size = img_size
        self.transform = transform
        self.train = train
        self.target_dict = target_dict

        connection_string = os.getenv("BLOB_CONNECTION_STRING")

        if not connection_string:
            raise Exception("BLOB_CONNECTION_STRING is not defined in your environment variables.")

        # connect to Azure blob service
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        self.containers = self.blob_service_client.list_containers(include_metadata=False)
        
        is_train = 'training' if self.train else 'test'
        self.blob_container = next(self.blob_service_client.get_container_client(container) for container in self.containers if is_train in container.name)

        if not self.blob_container:
            raise ValueError(f"Container containing word '{is_train}' not found.")
        
        self.blobs = list(self.blob_container.list_blobs())

    def __len__(self):
        return len(self.blobs)
    
    def __getitem__(self, index):
        blob = self.blobs[index]
        galaxy_id = os.path.splitext(blob.name)

        # Download and proccess image in memory
        img_client = self.blob_container.get_blob_client(blob)
        img_bytes = img_client.download_blob().readall()

        # Load with scikit-image
        img = io.imread(BytesIO(img_bytes))

        # Convert image to float, normalized in the range [0,1]
        img = img_as_float(img)

        # Optional resizing (Experimental: original images are pretty clean and the accuracy is needed for detailed classifications e.g for spirals)
        img = transform.resize(img, self.img_size, anti_aliasing=True)

        # If additional transforms from TorchVision are provided 
        if self.transform:
            img_tensor = self.transform(img)
        else:
            # Default conversion from numpy array to tensor, with channel-first format.
            img_tensor = torch.from_numpy(img).permute(2, 0, 1).float()
            
        output =  {
            'image' : img_tensor,
            'galaxy_id' : galaxy_id,
        }

        if self.train:
            try:
                target = torch.tensor(self.target_dict.get(galaxy_id, []), dtype=torch.float32)
            except KeyError:
                raise RuntimeError(f"Missing target for training GalaxyID: {galaxy_id}")
            output['target'] = target

        return output
