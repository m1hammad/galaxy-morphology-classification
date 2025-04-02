# custom_transforms.py
import random
import numpy as np
from skimage.transform import rotate
from torchvision.transforms.functional import to_pil_image
from PIL import Image

class RandomRotation:
    def __init__(self, angles=[0, 90, 180, 270]):
        self.angles = angles
    
    def __call__(self, img):
        # If img is a PIL Image, convert it to a numpy array.
        if isinstance(img, Image.Image):
            img = np.array(img)
        angle = random.choice(self.angles)
        rotated = rotate(img, angle, resize=False, mode='edge')
        # Convert rotated image back to a PIL Image
        return to_pil_image(rotated)