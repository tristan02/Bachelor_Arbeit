
import numpy as np
import cv2
from matplotlib.backends.backend_webagg import WebAggApplication

img = cv2.imread('rgb.jpg',0)

cv2.imshow('imagen', img)
print('Pulsando s guardara la imagen, ESC significara que no la quiere guardar')
k = cv2.waitKey(0)

if k == 115:
    cv2.imwrite('rgb_grises.jpg', img)
elif k == 27:
    cv2.destroyWindow('imagen')
    print('Ha descartado la imagen')

print (k)
cv2.destroyAllWindows()



''' Codigo de la pagina Web:
img = cv2.imread('messi5.jpg',0)
cv2.imshow('image',img)
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',img)
    cv2.destroyAllWindows()'''