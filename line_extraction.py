import cv2
import numpy as np
from skimage.morphology import skeletonize

# Load the image
image_path = "preprocessed_images/floor_plan_no_text1.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Apply GaussianBlur to smoothen and reduce noise
blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Apply adaptive thresholding to get a binary image
binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 2)

# Skeletonization to reduce thick lines to single pixel width
skeleton = skeletonize(binary // 255)  # Convert binary to 0-1 before skeletonizing
skeleton = (skeleton * 255).astype(np.uint8)  # Convert back to 0-255

# Detect edges using Canny
edges = cv2.Canny(skeleton, 50, 150, apertureSize=3)

# Use Hough Line Transform to detect straight lines
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)

# Create an output image to draw lines
output = np.zeros_like(image)

# Draw detected lines
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(output, (x1, y1), (x2, y2), 255, 1)

# Save and show the processed image
cv2.imwrite("/mnt/data/extracted_lines.png", output)
cv2.imshow("Extracted Lines", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
