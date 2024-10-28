import cv2
import numpy as np

img = cv2.imread('Pic1.jpg')

kernel_identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
kernel_3x3 = np.ones((3, 3), np.float32) / 9.0
kernel_5x5 = np.ones((5, 5), np.float32) / 25.0

output_identity = cv2.filter2D(img, -1, kernel_identity)
output_3x3 = cv2.filter2D(img, -1, kernel_3x3)

img_copy = img.copy()
output_5x5 = cv2.filter2D(img[0:100, 0:100], -1, kernel_5x5)
img_copy[0:100, 0:100] = output_5x5

def add_text(image, text):
    return cv2.putText(image.copy(), text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

img_annotated = add_text(img, "Original")
output_identity_annotated = add_text(output_identity, "Identity Filter")
output_3x3_annotated = add_text(output_3x3, "3x3 Filter")
output_5x5_annotated = add_text(img_copy, "5x5 Filter")

top_row = cv2.hconcat([img_annotated, output_identity_annotated])
bottom_row = cv2.hconcat([output_3x3_annotated, output_5x5_annotated])
combined = cv2.vconcat([top_row, bottom_row])

cv2.imshow('Filters Combined in Grid', combined)
cv2.waitKey(0)
cv2.destroyAllWindows()
