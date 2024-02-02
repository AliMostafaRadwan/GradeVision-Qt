import os
import cv2
import numpy as np

# def get_all_rows(img, num_columns, num_rows, roi):
#     # Convert the image to a NumPy array
#     img_np = np.array(img)

#     # Extract the ROI coordinates
#     left, top, width, height = roi
#     # Crop the image to the selected ROI
#     roi_img = img_np[top:top + height, left:left + width]

#     # Calculate the width and height of each bubble
#     bubble_width = width // num_columns
#     bubble_height = height // num_rows

#     row_images = []
#     # Loop through all rows
#     for row_number in range(num_rows):
#         row_start = row_number * bubble_height
#         row_end = row_start + bubble_height

#         # Extract the specific row image from the ROI
#         row_image = roi_img[row_start:row_end, :]
#         row_images.append(row_image)

#     return row_images



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


# def process_images(input_folder, output_folder, num_columns, num_rows, roi):
#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     # Loop through all files in the input folder
#     for filename in os.listdir(input_folder):
#         print(filename)
#         if filename.endswith(".tif") or filename.endswith(".jpg") or filename.endswith(".png"):
#             # Read the image
#             image_path = os.path.join(input_folder, filename)
#             img = cv2.imread(image_path)
#             img = cv2.resize(img, (1000, 1000))  # Adjust the size if needed

#             # Get all row images
#             row_images = get_all_rows(img, num_columns, num_rows, roi)

#             # Save all row images to the output folder
#             for i, row_image in enumerate(row_images):
#                 output_path = os.path.join(output_folder, f"row_{i + 1}_{filename}")
#                 cv2.imwrite(output_path.replace('.tif', '.jpeg').replace('.jpg', '.jpeg').replace('.png', '.jpeg'), row_image)




def analyze_bubble_sheet(image_path, roi, num_columns, num_rows,tolerance=50):
    def find_duplicated_rows(choice):
        choice_rows = [i[0] for i in choice]
        return {x for x in choice_rows if choice_rows.count(x) > 1}

    # Load the image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (1000, 1000), interpolation=cv2.INTER_AREA)

    # Extract the ROI coordinates
    x, y, w, h = roi

    # Crop the image to the selected ROI
    roi_img = img[y:y + h, x:x + w]

    # Calculate the width and height of each bubble
    bubble_width = w // num_columns
    bubble_height = h // num_rows

    bubbles = []  # Store bubble coordinates
    CHOICE = []  # Store non-black bubble coordinates

    for row in range(num_rows):
        row_bubbles = []  # Store row bubble coordinates
        for col in range(num_columns):
            x1 = col * bubble_width
            y1 = row * bubble_height
            x2 = x1 + bubble_width
            y2 = y1 + bubble_height

            row_bubbles.append((x1, y1, x2, y2))
            bubble = roi_img[y1:y2, x1:x2]

            black_pixels = np.sum(bubble < 150)  # Count black pixels
            total_pixels = bubble_width * bubble_height
            percentage_black_pixels = (black_pixels / total_pixels) * 100
            # print(f"Percentage of black pixels in Row {row + 1}, Choice {col + 1}: {percentage_black_pixels:.2f}%")
            # print("------")

            if percentage_black_pixels > tolerance:
                CHOICE.append((row, col))

        bubbles.append(row_bubbles)

    duplicated_row = find_duplicated_rows(CHOICE)

    return bubbles, roi_img, CHOICE, duplicated_row






if __name__ == "__main__":
    input_folder = "C:/Main/Code/GradeVision/test1000"
    output_folder = "A:\Main\CODE\GUI\GradeVision-QT-material - TESTVERSION\GradeVision/app\components\datasetSorted"
    num_columns = 4
    num_rows = 19
    roi = (608, 378, 205, 571)

    # process_images(input_folder, output_folder, num_columns, num_rows, roi)
    
    #loop through the input folder
    

    for filename in os.listdir(input_folder):
        
        bubbles, roi_img, CHOICE, duplicated_row = analyze_bubble_sheet(os.path.join(input_folder, filename), roi, num_columns, num_rows)
        
        fullimage = cv2.imread(os.path.join(input_folder, filename))
        fullimage = cv2.resize(fullimage, (1000, 1000), interpolation=cv2.INTER_AREA)
        if len(duplicated_row) > 0:
            for row in duplicated_row:
                row_image = get_row_image(fullimage, num_columns, num_rows, row+1, roi)
                output_path = os.path.join(output_folder, f"row_{row + 1}_{filename}")
                cv2.imwrite(output_path.replace('.tif', '.jpeg').replace('.jpg', '.jpeg').replace('.png', '.jpeg'), row_image)
            # row = get_row_image(roi_img, num_columns, num_rows, duplicated_row, roi)
            
