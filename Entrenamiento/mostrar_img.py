import numpy as np
import cv2

# Load an color image in grayscale
img = cv2.imread('rgb.jpg',1)
img1 = cv2.imread('rgb.jpg',0)

cv2.imshow('image',img)
cv2.imshow('segunda',img1)

cv2.waitKey(0)

cv2.destroyWindow('image')
cv2.imwrite('rgb_grises.gif', img1)

cv2.waitKey(0)
cv2.destroyAllWindows()