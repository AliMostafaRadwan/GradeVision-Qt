import cv2
import numpy as np
from PIL import Image

class Paper:
    """
    The Elementary DS we pass around
    """
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = self.load_image()
        # self.img_np = np.array(self.image)
        self.answers = None
        self.bubbles = None
        self.type = None
        ## metadata and stuff
    
    def load_image(self):
        pass
    
    def get_row_image(self, num_columns, num_rows, row_number, roi):
        # Convert the image to a NumPy array
        if not self.img_np: self.img_np = np.array(self.image)

        # Extract the ROI coordinates
        left, top, width, height = roi
        # Crop the image to the selected ROI
        roi_img = self.img_np[top:top + height, left:left + width]

        # Calculate the width and height of each bubble
        bubble_width = width // num_columns
        bubble_height = height // num_rows

        # Calculate the y-coordinate range for the specific row
        row_number = row_number - 1
        row_start = row_number * bubble_height
        row_end = row_start + bubble_height

        # Extract the specific row image from the ROI
        row_image = roi_img[row_start:row_end, :]
        # row_image = Image.fromarray(row_image)
        return row_image