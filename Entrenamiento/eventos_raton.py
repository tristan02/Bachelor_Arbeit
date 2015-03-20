import cv2
import numpy as np
color = 0
mode = False
#Varialbes globales para pintar la linea
ix,iy = 0,0

def draw_figur(event,x,y,flags,param):
    global color,ix,iy
    if event == cv2.EVENT_FLAG_LBUTTON:
        if color == 0 or color == 1:
            if mode:
                cv2.circle(img,(x,y),20,(255,0,0),-1)
            else:
                cv2.rectangle(img,(x,y),(x+29,y+29),(255,0,0),10)
            color += 1
            if color == 4:
                color = 0
        elif color == 2 or color == 3:
            if mode:
                cv2.circle(img,(x,y),20,(0,0,255),-1)
            else:
                cv2.rectangle(img,(x,y),(x+29,y+29),(0,0,255),10)
            color += 1
            if color == 4:
                color = 0
    elif event == cv2.EVENT_FLAG_RBUTTON:
        cv2.circle(img,(250,250),1000,(0,0,0),-1)
    '''elif event == cv2.EVENT_FLAG_ALTKEY:
        ix,iy = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        cv2.line(img, (ix,iy), (x,y), (0,255,0),15)'''

# Create a black image, a window and bind the function to window
img = np.zeros((512,512,3),np.uint8)
cv2.namedWindow('ventana')
cv2.setMouseCallback('ventana', draw_figur)

while(1):
    cv2.imshow('ventana', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('c'):
        mode = not mode
    elif cv2.waitKey(20) & 0xFF == 27:
        break
    
cv2.destroyAllWindows()