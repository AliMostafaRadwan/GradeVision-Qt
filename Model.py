import torch
import numpy as np
import cv2
# import time
# import mss
from glob import glob
# from PIL import Image

from Grider import get_row_image

class ObjectDetection:
    """
    Class implements Yolo5 model to make inferences on a youtube video using OpenCV.
    """
    
    def __init__(self):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param out_file: A valid output file name.
        """
        self.model = self.load_model()
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("\n\nDevice Used:",self.device)



    def load_model(self):
        return torch.hub.load('yolov5', model='custom', path='best.pt', source='local', force_reload=True)



    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
    
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord


    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]


    def plot_boxes(self, results, frame):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                bgr2 = (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
                cv2.putText(frame, f'{row[4]:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr2, 1)
        return frame

    def load_images(self, folder_path):
        """
        Load a list of images from a folder.
        :param folder_path: Path to the folder containing images.
        :return: List of image file paths.
        """
        image_files = glob(folder_path + '/*.tif')  # Update the file extension if needed
        return image_files


    def Analize_Dublicates(self, image, num_columns=4, num_rows=19,duplicated_row=None, roi=None):


        # image_files = self.load_images('scan')  # Update with your image folder path
        # for image_file in image_files:
        # img = cv2.imread(image_file)
        # img = cv2.resize(img, (1000, 1000), interpolation=cv2.INTER_AREA)

        img = get_row_image(image, num_columns, num_rows, duplicated_row, roi)

        image_height, image_width, _ = img.shape
        
        # Calculate the width of each column
        column_width = image_width // num_columns

        # Split the image into columns
        column_images = [img[:, i * column_width: (i + 1) * column_width, :] for i in range(num_columns)]
        


        # Display each column
        for i, column_img in enumerate(column_images):
            results1 = self.score_frame(column_img)
            column_img = self.plot_boxes(results1, column_img)
            # cv2.imshow(f"Column {chr(65 + i)}", column_img)
            if len(results1[0]) > 0:
                detected_class = int(results1[0][0])  # Access the first detected class label
                # print(f"Detected Class is Column {chr(65 + i)}:", self.classes[detected_class])
                if self.classes[detected_class] == "correct":
                    # print(chr(65 + i), "is correctttt")
                    return chr(65 + i)

            else:
                pass



        # key = cv2.waitKey(0)
        # if key == ord('n'):
        #     continue
        # elif key == ord('q'):
        #     cv2.destroyAllWindows()
        #     break


# Create a new object and execute.
# detection = ObjectDetection()
# detection()

# image_files = glob('scan' + '/*.tif')

# num_columns = 4
# detection = ObjectDetection()
# print("model loaded")
# for image_file in image_files:
#     img = cv2.imread(image_file)
#     img = cv2.resize(img, (1000, 1000), interpolation=cv2.INTER_AREA)

#     print(detection.Analize_Dublicates(img, num_columns, 19, 1, (605, 381, 198, 575)))
