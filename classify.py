import numpy as np
from PIL import Image
import cv2
from scipy.spatial.distance import cdist

def load_and_preprocess(image_path):
    # Load image and convert to grayscale
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    
    # Convert to binary image (black and white only)
    _, binary = cv2.threshold(img_array, 127, 255, cv2.THRESH_BINARY_INV)
    return binary

def detect_lines(binary_image):
    # Use HoughLinesP to detect straight lines
    lines = cv2.HoughLinesP(
        binary_image,
        rho=1,
        theta=np.pi/180,
        threshold=50,
        minLineLength=20,
        maxLineGap=10
    )
    
    # Convert lines to a more manageable format
    processed_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Calculate line length
            length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            # Calculate angle
            angle = np.arctan2(y2-y1, x2-x1)
            processed_lines.append({
                'points': [(x1, y1), (x2, y2)],
                'length': length,
                'angle': angle
            })
    
    return processed_lines

def merge_similar_lines(lines, distance_threshold=10, angle_threshold=0.1):
    if not lines:
        return []
    
    merged_lines = []
    used = set()
    
    for i, line1 in enumerate(lines):
        if i in used:
            continue
            
        similar_lines = [line1['points']]
        used.add(i)
        
        for j, line2 in enumerate(lines):
            if j in used:
                continue
                
            # Check if lines are parallel and close
            angle_diff = abs(line1['angle'] - line2['angle'])
            if angle_diff < angle_threshold or abs(angle_diff - np.pi) < angle_threshold:
                # Calculate distances between endpoints
                points1 = np.array(line1['points'])
                points2 = np.array(line2['points'])
                distances = cdist(points1, points2)
                
                if np.min(distances) < distance_threshold:
                    similar_lines.append(line2['points'])
                    used.add(j)
        
        # Merge similar lines
        if similar_lines:
            all_points = np.array([point for line in similar_lines for point in line])
            if len(all_points) >= 2:
                # Find the two most distant points
                distances = cdist(all_points, all_points)
                i, j = np.unravel_index(distances.argmax(), distances.shape)
                merged_lines.append({
                    'points': [
                        (int(all_points[i][0]), int(all_points[i][1])),
                        (int(all_points[j][0]), int(all_points[j][1]))
                    ]
                })
    
    return merged_lines

def generate_wall_geometry(line, thickness=0.2, height=8.0):
    (x1, y1), (x2, y2) = line['points']
    
    # Scale coordinates from pixels to feet (adjust scale factor as needed)
    scale = 0.1  # This means 10 pixels = 1 foot
    x1, y1 = x1 * scale, y1 * scale
    x2, y2 = x2 * scale, y2 * scale
    
    # Create wall geometry with thickness
    dx = x2 - x1
    dy = y2 - y1
    length = np.sqrt(dx*dx + dy*dy)
    if length == 0:
        return None
        
    # Normalize direction vector
    dx, dy = dx/length, dy/length
    
    # Perpendicular vector for thickness
    px, py = -dy * thickness/2, dx * thickness/2
    
    # Generate four corners of the wall
    points = [
        [x1 - px, y1 - py],
        [x2 - px, y2 - py],
        [x2 + px, y2 + py],
        [x1 + px, y1 + py]
    ]
    
    return {
        "type": "wall",
        "points": points,
        "height": height
    }

def process_floor_plan(image_path):
    # Load and preprocess image
    binary_image = load_and_preprocess(image_path)
    
    # Detect lines
    lines = detect_lines(binary_image)
    
    # Merge similar lines
    merged_lines = merge_similar_lines(lines)
    
    # Generate geometry data
    geometry_data = []
    for line in merged_lines:
        wall_geometry = generate_wall_geometry(line)
        if wall_geometry:
            geometry_data.append(wall_geometry)
    
    return geometry_data

def save_geometry_data(geometry_data, output_path):
    import json
    with open(output_path, 'w') as f:
        json.dump(geometry_data, f, indent=2)

if __name__ == "__main__":
    image_path = "preprocessed_images/floor_plan_no_text.png"  
    output_path = "generated_geometry_data.json"
    
    geometry_data = process_floor_plan(image_path)
    save_geometry_data(geometry_data, output_path)