import cv2
import numpy as np
import math



#Carga de imagenes
img = cv2.imread('img.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,500,250)
cv2.imshow("Canny",edges)
cv2.waitKey()

sobely = cv2.Sobel(edges,cv2.CV_64F,0,1,ksize=9)
cv2.imshow("Canny",sobely)
cv2.waitKey()

lines = cv2.HoughLines(edges,1,np.pi/180,200)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(edges,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imshow("Canny",edges)
cv2.waitKey()

cv2.destroyAllWindows()