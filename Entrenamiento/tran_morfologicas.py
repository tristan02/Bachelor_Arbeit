import cv2
import numpy as np

kernel = np.ones((0,0),np.uint8)
salir = False

img = cv2.imread('img (96).jpg',0)
#img = cv2.bitwise_not(img)

cv2.namedWindow('Trans_morfo')
cv2.namedWindow('valores')

def exit(num):
    global salir
    if num == 1:
        salir = True
#setter del kernel
def set_erode(num):
    global img,kernel
    img = cv2.erode(img,kernel,iterations = num)
    recarga_img() 

def set_kernel(num):
    global kernel
    kernel = np.ones((num,num),np.uint8)
    recarga_img()

def set_dilate(num):
    global img,kernel
    img = cv2.dilate(img,kernel,iterations = num)
    recarga_img()
    
def recarga_img():
    cv2.imshow('Trans_morfo', img)

cv2.createTrackbar('kernel', 'valores', 0, 10, set_kernel)
cv2.createTrackbar('erode', 'valores', 0, 10, set_erode)
cv2.createTrackbar('dilate', 'valores', 0, 10, set_dilate)
cv2.createTrackbar('salir?', 'valores', 0, 1, exit)

while (salir == False):
    cv2.imshow('Trans_morfo', img)
    #img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    cv2.waitKey(0)

cv2.imwrite("tmpp.jpg", img)   
cv2.destroyAllWindows()
    