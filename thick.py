import cv2
import numpy as np

# 1. Load the preprocessed image
image = cv2.imread("preprocessed_images/floor_plan_processed.png", cv2.IMREAD_GRAYSCALE)

# 2. Dilation kernel - adjust size for thickness
kernel = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(image, kernel, iterations=1)

# 3. Show/save
cv2.imshow("Dilated (Thick All Lines)", dilated)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("preprocessed_thick_all_lines.png", dilated)
