import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_img(img):
  plt.axis("off")
  plt.imshow(img,cmap='gray')
  plt.show()

def remove_border_and_lines(gray):
    # # Read the image
    # image = cv2.imread(image_path)
    # show_img(image)
    # # Convert to grayscale
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    show_img(gray)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Create horizontal and vertical kernels for morphological operations
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))

    # Remove horizontal lines
    horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    thresh = cv2.subtract(thresh, horizontal_lines)

    # Remove vertical lines
    vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    thresh = cv2.subtract(thresh, vertical_lines)

    # Remove small noise using morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # Invert the image
    thresh = cv2.bitwise_not(thresh)

    show_img(thresh)
    return thresh

# Example usage
#remove_border_and_lines('check_image.png')
