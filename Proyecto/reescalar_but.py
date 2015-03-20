import cv2
import numpy as np


#Funcion a le que le pasamos dos imagenes en escala de grises y intenta un matchtemplate del primer elemento en el segundo.
#Devuelve la imagen con el rectangulo pintado, la mnLoc (x,y) y el valor de acierto (mn)
#No es del todo eficiente =(
def match(img):
    
    tmp_n = cv2.imread('tmp_n.jpg')
    tmp_p = cv2.imread('tmp_p.jpg')
    tmp_g = cv2.imread('tmp_p.jpg')
    tmp_n = cv2.cvtColor(tmp_n, cv2.CV_32FC1)
    tmp_p = cv2.cvtColor(tmp_p, cv2.CV_32FC1)
    tmp_g = cv2.cvtColor(tmp_p, cv2.CV_32FC1)
    
    bad = True
    
    while(bad):
        d1 = cv2.matchTemplate(tmp_n, img, cv2.cv.CV_TM_SQDIFF_NORMED)
        d2 = cv2.matchTemplate(tmp_p, img, cv2.cv.CV_TM_SQDIFF_NORMED)
        d3 = cv2.matchTemplate(tmp_g, img, cv2.cv.CV_TM_SQDIFF_NORMED)
        
        mn1,_,mnLoc1,_ = cv2.minMaxLoc(d1)
        mn2,_,mnLoc2,_ = cv2.minMaxLoc(d2)
        mn3,_,mnLoc3,_ = cv2.minMaxLoc(d3)
        
        mn = min(mn1,mn2,mn3)
        
        if mn == mn1:
            MPx,MPy = mnLoc1
            trows,tcols = tmp_n.shape[:2]
        elif mn == mn2:
            MPx,MPy = mnLoc2
            trows,tcols = tmp_p.shape[:2]
        else:
            MPx,MPy = mnLoc3
            trows,tcols = tmp_g.shape[:2]    
           
        h,w = img.shape[:2]
        # Print it, for comparison    
        print mn
           
        if mn >= 0.24 and bad == True:
            #recortamos la imagen para acercarnos mas al resultado
            crop_img = img[h-70:h,0:w-70] # Crop from x, y, w, h -> 100, 200, 300, 400
            # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h] 
            bad = False
  
        else:
            bad = False
     
    # Draw the rectangle 
    cv2.rectangle(img, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)
    
    return MPx,MPy,mn

def cero_tres(img):
    
    h,w = img.shape[:2]
    mask = np.zeros((h,w,3), np.uint8)
    v0 = [h,w]
    v3 = [0,0]    
    
    h,w = img.shape[:2]
   
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    #Detecta perfectamente el zero y el tres
    dst = cv2.cornerHarris(gray,15,21,0.22)   
    
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)   

    # Threshold for an optimal value, it may vary depending on the image.
    mask[dst>0.005*dst.max()]=[0,0,255]        

    for x in range(w):
        for y in range(h):
            px = mask[y,x]
            #Si el pixel es rojo mejoramos el valor para seguir bajando                       
            if px[0] == 0 and px[1] == 0 and px[2] == 255:
                if v3[0] < y or v3[1] < y:                    
                    #print 'Valor mejorado. Antes:(' + str(v0[0]) +',' + str(v0[1]) + ') ahora:(' + str(x) +',' + str(y) + ')'
                    v3 = [x,y]
                if v0[0] > x or v0[1] < y:
                    v0 = [x,y]
    #print str(v0[0]) + '---->' + str(v0[1])
    cv2.circle(img,(v3[0],v3[1]), 10, (0,255,0), -1)
    cv2.circle(img,(v0[0],v0[1]), 10, (255,0,0), -1)
    sol = v3[0]-v0[0]
    return img,sol


for i in range(100):
    path = 'ima/img (' + str(i+1) + ').jpg'
    img = cv2.imread(path)
    
    #edges = cv2.Canny(img,270,500)    
    #cv2.imwrite('canny.jpg', edges)
    
    #img = cv2.imread('canny.jpg')
    #img_g = cv2.cvtColor(img, cv2.CV_32FC1)
    
    #x,y,mn = match(img_g)
    
    img_z,sol = cero_tres(img)
    print sol
    cv2.imshow('output',img_z)   
    cv2.waitKey()
    

cv2.destroyAllWindows()