import cv2
import numpy as np

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
            print(f"Percentage of black pixels in Row {row + 1}, Choice {col + 1}: {percentage_black_pixels:.2f}%")
            print("------")

            if percentage_black_pixels > tolerance:
                CHOICE.append((row, col))

        bubbles.append(row_bubbles)

    duplicated_row = find_duplicated_rows(CHOICE)

    return bubbles, roi_img, CHOICE, duplicated_row

# if __name__ == "__main__":
#     image_path = "Physics G11/0001.jpg"
#     roi = [69, 180, 154, 404]  # ROI coordinates
#     num_columns = 4  # Number of columns in the bubble sheet
#     num_rows = 15   # Number of rows in the bubble sheet

#     bubbles, roi_img, CHOICE, duplicated_row = analyze_bubble_sheet(image_path, roi, num_columns, num_rows)

#     # Rest of the code remains the same

#     # Now you can access each bubble using the nested list (bubbles[row][column])
#     # For example, to access the second row, fourth column bubble:
#     BUBBLE = bubbles[1][1]
#     print("Coordinates of the second row, fourth column bubble:", BUBBLE)

#     # Draw red rectangles around the selected bubbles
#     x1, y1, x2, y2 = BUBBLE
#     roi_img = cv2.rectangle(roi_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

#     # Draw red rectangles around duplicated rows
#     for row in duplicated_row:
#         x1, y1, x2, y2 = bubbles[row][0]
#         roi_img = cv2.rectangle(roi_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
#     print("Duplicated row/s:", duplicated_row)
#     print("Choice:", CHOICE)
#     cv2.imshow("Bubble Sheet with Boxes", roi_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()