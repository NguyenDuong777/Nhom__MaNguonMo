import cv2
import numpy as np

img = cv2.imread('Pic1.jpg')
img = cv2.resize(img, (300, 300))

kernel_identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
kernel_3x3 = np.ones((3, 3), np.float32) / 9.0
kernel_5x5 = np.ones((5, 5), np.float32) / 25.0

output_identity = cv2.filter2D(img, -1, kernel_identity)
output_3x3 = cv2.filter2D(img, -1, kernel_3x3)

img_copy = img.copy()
output_5x5 = cv2.filter2D(img[0:100, 0:100], -1, kernel_5x5)
img_copy[0:100, 0:100] = output_5x5

def create_captioned_image(image, caption, width, height):
    caption_area = np.zeros((50, width, 3), dtype=np.uint8)
    cv2.putText(caption_area, caption, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    return cv2.vconcat([caption_area, image])

img_captioned = create_captioned_image(img, "Original", 300, 300)
output_identity_captioned = create_captioned_image(output_identity, "Identity Filter", 300, 300)
output_3x3_captioned = create_captioned_image(output_3x3, "3x3 Filter", 300, 300)
output_5x5_captioned = create_captioned_image(img_copy, "5x5 Filter", 300, 300)

top_row = cv2.hconcat([img_captioned, output_identity_captioned])
bottom_row = cv2.hconcat([output_3x3_captioned, output_5x5_captioned])
combined = cv2.vconcat([top_row, bottom_row])

cv2.imshow('Filters Combined with Captions', combined)
cv2.waitKey(0)
cv2.destroyAllWindows()
