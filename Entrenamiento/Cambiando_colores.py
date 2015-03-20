import cv2
import numpy as np
from matplotlib import pyplot as plt

def nothing(x):
    pass  

img = cv2.imread('contornocont.jpg')
cv2.namedWindow('Ventana')
cv2.createTrackbar('Value', 'Ventana', 0, 255, nothing)
cv2.createTrackbar('Canal', 'Ventana', 0, 2, nothing)
#wrap = cv2.copyMakeBorder(img,10,10,10,10,cv2.BORDER_WRAP)

while(1):
    #plt.subplot(235),plt.imshow(wrap,'gray'),plt.title('WRAP')
    cv2.imshow('Ventana', img)
    #plt.show()
        
    k = cv2.waitKey(0)
    if k == 27:
        break
     
    v = cv2.getTrackbarPos('Value', 'Ventana')
    c = cv2.getTrackbarPos('Canal','Ventana')
    
    img[:,:,c] = v
    print (c,v)
    
    

#cv2.imwrite('Colag.jpg', img)    
cv2.destroyAllWindows()
