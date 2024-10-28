import cv2
import numpy as np

img = cv2.imread('Pic1.jpg')
rows, cols = img.shape[:2]

kernel_identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
kernel_3x3 = np.ones((3, 3), np.float32) / 9.0
kernel_5x5 = np.ones((5, 5), np.float32) / 25.0

output_identity = cv2.filter2D(img, -1, kernel_identity)
output_3x3 = cv2.filter2D(img, -1, kernel_3x3)

output_5x5 = cv2.filter2D(img[0:100, 0:100], -1, kernel_5x5)
img_copy = img.copy()
img_copy[0:100, 0:100] = output_5x5

combined = cv2.hconcat([img, output_identity, output_3x3, img_copy])

cv2.imshow('Filters Combined', combined)
cv2.waitKey(0)
cv2.destroyAllWindows()
