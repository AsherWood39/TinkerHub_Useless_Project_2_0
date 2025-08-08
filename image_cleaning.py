import cv2
import numpy as np
import os

def detect_creases(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to load image at {image_path}")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    edges = cv2.Canny(blurred, 30, 90, apertureSize=3)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_image = np.zeros_like(img)

    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 2)

    final_image = cv2.addWeighted(img, 0.8, contour_image, 1, 0)

    output_path = "traced_creases.png"
    cv2.imwrite(output_path, final_image)
    print(f"Traced image saved to {output_path}")
    return output_path