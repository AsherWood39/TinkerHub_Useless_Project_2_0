# Image processing module for detecting and highlighting patterns in images
# Uses OpenCV to detect edges and create a high-contrast outline of interesting shapes

import cv2
import numpy as np
import os

def detect_creases(image_path):
    """
    Process an image to detect and highlight interesting patterns.
    
    Args:
        image_path (str): Path to the input image file
        
    Returns:
        str: Path to the processed image file with detected contours
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to load image at {image_path}")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    edges = cv2.Canny(blurred, 30, 90, apertureSize=3)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a black background
    contour_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    # Draw white contours on black background
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 2)

    # Optional: Thicken the lines slightly for better visibility
    kernel = np.ones((3,3), np.uint8)
    contour_image = cv2.dilate(contour_image, kernel, iterations=1)

    output_path = "traced_creases.png"
    cv2.imwrite(output_path, contour_image)
    print(f"Traced image saved to {output_path}")
    return output_path