import cv2
import numpy as np

img1 = np.zeros((400,200), np.uint8)
img2 = np.zeros((400,200), np.uint8)
img3 = np.zeros((400,200), np.uint8)

fil,col = img1.shape

img1[0:fil,0:col/2] = 255
cv2.imshow("img1",img1)

img2[100:150,150:350] = 255
cv2.imshow("img2",img2)
 
res = cv2.bitwise_and(img1,img2,img3)
cv2.imshow("AND",res)

res = cv2.bitwise_or(img1,img2,res)
cv2.imshow("OR",res);

res = cv2.bitwise_xor(img1,img2,res)
cv2.imshow("XOR",res)

res = cv2.bitwise_not(img1)
cv2.imshow("NOT",res)
 
cv2.waitKey(0)
cv2.destroyAllWindows()