import cv2
import numpy as np

p,mb,b,gb,bi = 1,0,0,0,1

def nothing(x):
    pass

img = cv2.imread('border.jpg')
fils, cols = img.shape[:2]

cv2.namedWindow('valores')

cv2.createTrackbar('promedio', 'valores', 1, 100, nothing)
cv2.createTrackbar('median_blur', 'valores', 0, 48, nothing)
cv2.createTrackbar('blur', 'valores', 0, 48, nothing)
cv2.createTrackbar('gaussian_blur', 'valores', 0, fils, nothing)
cv2.createTrackbar('bilateral', 'valores', 1, 200, nothing)

while(1):
    if b%2 == 0:
        b+=1
    if gb%2 == 0:
        gb+=1
    if mb%2 == 0:
        mb+=1
    #2D Convolution
    kernel = np.ones((5,5),np.float32)/p
    res = cv2.filter2D(img,-1,kernel)
    #median blur, efectivo para quitar ruido
    res = cv2.medianBlur(res,mb)
    #blur normal
    res = cv2.blur(res,(b,b))
    #gaussian_blur
    res = cv2.GaussianBlur(res,(gb,gb),0)
    #bilateral
    res = cv2.bilateralFilter(res,bi,50,50)
    
    cv2.imshow('Filtrando imagenes',res)
     
    p = cv2.getTrackbarPos('promedio', 'valores')
    mb = cv2.getTrackbarPos('median_blur', 'valores')
    b = cv2.getTrackbarPos('blur','valores')
    gb = cv2.getTrackbarPos('gaussian_blur','valores')
    bi = cv2.getTrackbarPos('bilateral','valores')

    k = cv2.waitKey(0)
    if k==27:
        break
#cv2.imwrite('mezcla.jpg', dst)    
cv2.destroyAllWindows()