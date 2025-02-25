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
    cv2.namedWindow("Result")
    def nothing(x):
        pass

    cv2.createTrackbar("Threshold", "Result", 2, 255, nothing)
    cv2.createTrackbar("Erosion Iterations", "Result", 1, 20, nothing)
    # Dilate the text mask slightly to ensure complete coverage
    text_mask = cv2.dilate(text_mask, kernel, iterations=2)
    
    while True:
    # Inpaint the text regions
        threshold_value = cv2.getTrackbarPos("Threshold", "Result")
        erosion_iterations = cv2.getTrackbarPos("Erosion Iterations", "Result")
        result = cv2.inpaint(image, text_mask.astype(np.uint8), 3, cv2.INPAINT_TELEA)
        ksize = (erosion_iterations, erosion_iterations) 
        result = cv2.blur(result, ksize, cv2.BORDER_DEFAULT) 
  
        _, result = cv2.threshold(result, threshold_value, 255, cv2.THRESH_BINARY_INV)
        # result = cv2.erode(result, kernel, iterations=10)





        # _, result = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY_INV)

        # # Apply erosion
        # result = cv2.erode(result, kernel, iterations=erosion_iterations)

    # result = cv2.dilate(src=result, kernel=kernel, iterations=1)
    # Save the result
        cv2.imshow("Result", result)

        # Press 'ESC' to exit the loop
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.imwrite(output_path, result)
    
    return result

# Example usage
input_image_path = "preprocessed_images/floor_plan_processed.png"  # Replace with your input image path
output_image_path = "preprocessed_images/floor_plan_no_text.png"  # Replace with desired output path
remove_text_from_floorplan(input_image_path, output_image_path)

