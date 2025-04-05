from torch.utils.data import DataLoader, random_split
import torch.nn as nn
from torchvision.models import efficientnet_b0, efficientnet_b1, efficientnet_b2, efficientnet_b3, efficientnet_b4, efficientnet_b5, efficientnet_b6, efficientnet_b7, resnet18, resnet50, vit_b_16, vit_b_32

class CNNFromScratch(nn.Module):
    def __init__(self, num_outputs=37):
        super(CNNFromScratch, self).__init__()

        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),  # 32*(pixel*pixel)   in our case 3*224*224
            nn.BatchNorm2d(num_features=32),      # Expects 32 channels. Will compute normalization separately for each channel. Normalizes the outputs of the convolution to speed up training and improve stability.
            nn.ReLU(inplace=True),  # ReLU activation function
            nn.MaxPool2d(2),  # Performs max pooling. kernel size 2 halves input pixels, reducing computational cost. 32*112*112

            # Block 2
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),   # 64*112*112
            nn.BatchNorm2d(num_features=64),  # Expects 64 channels. Will compute normalization separately for each channel. Normalizes the outputs of the convolution to speed up training and improve stability.
            nn.ReLU(inplace=True),  # ReLU activation function
            nn.MaxPool2d(2), # 64*56*56

            # Block 3
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),  # 128*56*56
            nn.BatchNorm2d(num_features=128),  # Expects 128 channels. Will compute normalization separately for each channel. Normalizes the outputs of the convolution to speed up training and improve stability.
            nn.ReLU(inplace=True),  # ReLU activation function
            nn.MaxPool2d(2),   # 128*28*28

            # Block 4
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1),  # 256*28*28
            nn.BatchNorm2d(num_features=256),  # Expects 256 channels. Will compute normalization separately for each channel. Normalizes the outputs of the convolution to speed up training and improve stability.
            nn.ReLU(inplace=True),  # ReLU activation function
            nn.MaxPool2d(2),   # 256*14*14

            # Block 5
            nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, padding=1),  # 512*14*14
            nn.BatchNorm2d(num_features=512),  # Expects 512 channels. Will compute normalization separately for each channel. Normalizes the outputs of the convolution to speed up training and improve stability.
            nn.ReLU(inplace=True),  # ReLU activation function
            nn.MaxPool2d(2),   # 512*7*7
        )

        self.classifier = nn.Sequential(    # Fully Connected Layers
            nn.Flatten(),   # Flatten 3D tensor of shape 512*7*7 to 1D vector 512 * 7 * 7 = 25088 elements
            nn.Linear(512 * 7 * 7, 1024),    # 1st fully connected layer, reduce the vector size to 1024
            nn.ReLU(inplace=True),    # ReLU activation functio
            nn.Dropout(0.5),    # Dropout regularization to help prevent overfitting
            nn.Linear(1024, num_outputs)   # Regression output
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

def get_efficientnet(version=0, num_outputs=37):

    # model selection
    if version == 0:
        model = efficientnet_b0(pretrained=True)
    elif version == 1:
        model = efficientnet_b1(pretrained=True)
    elif version == 2:
        model = efficientnet_b2(pretrained=True)
    elif version == 3:
        model = efficientnet_b3(pretrained=True)
    elif version == 4:
        model = efficientnet_b4(pretrained=True)
    elif version == 5:
        model = efficientnet_b5(pretrained=True)
    elif version == 6:
        model = efficientnet_b6(pretrained=True)
    elif version == 7:
        model = efficientnet_b7(pretrained=True)
    else:
        raise ValueError("Version must be an integer between 0 and 7.")
    
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_outputs)

    return model

def get_resnet(version, num_outputs=37):
    if version == 18:
        model = resnet18(pretrained=True)
    elif version == 50:
        model = resnet50(pretrained=True)
    else:
        raise ValueError("Version must be either 18 or 50.")
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_outputs)
    return model

def get_vit(layers = 16, num_outputs=37):
    if layers == 16:
        model = vit_b_16(pretrained=True)
    elif layers == 32:
        model = vit_b_32(pretrained=True)
    else:
        raise ValueError("Layers must be either 16 or 32.")
    in_features = model.heads.head.in_features
    model.heads.head = nn.Linear(in_features, num_outputs)
    return model
