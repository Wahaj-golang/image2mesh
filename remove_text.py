import cv2
import numpy as np
from PIL import Image

def remove_text_from_floorplan(input_path, output_path):
    # Read the image
    image = cv2.imread(input_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image to get black text
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Create a kernel for morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    
    # Detect text regions
    # Use connected components to find text-like regions
    connectivity = 8
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)
    
    # Create a mask for text removal
    text_mask = np.zeros_like(thresh)
    
    # Filter components based on size and aspect ratio to identify text
    for i in range(1, num_labels):  # Skip background (label 0)
        area = stats[i, cv2.CC_STAT_AREA]
        width = stats[i, cv2.CC_STAT_WIDTH]
        height = stats[i, cv2.CC_STAT_HEIGHT]
        
        # Adjust these thresholds based on your specific image
        if area < 1000 and width < 100 and height < 50:  # These are likely text regions
            text_mask[labels == i] = 255
    
    # Dilate the text mask slightly to ensure complete coverage
    text_mask = cv2.dilate(text_mask, kernel, iterations=2)
    
    # Inpaint the text regions
    result = cv2.inpaint(image, text_mask.astype(np.uint8), 3, cv2.INPAINT_TELEA)
    
    # Save the result
    cv2.imwrite(output_path, result)
    
    return result

# Example usage
input_image_path = "preprocessed_images/floor_plan_processed.png"  # Replace with your input image path
output_image_path = "preprocessed_images/floor_plan_no_text.png"  # Replace with desired output path
remove_text_from_floorplan(input_image_path, output_image_path)