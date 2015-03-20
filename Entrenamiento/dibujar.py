import numpy as np
import cv2

# Create a black image
img = np.zeros((512,1300,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
cv2.line(img,(0,0),(511,511),(0,0,255),55)
cv2.line(img,(100,0),(611,511),(255,255,255),45)
cv2.line(img,(000,100),(411,511),(255,255,255),45)
cv2.line(img,(000,200),(311,511),(255,0,0),35)
cv2.line(img,(200,0),(711,511),(255,0,0),35)

cv2.rectangle(img,(384,0),(500,128),(0,255,233),13)

cv2.circle(img, (400,400), 200, (0,255,0),15)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'National Geographic',(10,500), font, 4,(0,255,255),4)

cv2.imshow('line', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
