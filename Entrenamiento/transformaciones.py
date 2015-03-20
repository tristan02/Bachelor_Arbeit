import cv2
import numpy as np

s,b,mx,my,rz,rx,ry = 1,0,0,0,0,200,200

def nothing(x):
    pass

img = cv2.imread('Acoplada.jpg')
fils, cols = img.shape[:2]
cv2.namedWindow('valores')
cv2.createTrackbar('size', 'valores', 1, 20, nothing)
cv2.createTrackbar('blur', 'valores', 0, 48, nothing)
cv2.createTrackbar('move_X', 'valores', 0, cols, nothing)
cv2.createTrackbar('move_Y', 'valores', 0, fils, nothing)
cv2.createTrackbar('rotate_Z', 'valores', 0, 360, nothing)
cv2.createTrackbar('rotate_X', 'valores', 200, 200, nothing)
cv2.createTrackbar('rotate_Y', 'valores', 200, 200, nothing)

while(1):
    if b%2 == 0:
        b+=1
    #Enfoque
    res = cv2.medianBlur(img,b)
    #Reescalado
    res = cv2.resize(res,(s*cols, s*fils), interpolation = cv2.INTER_CUBIC)
    #Movimiento respecto de X e Y
    M = np.float32([[1,0,mx],[0,1,my]])
    res = cv2.warpAffine(res,M,(cols,fils))
    #Rotacion
    M = cv2.getRotationMatrix2D((cols/2,fils/2),rz,1)
    res = cv2.warpAffine(res,M,(cols,fils))
    #Perspectiva
    pts1 = np.float32([[50,50],[200,50],[50,200]])
    pts2 = np.float32([[50,50],[ry,50],[50,rx]])
    M = cv2.getAffineTransform(pts1,pts2)
    res = cv2.warpAffine(res,M,(cols,fils))
    cv2.imshow('Transformaciones en imagenes',res)
     
    s = cv2.getTrackbarPos('size', 'valores')
    b = cv2.getTrackbarPos('blur', 'valores')
    mx = cv2.getTrackbarPos('move_X','valores')
    my = cv2.getTrackbarPos('move_Y','valores')
    rz = cv2.getTrackbarPos('rotate_Z','valores')
    rx = cv2.getTrackbarPos('rotate_X','valores')
    ry = cv2.getTrackbarPos('rotate_Y','valores')

    k = cv2.waitKey(0)
    if k==27:
        break
#cv2.imwrite('mezcla.jpg', dst)    
cv2.destroyAllWindows()