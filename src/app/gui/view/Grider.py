import cv2
import numpy as np
from PIL import Image

def get_row_image(img, num_columns, num_rows, row_number, roi):
    # Convert the image to a NumPy array
    img_np = np.array(img)

    # Extract the ROI coordinates
    left, top, width, height = roi
    # Crop the image to the selected ROI
    roi_img = img_np[top:top + height, left:left + width]

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



if __name__ == "__main__":
    image_path = "C:\Main\Code\GradeVision/test10/1685500.tif"
    img = cv2.imread(image_path)
    # img = cv2.resize(img, (1000, 1000))
    num_columns = 4
    num_rows = 15
    row_number = 2
    roi = (190, 671, 356, 1383)
    row_image = get_row_image(img, num_columns, num_rows, row_number, roi)
    cv2.imshow("Row Image", row_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()