import os
import cv2
import numpy as np
from PIL import Image

image_path = "plan.jpg"
image = cv2.imread(image_path)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# edges = cv2.Canny(gray, threshold1=50, threshold2=150)

# kernel = np.ones((5, 5), np.uint8)
# dilated = cv2.dilate(edges, kernel, iterations=1)
# eroded = cv2.erode(dilated, kernel, iterations=1)

# contours, _ = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# result_image = np.zeros_like(image)

# for contour in contours:
#     if cv2.contourArea(contour) > 10000:  
#         cv2.drawContours(result_image, [contour], -1, (255, 255, 255), 1)

# final_result = Image.fromarray(result_image)

output_folder = "preprocessed_images"
output_filename = "floor_plan_processed.png"
output_path = os.path.join(output_folder, output_filename)

# final_result.save(output_path)

# print(f"Image saved at: {output_path}")

_, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

cv2.imwrite(output_path, binary)
print("done")

contours, _= cv2.findContours(binary, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

image_copy = binary.copy()

image_copy = cv2.drawContours(image_copy, contours, -1, (123, 0, 128), 2)

cv2.imshow('CONTOUR', image_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()