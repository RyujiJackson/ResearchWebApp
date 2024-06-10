import json
import cv2
import numpy as np
from PIL import Image


def get_mask():
    # Define the file path
    file_path = 'static/annotation/0/array.txt'

    # Read the data from the file as a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Replace single quotes with double quotes to make it a valid JSON
    file_content = file_content.replace("'", '"')

    # Parse the JSON data
    data = json.loads(file_content)

    # Extract the x and y coordinates
    coordinates = [(point['x'] * 2, point['y'] * 2) for point in data]

    # Print the coordinates array
    print(coordinates)
    
    # Define the size of the mask image
    mask_height = 1024  # You can adjust the height as needed
    mask_width = 1024   # You can adjust the width as needed

    # Create a blank binary mask image
    mask = np.zeros((mask_height, mask_width), dtype=np.uint8)

    # Convert the coordinates to integer values
    int_coords = [(int(x), int(y)) for x, y in coordinates]

    # Draw the polygon on the mask image
    cv2.fillPoly(mask, [np.array(int_coords, dtype=np.int32)], 255)

    
    cv2.imshow('Binary Mask', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    apply_mask(mask)

def apply_mask(mask):
    heatmap = cv2.imread("static/uploads/heatmap/20150414000010001.png")
    image = cv2.imread("static/uploads/origin/20150414000010001.png")
    # Blend the images with specified weights
    alpha = 0.4  # Weight of the first image
    beta = 1 - alpha  # Weight of the second image
    image = cv2.addWeighted(heatmap, alpha, image, beta, 0)
    masked_heatmap = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow('Binary Mask', masked_heatmap)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

get_mask()

