import cv2
import numpy as np
from app.preprocessing.image_preprocessor import ImagePreProcessor

class Grader:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)


    def load_model(self, model_path):
        # Load the trained YOLOv5 model
        model = None
        return model

    def preprocess_image(self, image):
        # Preprocess the input image
        pass