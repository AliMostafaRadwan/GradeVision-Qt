import cv2
import numpy as np

def detect_circles(image_path):
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply GaussianBlur to reduce noise and help circle detection
    img_blur = cv2.GaussianBlur(img, (9, 9), 2)

    # Use HoughCircles to detect circles
    circles = cv2.HoughCircles(
        img_blur,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=10,
        maxRadius=30
    )

    if circles is not None:
        # Convert the circle coordinates to integers
        circles = np.round(circles[0, :]).astype("int")

        # Sort the circles by their y-coordinates to group them into rows
        circles = sorted(circles, key=lambda x: x[1])

        # Calculate the average radius to use as a threshold for grouping circles into rows
        avg_radius = np.mean([circle[2] for circle in circles])

        # Initialize variables to store the number of rows and columns
        num_rows = 1
        num_columns = 0

        # Iterate through the circles to group them into rows and columns
        prev_y = circles[0][1]
        for circle in circles[1:]:
            if circle[1] - prev_y > avg_radius * 0.8:  # Adjust the tolerance factor
                # New row detected
                num_rows += 1
                num_columns = 1
            else:
                # Still in the same row
                num_columns += 1
            prev_y = circle[1]

        # Print the number of rows and columns
        print(f"Number of rows: {num_rows}")
        print(f"Number of columns: {num_columns}")

        # Draw the circles on the image
        for (x, y, r) in circles:
            cv2.circle(img, (x, y), r, (0, 255, 0), 4)

        # Display the image with detected circles
        cv2.imshow("Detected Circles", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No circles detected in the image.")

if __name__ == "__main__":
    image_path = "test.png"
    detect_circles(image_path)
