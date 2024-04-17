
"""
pre processing of the images to be used in the model

input: folder path of the images
output: processed images

using yield to return the processed images one by one to avoid memory issues since the images are in batches
"""

import os
import cv2

class ImageProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def process_images_generator(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')):
                image_path = os.path.join(self.folder_path, filename)
                image = cv2.imread(image_path)
                # Resize the image to a maximum of 1000 pixels while maintaining the aspect ratio
                height, width = image.shape[:2]
                max_dim = max(height, width)
                scale = 1000 / max_dim
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = cv2.resize(image, (new_width, new_height))
                
                
                # Perform your image processing operations on 'image'
                bitwise_not = cv2.bitwise_not(image)
                image = cv2.cvtColor(bitwise_not, cv2.COLOR_BGR2GRAY)
                
                
                yield image

if __name__ == "__main__":
    folder_path = r"C:\Main\Code\GradeVision\test10"
    image_processor = ImageProcessor(folder_path)

    # Using the generator
    image_generator = image_processor.process_images_generator()

    for processed_image in image_generator:
        # Process each image as needed
        cv2.imshow('Processed Image', processed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
