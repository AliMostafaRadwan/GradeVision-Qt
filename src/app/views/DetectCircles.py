import cv2
import numpy as np

def detect_contours(img, x, y, w, h):
    # Read the image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    roi = img[y:y+h, x:x+w]

    # Apply GaussianBlur to reduce noise
    roi_blur = cv2.GaussianBlur(roi, (9, 9), 2)

    # Apply adaptive thresholding to create a binary image
    _, binary = cv2.threshold(roi_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Compute horizontal projection
    horizontal_projection = np.sum(binary, axis=1)

    # Compute vertical projection
    vertical_projection = np.sum(binary, axis=0)

    # Set a threshold for detecting rows and columns
    row_threshold = 0.8 * np.max(horizontal_projection)
    column_threshold = 0.8 * np.max(vertical_projection)

    # Find row positions where the projection values exceed the threshold
    row_positions = np.where(horizontal_projection > row_threshold)[0]

    # Find column positions where the projection values exceed the threshold
    column_positions = np.where(vertical_projection > column_threshold)[0]

    # Calculate the number of rows and columns
    num_rows = len(row_positions)
    num_columns = len(column_positions)

    # Print the number of rows and columns
    print(f"Number of rows: {num_rows}")
    print(f"Number of columns: {num_columns}")

    # Display the ROI with detected rows and columns
    cv2.imshow("Detected Rows and Columns", roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# if __name__ == "__main__":
#     image_path = "C:\Main\Code\GradeVision/test10/1685500.tif"
#     x = 209
#     y = 193
#     w = 81
#     h = 282
#     img = cv2.imread(image_path)
#     img = cv2.resize(img, (351, 500))
#     detect_rows_and_columns(img, x, y, w, h)