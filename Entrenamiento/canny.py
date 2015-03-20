import cv2
import numpy as np

u1,u2=100,200

def nothing():
    cv2.imshow("Canny",edges)

img = cv2.imread('img (34).jpg',0)
cv2.namedWindow("umbrales",cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("Umbral1", "umbrales", 0, 500, nothing)
cv2.createTrackbar("Umbral2", "umbrales", 0, 500, nothing)


while(1):
    edges = cv2.Canny(img,u1,u2)
    cv2.imshow("Original",img)
    cv2.imshow("Canny",edges)
    
    u1 = cv2.getTrackbarPos("Umbral1", "umbrales")
    u2 = cv2.getTrackbarPos("Umbral2", "umbrales")
    
    if cv2.waitKey(1) == 27:
        cv2.imwrite("canny.jpg", edges)
        break

cv2.destroyAllWindows()