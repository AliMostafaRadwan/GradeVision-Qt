def adjust_roi(original_size, roi):
    """
    Adjusts an ROI from an original image to match a 1000x1000 version of that image.
    
    Parameters:
        original_size (tuple): The (width, height) of the original image.
        roi (tuple): The (x, y, width, height) defining the ROI in the original image.
    
    Returns:
        tuple: The adjusted (x, y, width, height) for the ROI in a 1000x1000 image.
    """
    original_width, original_height = original_size
    x, y, width, height = roi
    
    scaled_width, scaled_height = 1000, 1000  # Target size
    # Calculate scaling factor (assuming a square scale target)
    width_scaling_factor = scaled_width / original_width
    height_scaling_factor = scaled_height / original_height

    
    print(f"Scaling Factor: {width_scaling_factor}, {height_scaling_factor}")
    # Adjust ROI dimensions
    adjusted_x = int(x * width_scaling_factor)
    adjusted_y = int(y * height_scaling_factor)
    adjusted_width = int(width * width_scaling_factor)
    adjusted_height = int(height * height_scaling_factor)
    
    return int(adjusted_x), int(adjusted_y), int(adjusted_width), int(adjusted_height)

# Example Usage
original_image_size = (351, 500)  # Example original size
original_roi = (211, 191, 76, 287)  # Example ROI in original image

adjusted_roi = adjust_roi(original_image_size, original_roi)
print(f"Adjusted ROI: {adjusted_roi}")
